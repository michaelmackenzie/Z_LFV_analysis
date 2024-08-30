import ROOT
import os, sys
import shutil
import subprocess
import argparse
from importlib import import_module
from math import ceil

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

ROOT.PyConfig.IgnoreCommandLineOptions = True


#---------------------------------#
p = argparse.ArgumentParser(description='Select whether to download MC or data')
p.add_argument('input_dir'  , help='Type e.g. input file path')
p.add_argument('--outdir'   , help='Type e.g. output file path', default="", required=False)
p.add_argument('--mc_data'  , help='Type MC or Data for only MC or Data', default="", required=False)
p.add_argument('--year'     , help='Specific year to process',default="", required=False)
p.add_argument('--tag'      , help='Dataset tag list to process',default="", required=False)
p.add_argument('--veto'     , help='Comma separated list of tags to not process (e.g. DY,ttbar,Embed)',default="", required=False)
p.add_argument('--dryrun'   , help='Setup merging without running', action='store_true', required=False)
p.add_argument('--dosingle' , help='Merge first dataset only', action='store_true', required=False)
p.add_argument('--usedirect', help='Use the direct EOS path instead of XROOTD', action='store_true', required=False)
p.add_argument('--copylocal', help='Copy files locally to merge', action='store_true', required=False)
p.add_argument('--segments' , help='Use job segments rather than a merged ntuple', action='store_true', required=False)
p.add_argument('--onlylink' , help='Link segments instead of copying them over', action='store_true', required=False)
p.add_argument('--mergeseg' , help='Merge existing segment files', action='store_true', required=False)
p.add_argument('--maxsize'  , help='Maximum output file size in MB, larger datasets are split into sub-datasets', default="", required=False)
p.add_argument('--jsononly' , help='Only process lumi json files', action='store_true', required=False)
p.add_argument('--skipjson' , help='Skip lumi json files', action='store_true', required=False)
p.add_argument('--verbose'  , help='Print additional information', action='store_true', required=False)

args = p.parse_args()

inputpath  = args.input_dir
outputpath = args.outdir
mc_data    = args.mc_data
year       = args.year
tag        = args.tag.split(',')
veto       = args.veto.split(',')
dryrun     = args.dryrun
dosingle   = args.dosingle
usedirect  = args.usedirect
copylocal  = args.copylocal
segments   = args.segments
onlylink   = args.onlylink
mergeseg   = args.mergeseg
maxsize    = args.maxsize
jsononly   = args.jsononly
skipjson   = args.skipjson
verbose    = args.verbose

if copylocal and segments:
    print "Can't use both --copylocal and --segments!"
    exit()
if onlylink and not segments:
    print "--onlylink is only defined when using --segments!"
    exit()
if jsononly and skipjson:
    print "Can't use --jsononly and --skipjson"
    exit()
if maxsize != "":
    maxsize = int(maxsize)
    print "Using a maximum output file size of", maxsize, "MB"
else:
    maxsize = -1

if inputpath[-1:] != '/':
    inputpath = inputpath + '/'

if outputpath == "":
    outputpath = "lfvanalysis_rootfiles/"
doDataMC = 0
if mc_data == "MC":
    print "Only processing MC..."
    doDataMC = -1
elif mc_data == "Data":
    print "Only processing Data..."
    doDataMC = 1
elif mc_data != "":
    print "Unrecognized Data/MC option! Ignoring it..."
if year != "":
    print "Processing only year tag", year

if outputpath[-1] != '/': outputpath += '/'
print "Using input path %s and output path %s" % (inputpath, outputpath)

#---------------------------------#

user = os.environ.get('USER')
hostname = os.environ.get('HOSTNAME')
host = 'lxplus' if 'lxplus' in hostname else 'lpc'


if host == 'lpc':
    #make a directory to store merged files temporarily
    if not os.path.exists("batch/temp_root/") :
        os.makedirs("batch/temp_root")
    tmp_dir = 'batch/temp_root/'
else:
    tmp_dir = os.environ.get('TMPDIR') + '/'

#Get the list of files in the batch output directory
if usedirect:
    if host == 'lxplus':
        eospath = '/eos/cms/store/group/phys_smp/ZLFV/'
    else:
        eospath = '/eos/uscms/store/user/%s/' % (user)
else:
    if host == 'lxplus':
        eospath = 'root://eoscms.cern.ch//store/group/phys_smp/ZLFV/'
    else:
        eospath = 'root://cmseos.fnal.gov//store/user/%s/' % (user)
        
    # inputpath = eospath + inputpath
if verbose:
    print "Processing input path", inputpath, "to output path", outputpath

#list_dirs = os.listdir(inputpath) #list all first files to get 1 per dataset
if host == 'lxplus':
    #FIXME: remove non-root files from search list
    command = 'eos root://eoscms.cern.ch ls /store/group/phys_smp/ZLFV/%s' % (inputpath)
else:
    # command = 'eos root://cmseos.fnal.gov ls /store/user/%s/%s' % (user, inputpath)
    command = 'ls /eos/uscms/store/user/%s/%s' % (user, inputpath) #FIXME: eos <redir> ls doesn't work in Singularity
if verbose:
    print "Running command", command
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
if verbose:
    print "Sent command"
stdout, stderr = process.communicate()
list_dirs = stdout.split('\n')

list_processed = []

#process each input dataset, skipping files of already processed datasets
if verbose:
    print "Found directory list with %i entries" % (len(list_dirs))

for dirname in list_dirs:
    if verbose:
        print "Found file", dirname
    if dirname == "":
        continue
    if mergeseg:
        if '.' in dirname: continue
    elif dirname[-4:] != 'root':
        continue

    if mergeseg:
        outputname = dirname
    else:
        samplename = dirname.split("_")
        outputname = ""
        for index in range(len(samplename)-1):
            if index > 0:
                outputname = outputname + "_"
            outputname = outputname + samplename[index]

    if verbose:
        print "Using output name", outputname
    #determine if the file is data or embedding for special processing (e.g. lumi files)
    isData = "SingleElectron" in dirname or "SingleMuon" in dirname or 'MuonEG' in dirname
    isEmbed = "Embed-" in dirname

    #skip datasets not being considered in the processing
    if (doDataMC < 0 and isData) or (doDataMC > 0 and not isData):
        continue
    if year != "" and year not in outputname:
        continue
    if outputname in list_processed:
        continue
    tagged = False if len(tag) > 0 else True
    for tag_i in tag:
        if tag_i in outputname:
            tagged = True
    if not tagged:
        continue
    skip_dataset = False
    for veto_tag in veto:
        if veto_tag != "" and veto_tag in outputname:
            skip_dataset = True
            break
    if skip_dataset:
        continue

    #accept the dataset to process
    list_processed.append(outputname)
    print "Processing dataset", outputname

    #get the list of ntuple files to merge
    if mergeseg:
        inputname = outputname + '/'
    else:
        if host == 'lxplus': #can't use wildcard in lxplus 'ls' command
            inputname  = outputname + "_"
        else:
            # inputname  = outputname + "_*.root"
            inputname  = outputname  #FIXME: eos <redir> ls doesn't work in Singularity
    outputname = outputname.replace("output_" ,"")
    luminame = 'lumis_'+outputname

    if not jsononly:
        outputname = outputname + ".root"
        if host == 'lxplus':
            if usedirect:
                lscommand = 'ls /eos/cms/store/group/phys_smp/ZLFV/%s' % (inputpath)
            else:
                lscommand = 'eos root://eoscms.cern.ch ls /store/group/phys_smp/ZLFV/%s' % (inputpath)
        else:
            # lscommand = 'eos root://cmseos.fnal.gov ls /store/user/%s/%s%s' % (user, inputpath, inputname)
            lscommand = 'ls /eos/uscms/store/user/%s/%s' % (user, inputpath)  #FIXME: eos <redir> ls doesn't work in Singularity
        if verbose: print "ls command:", lscommand
        process = subprocess.Popen(lscommand.split(), stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()
        inputlist = stdout.split('\n')
        if verbose: print inputlist
        inputlist = [l for l in inputlist if inputname in l and '.root' in l]
        if verbose: print inputlist
        if mergeseg: inputlist = [inputname + l for l in inputlist]
        if usedirect:
            if host == 'lxplus':
                inputlist = ['/eos/cms/store/group/phys_smp/ZLFV/%s%s' % (inputpath, s) for s in inputlist]
            else:
                inputlist = ['/eos/uscms/store/user/%s/%s%s' % (user, inputpath, s) for s in inputlist]
        else:
            if host == 'lxplus':
                inputlist = ['root://eoscms.cern.ch//store/group/phys_smp/ZLFV/%s%s' % (inputpath, s) for s in inputlist]
            else:
                inputlist = ['root://cmseos.fnal.gov//store/user/%s/%s%s' % (user, inputpath, s) for s in inputlist]

        if copylocal:
            #write the inputs into the temp space to merge them locally
            local_list = []
            for infile in inputlist:
                local_copy = 'xrdcp -f %s %s' % (infile, tmp_dir)
                print local_copy
                if not dryrun:
                    os.system(local_copy)
                local_list.append('%s%s' % (tmp_dir, infile.split('/')[-1]))
            inputlist = local_list

        ###################################
        # Process the job segments
        if segments:
            ###################################
            # Use the job segment ntuples

            dataset_dir = '/eos/cms/store/group/phys_smp/ZLFV/' if host == 'lxplus' else '/eos/uscms/store/user/%s/' % (user)
            dataset_dir = dataset_dir + outputpath + outputname[:-5]
            if verbose:
                print "If needed, making directory %s" % (dataset_dir)
            os.system('[ ! -d %s ] && mkdir %s' % (dataset_dir, dataset_dir))
            # remove previous ntuples
            if not dryrun:
                os.system('rm %s/*' % (dataset_dir))
                for data_file in inputlist:
                    if not ".root" in data_file: continue
                    if verbose:
                        print "Adding segment file %s" % (data_file)
                    if onlylink:
                        print "Links not yet implemented!"
                    else:
                        if usedirect:
                            segment_copy = 'cp %s %s/' % (data_file, dataset_dir)
                        else:
                            redir = 'root://eoscms.cern.ch/' if host == 'lxplus' else 'root://cmseos.fnal.gov/'
                            segment_copy = 'xrdcp %s%s %s/' % (redir, data_file[data_file.index('/store'):], dataset_dir)
                        if verbose:
                            print "Segment copy: %s" % (segment_copy)    
                        os.system(segment_copy)

        else:
            ###################################
            # Merge the dataset files
            hadd_command = "time ../haddnano.py " + tmp_dir + outputname
            if inputlist == []:
                print "Not datafiles found for dataset", outputname
                if dosingle:
                    exit()
                continue
            #get the total dataset size in MB
            dataset_size = 0.
            ndataset_files = 0
            for data_file in inputlist:
                if ".root" in data_file:
                    ndataset_files += 1
                    file_location = data_file
                    file_location = file_location.replace("root://cmseos.fnal.gov//", "/eos/uscms/")
                    file_location = file_location.replace("root://eoscms.cern.ch//", "/eos/cms/")
                    file_size = os.stat(file_location).st_size / (1024*1024)
                    dataset_size += file_size
                    if verbose:
                        print data_file, "is", file_size, "MB"
            ndataset_files = int(ndataset_files)
            if verbose:
                print "Total dataset size is", dataset_size, "MB with", ndataset_files, "files"
            # number of datasets to split into based on size
            nsplit = 1 if maxsize <= 0 or dataset_size <= 0. else min(ndataset_files, ceil(dataset_size / maxsize))
            nsplit = int(nsplit)
            nfiles_per_subset = int(ndataset_files if nsplit == 1 else ceil(ndataset_files / float(nsplit)))
            if verbose:
                print "Output dataset splitting factor:", nsplit, "-->", nfiles_per_subset, "files per subset"
            print "Merging into output dataset", outputname
            # run a merge and copy back command for each output subset of the dataset
            for isplit in range(nsplit):
                index_start = int(nfiles_per_subset*isplit)
                index_end   = int(min(ndataset_files, nfiles_per_subset*(isplit+1)))
                subset_hadd_command = hadd_command
                if maxsize > 0:
                    subset_hadd_command.replace(".root", "-%i.root" % (isplit))
                #ensure only root files are considered, adding each to the merge command
                for data_file in inputlist[index_start:index_end]:
                    if ".root" in data_file:
                        subset_hadd_command = subset_hadd_command + " " + data_file
                if nsplit > 1: print " Merging subset dataset", isplit

                if not dryrun:
                    os.system(subset_hadd_command)
                else:
                    print subset_hadd_command

                #remove the input files if copied over after merging
                if copylocal:
                    for infile in inputlist[index_start:index_end]:
                        if not dryrun:
                            os.remove(infile)
                        else:
                            print "rm", infile

                # Copy back the merged data:
                if maxsize <= 0:
                    copy_command = 'time xrdcp -f ' + tmp_dir + outputname
                    rm_command   = tmp_dir + outputname
                else:
                    copy_command = 'time xrdcp -f ' + tmp_dir + outputname
                    copy_command = copy_command.replace(".root", "-%i.root" % (isplit))
                    rm_command = tmp_dir + outputname
                    rm_command = rm_command.replace(".root", "-%i.root" % (isplit))
                if host == 'lxplus':
                    copy_command = copy_command + ' root://eoscms.cern.ch//store/group/phys_smp/ZLFV/' + outputpath
                else:
                    copy_command = copy_command + ' root://cmseos.fnal.gov//store/user/' + user +'/'  + outputpath
                print copy_command
                if not dryrun:
                    os.system(copy_command)
                print "Removing", rm_command
                if not dryrun:
                    os.remove(rm_command)
            if dosingle:
                exit()

    ######################################################
    # Process lumi files, if relevant
    if (isData or isEmbed) and not skipjson:
        if host == 'lxplus':
            lumi_command = 'python ../scripts/combine_json.py /eos/cms/store/group/phys_smp/ZLFV/' + inputpath + luminame + '_'
            lumi_command += ' --out_name /eos/cms/store/group/phys_smp/ZLFV/' + outputpath + luminame + '.txt'
        else:
            lumi_command = 'python ../scripts/combine_json.py /eos/uscms/store/user/' + user + '/' + inputpath + luminame + '_'
            lumi_command += ' --out_name /eos/uscms/store/user/' + user + '/' + outputpath + luminame + '.txt'
        print lumi_command
        os.system(lumi_command)

    if dosingle:
        break

if dryrun:
    print "Completed dryrun!"
    exit()

            
print "All done!"
