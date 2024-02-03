import sys, os, glob, subprocess, fileinput, math, datetime
from subprocess import PIPE, Popen

def get_current_time():
    now = datetime.datetime.now()
    currentTime = '{0:02d}{1:02d}{2:02d}_{3:02d}{4:02d}{5:02d}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second)
    return currentTime

def make_directory(filePath, clear = True):
    if not os.path.exists(filePath):
        os.system('mkdir -p '+filePath)
    if clear and len(os.listdir(filePath)) != 0:
        os.system('rm '+filePath+'/*')

def inputFiles_from_txt(txt):
    ftxt = open(txt)
    inputFiles = ftxt.readlines()
    inputFiles = [f.strip() for f in inputFiles]
    return inputFiles


def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]


class JobConfig():
    '''Class for storing configuration for each dataset'''
    def __init__(self, dataset, nEvtPerJobIn1e6, year, isData, suffix, inputDBS = "global", maxEvtPerDataset = None,
                 user_redir = None, user_nfiles = 10, user_tag = None, user_file = None):
        self._dataset   = dataset
        self._nEvtPerJobIn1e6 = nEvtPerJobIn1e6
        self._inputDBS = inputDBS
        #for accessing datasets not in DAS
        self._user_redir = user_redir
        self._user_nfiles = user_nfiles
        self._user_tag = user_tag
        self._user_file = user_file #local file list

        #maximum processing info
        self._maxEvtPerDataset = maxEvtPerDataset
        
        # need to pass to executable
        self._year      = year
        self._isData    = isData
        self._suffix    = suffix

                

class BatchMaster():
    '''A tool for submitting batch jobs'''
    def __init__(self, analyzer, config_list, stage_dir, output_dir,
                 executable='execBatch.sh', location='lpc', maxFilesPerJob = -1,
                 memory = 4800, disk = 5000000, queue = 'tomorrow'):
        self._current     = os.path.abspath('.')

        self._analyzer       = analyzer
        self._config_list    = config_list
        self._stage_dir      = stage_dir
        self._output_dir     = output_dir

        self._executable     = executable
        self._location       = location
        self._maxFilesPerJob = maxFilesPerJob
        self._memory         = memory
        self._disk           = disk
        self._queue          = queue

    #-------------------------------------------------------------------------------------------------------------------
    def split_jobs_for_cfg(self, cfg):
        if cfg._user_redir is None and cfg._user_file is None:
            return self.split_jobs_for_cfg_das(cfg)
        else:
            return self.split_jobs_for_cfg_user(cfg)

    #-------------------------------------------------------------------------------------------------------------------
    def split_jobs_for_cfg_user(self, cfg):
        xrootd = 'cmsxrootd.fnal.gov' if self._location == 'lpc' else 'xrootd-cms.infn.it' #'cms-xrd-global.cern.ch'
        if cfg._user_file is None:
            eosQuery_outFile = 'eosQuery_%s.txt' % (cfg._suffix)
            eosQuery_command = 'eos %s ls %s > %s' % (cfg._user_redir, cfg._dataset, eosQuery_outFile)
            os.system(eosQuery_command)        
            ftxt = open(eosQuery_outFile)
            fileList = ["root://%s//%s/%s" % (xrootd, cfg._dataset, f.strip()) for f in ftxt.readlines() if '.root' in f and (cfg._user_tag is None or cfg._user_tag in f)]
        else:
            # print os.getcwd(), os.getenv('CMSSW_BASE')
            file_path = os.path.join(os.getenv('CMSSW_BASE'), "src/PhysicsTools/NanoAODTools/condor/"+cfg._user_file)
            # print file_path
            ftxt = open(file_path, 'r')
            fileList = ["root://%s//%s" % (xrootd, f.strip()) for f in ftxt.readlines() if '.root' in f and (cfg._user_tag is None or cfg._user_tag in f)]
        ftxt.close()
        nFiles = len(fileList)
        if nFiles <= 0:
            print "ERROR! No sample files are found! Exiting..."
            exit()
        # Split the files by requested number of files / job
        nFilesPerJob = self._maxFilesPerJob if self._maxFilesPerJob > 0 and self._maxFilesPerJob < cfg._user_nfiles else cfg._user_nfiles
        nJobs = int(math.ceil(nFiles/nFilesPerJob))
        sources = [ fileList[i:i+nFilesPerJob] for i in range(0, len(fileList), nFilesPerJob) ]
        print "EOS for dataset: ", cfg._dataset
        print "**************************************************"
        print "*  dataset: ", cfg._suffix
        print "*  X events in {} files, raw_nJobs {}, nJobs {}".format(nFiles, nJobs, len(sources))
        print "**************************************************"        
        if cfg._user_file is None:
            print "saved the EOS output to ", eosQuery_outFile

        # return a list with len=nJobs, For the given dataset
        return sources

    #-------------------------------------------------------------------------------------------------------------------
    def split_jobs_for_cfg_das(self, cfg):
        # query the root files using das commandline tool
        print "das query files"
        dasQuery_outFile = 'dasQuery_{}.txt'.format(cfg._suffix)
        if cfg._inputDBS == "global" :
            dasQuery_command = 'das_client -query="file dataset={}" > {}'.format(cfg._dataset, dasQuery_outFile)
        else :
            dasQuery_command = 'das_client -query="file dataset={} instance=prod/{}" > {}'.format(cfg._dataset, cfg._inputDBS, dasQuery_outFile)
        os.system(dasQuery_command)
        
        ftxt = open(dasQuery_outFile)
        xrootd = 'cmsxrootd.fnal.gov' if self._location == 'lpc' else 'xrootd-cms.infn.it' #'cms-xrd-global.cern.ch'
        fileList = ["root://%s//%s" % (xrootd, f.strip()) for f in ftxt.readlines()]
        ftxt.close()
        nFiles = len(fileList)
        if nFiles <= 0:
            print "ERROR! No sample files are found! Exiting..."
            exit()
            
        # query number of events in the dataset
        print "das query number of events"
        if cfg._inputDBS == "global":
            output  = cmdline('das_client -query="dataset={} | grep dataset.nevents " '.format(cfg._dataset))
        else :
            output  = cmdline('das_client -query="dataset={} instance=prod/{} | grep dataset.nevents " '.format(cfg._dataset, cfg._inputDBS))
        nEvents = -1
        for l in output.splitlines():
            try: nEvents = int(l); break
            except: continue
        if nEvents < 0:
            print "ERROR! Unable to get the number of events for the dataset! Will use file based..."
            nJobs = nFiles
        else :
            # Split files to requested number.  Cannot exceed the number of files being run over.
            nJobs = int(math.ceil(nEvents/(1000000.0*cfg._nEvtPerJobIn1e6)))
            nJobs = nFiles if nJobs > nFiles else nJobs
            # enforce a maximum allowed number of files per job, if defined
            nJobs = int(math.ceil(nFiles/(1.*self._maxFilesPerJob))) if self._maxFilesPerJob > 0 and nFiles/(1.*nJobs) > self._maxFilesPerJob else nJobs
        nFilesPerJob = int(math.ceil(float(nFiles)/float(nJobs)))
        sources = [ fileList[i:i+nFilesPerJob] for i in range(0, len(fileList), nFilesPerJob) ]
        # check if dataset is larger than maximum dataset size
        if cfg._maxEvtPerDataset is not None and cfg._maxEvtPerDataset > 0 and cfg._maxEvtPerDataset < nEvents:
            #reduce number of jobs to keep closer to the maximum
            nSources = len(sources)
            last_job = int(math.ceil(cfg._maxEvtPerDataset / (nEvents * 1.) * nSources))
            if last_job < len(sources):
                sources = [ sources[i] for i in range(0, last_job) ]
            

        print "DAS for dataset: ", cfg._dataset
        print "**************************************************"
        print "*  dataset: ", cfg._suffix
        print "*  {} events in {} files, raw_nJobs {}, nJobs {}".format(nEvents, nFiles, nJobs, len(sources))
        print "**************************************************"        
        print "saved the DAS output to ", dasQuery_outFile

        # return a list with len=nJobs, For the given dataset
        return sources

    #-------------------------------------------------------------------------------------------------------------------
    def make_batch_lpc(self, cfg):
        '''
        Prepares for submission to lpc.  Does the following:

        1. Generates input_files.txt with files to run over
        2. Write batch configuration file
        '''

        if self._location == 'lpc':
            output_dir = 'root://cmseos.fnal.gov/' + self._output_dir
            print output_dir
        elif self._location == 'lxplus' and self._location[:4] != '/eos':
            output_dir = 'root://eoscms.cern.ch/' + self._output_dir
        else:
            output_dir = self._output_dir

        ## Writing the batch config file
        batch_tmp = open('batchJob_{0}.jdl'.format(cfg._suffix), 'w')
        batch_tmp.write('Universe              = vanilla\n')
        batch_tmp.write('Should_Transfer_Files = YES\n')
        batch_tmp.write('WhenToTransferOutput  = ON_EXIT\n')
        batch_tmp.write('Notification          = Never\n')


        if self._location in ['lpc', 'lxplus']:
            batch_tmp.write('Requirements          = OpSys == "LINUX"&& (Arch != "DUMMY" )\n')
            batch_tmp.write('request_disk          = %i\n' % (self._disk)) # 10 GB to xrdcp temp nanoAOD xrootd reading
            batch_tmp.write('request_memory        = %i\n' % (self._memory))
            if self._location == 'lxplus':
                # batch_tmp.write('+MaxRuntime           = 1440\n') #FIXME: remove if not needed
                batch_tmp.write('+JobFlavour           = \"%s\"\n' % (self._queue)) #see https://twiki.cern.ch/twiki/bin/view/ABPComputing/LxbatchHTCondor#Queue_Flavours

        batch_tmp.write('\n')

        sources = self.split_jobs_for_cfg(cfg)
        for i, source in enumerate(sources):

            ## make file with list of inputs ntuples for the analyzer
            input_file = open('input_{}_{}.txt'.format(cfg._suffix, i+1), 'w')
            if self._location in ['lpc', 'lxplus']:
                for s in source:
                    input_file.write( s + "\n")
            input_file.close()


            ### set output directory
            batch_tmp.write('Arguments             = {0} {1} {2} {3} {4} {5} \n'.format(i+1, cfg._year, cfg._isData, cfg._suffix, output_dir, self._analyzer))
            batch_tmp.write('Executable            = {0}\n'.format(self._executable))
            batch_tmp.write('Transfer_Input_Files  = source.tar.gz, input_{0}_{1}.txt\n'.format(cfg._suffix, i+1))
            batch_tmp.write('Output                = reports/{0}_{1}_$(Cluster)_$(Process).stdout\n'.format(cfg._suffix, i+1))
            batch_tmp.write('Error                 = reports/{0}_{1}_$(Cluster)_$(Process).stderr\n'.format(cfg._suffix, i+1))
            batch_tmp.write('Log                   = reports/{0}_{1}_$(Cluster)_$(Process).log   \n'.format(cfg._suffix, i+1))
            batch_tmp.write('Queue\n\n')

        batch_tmp.close()
        

    def submit_to_batch(self, doSubmit=True):
        '''
        Submits batch jobs to scheduler.  Currently only works
        for condor-based batch systems.
        '''
        #  set stage dir
        print 'Running on {0}'.format(self._location)
        print 'Setting up stage directory...'
        current_time = get_current_time()
        self._stage_dir  = '{0}/{1}_{2}'.format(self._stage_dir, self._analyzer, current_time)
        make_directory(self._stage_dir, clear=False)

        # set output dir
        print 'Setting up output directory...'
        self._output_dir  = '{0}/{1}_{2}'.format(self._output_dir, self._analyzer, current_time)
        if self._location == 'lpc':
            make_directory('/eos/uscms/' + self._output_dir, clear=False)
        elif self._location == 'lxplus':
            make_directory('/eos/cms/' + self._output_dir, clear=False)

        # tar cmssw 
        print 'Creating tarball of current workspace in {0}'.format(self._stage_dir)
        if os.getenv('CMSSW_BASE') == '':
            print 'You must source the CMSSW environment you are working in...'
            exit()
        else:
            cmssw_version = os.getenv('CMSSW_BASE').split('/')[-1]
            if doSubmit:
                os.system('tar czf {0}/source.tar.gz -X $CMSSW_BASE/batch_exclude.txt -C $CMSSW_BASE/.. {1}'.format(self._stage_dir, cmssw_version))

        subprocess.call('cp {0} {1}'.format(self._executable, self._stage_dir), shell=True)
        os.chdir(self._stage_dir)
        make_directory('reports', clear=False)
    

        # submit
        print 'Ready to submit to batch system {0}!'.format(self._location)
        if self._location in ['lpc', 'lxplus']:
            for cfg in self._config_list:
                print "\n\n", cfg._suffix
                self.make_batch_lpc(cfg)
                if doSubmit:
                    subprocess.call('condor_submit batchJob_{0}.jdl'.format(cfg._suffix), shell=True)
