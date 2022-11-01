import ROOT
import os, sys
import shutil
import subprocess
import argparse
from importlib import import_module

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
p.add_argument('--tag'      , help='Dataset tag to process',default="", required=False)
p.add_argument('--veto'     , help='Comma separated list of tags to not process (e.g. DY,ttbar,Embed)',default="", required=False)
p.add_argument('--dryrun'   , help='Setup merging without running', action='store_true', required=False)
p.add_argument('--dosingle' , help='Merge first dataset only', action='store_true', required=False)
p.add_argument('--usedirect', help='Use the direct EOS path instead of XROOTD', action='store_true', required=False)
p.add_argument('--copylocal', help='Copy files locally to merge', action='store_true', required=False)
p.add_argument('--jsononly' , help='Only process lumi json files', action='store_true', required=False)
p.add_argument('--verbose'  , help='Print additional information', action='store_true', required=False)

args = p.parse_args()

inputpath  = args.input_dir
outputpath = args.outdir
mc_data    = args.mc_data
year       = args.year
tag        = args.tag
veto       = args.veto.split(',')
dryrun     = args.dryrun
dosingle   = args.dosingle
usedirect  = args.usedirect
copylocal  = args.copylocal
jsononly   = args.jsononly
verbose    = args.verbose

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

dir_output_data = outputpath + "dataprocess/"
dir_output_bkg  = outputpath + "MC/backgrounds/"
dir_output_sig  = outputpath + "MC/signals/"

#list_dirs = os.listdir(inputpath) #list all first files to get 1 per dataset
if host == 'lxplus':
    #FIXME: remove non-root files from search list
    command = 'eos root://eoscms.cern.ch ls /store/group/phys_smp/ZLFV/%s' % (inputpath)
else:
    command = 'eos root://cmseos.fnal.gov ls /store/user/%s/%s*.root' % (user, inputpath)

if verbose:
    print "Running command", command
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
stdout, stderr = process.communicate()
list_dirs = stdout.split('\n')

list_processed = []

#process each input dataset, skipping files of already processed datasets
for dirname in list_dirs:
    if verbose:
        print "Found file", dirname
    if dirname == "" or dirname[-4:] != "root":
        continue
    samplename = dirname.split("_")
    outputname = ""
    for index in range(len(samplename)-1):        
        if index > 0:
            outputname = outputname + "_"
        outputname = outputname + samplename[index]

    #determine if the file is data or embedding for special processing (e.g. lumi files)
    isData = "SingleElectron" in dirname or "SingleMuon" in dirname
    isEmbed = "Embed-" in dirname

    #skip datasets not being considered in the processing
    if (doDataMC < 0 and isData) or (doDataMC > 0 and not isData):
        continue
    if year != "" and year not in outputname:
        continue
    if outputname in list_processed:
        continue
    if tag != "" and tag not in outputname:
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
    if host == 'lxplus': #can't use wildcard in lxplus 'ls' command
        inputname  = outputname + "_"
    else:
        inputname  = outputname + "_*.root"
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
            lscommand = 'eos root://cmseos.fnal.gov ls /store/user/%s/%s%s' % (user, inputpath, inputname)
        if verbose: print "ls command:", lscommand
        process = subprocess.Popen(lscommand.split(), stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()
        inputlist = stdout.split('\n')
        if host == 'lxplus': inputlist = [l for l in inputlist if inputname in l and '.root' in l]
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
                
            
        #merge the dataset files
        hadd_command = "time ../haddnano.py " + tmp_dir + outputname
        if verbose: print "Hadd command:", hadd_command
        if inputlist == []:
            print "Not datafiles found for dataset", outputname
            if dosingle:
                exit()
            continue
        #ensure only root files are considered, adding each to the merge command
        for data_file in inputlist:
            if ".root" in data_file:
                hadd_command = hadd_command + " " + data_file

        print "Merging into output dataset", outputname
        if not dryrun:
            os.system(hadd_command)
        else:
            print hadd_command
            if dosingle:
                exit()
            continue

        #remove the input files if copied over after merging
        if copylocal:
            for infile in inputlist:
                os.remove(infile)

        # Copy back the merged data:
        copy_command = 'time xrdcp -f ' + tmp_dir + outputname
        if host == 'lxplus':
            copy_command = copy_command + ' root://eoscms.cern.ch//store/group/phys_smp/ZLFV/' + outputpath
        else:
            copy_command = copy_command + ' root://cmseos.fnal.gov//store/user/' + user +'/'  + outputpath
        print copy_command
        os.system(copy_command)
        os.remove("%s%s" % (tmp_dir, outputname))

    # Process lumi files, if relevant
    if isData or isEmbed:
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
