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

#---------------------------------#

#make a directory to store merged files temporarily
if not os.path.exists("batch/temp_root/") :
    os.makedirs("batch/temp_root")

user = os.environ.get('USER')
if usedirect:
    eospath = '/eos/uscms/store/user/' + user + '/'
else:
    eospath = 'root://cmseos.fnal.gov//store/user/' + user + '/'
    
    # inputpath = eospath + inputpath

print "Processing input path", inputpath, "to output path", outputpath

dir_output_data = outputpath + "dataprocess/"
dir_output_bkg  = outputpath + "MC/backgrounds/"
dir_output_sig  = outputpath + "MC/signals/"

#list_dirs = os.listdir(inputpath) #list all first files to get 1 per dataset
command = 'eos root://cmseos.fnal.gov ls ' + '/store/user/'+user+'/'+inputpath
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
stdout, stderr = process.communicate()
list_dirs = stdout.split('\n')

list_processed = []

for dirname in list_dirs:
    if dirname == "":
        continue
    samplename = dirname.split("_")
    outputname = ""
    for index in range(len(samplename)-1):        
        if index > 0:
            outputname = outputname + "_"
        outputname = outputname + samplename[index]

    isSignal = "EMu_" in dirname or "ETau_" in dirname or "MuTau_" in dirname
    isData = "SingleElectron" in dirname or "SingleMuon" in dirname

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

    list_processed.append(outputname)
    print "Processing dataset", outputname
    
    inputname  = outputname + "_*.root"
    outputname = outputname.replace("output_" ,"")
    # tmpoutput  = outputname + "-tmp.root"
    outputname = outputname + ".root"
    lscommand  = 'eos root://cmseos.fnal.gov ls ' + '/store/user/'+user+'/' + inputpath + inputname
    process = subprocess.Popen(lscommand.split(), stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    inputlist = stdout.split('\n')
    if usedirect:
        inputlist = ['/eos/uscms/store/user/'+user+'/'+inputpath+s for s in inputlist]
    else:
        inputlist = ['root://cmseos.fnal.gov//store/user/'+user+'/'+inputpath+s for s in inputlist]
    hadd_command = "../haddnano.py " + "batch/temp_root/" + outputname
    if inputlist == []:
        print "Not datafiles found for dataset", outputname
        if dosingle:
            exit()
        continue
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

    # Copy back the merged data:
    copy_command = 'xrdcp -f batch/temp_root/' + outputname + ' root://cmseos.fnal.gov//store/user/'+user+'/'+outputpath
    print copy_command
    os.system(copy_command)
    os.remove("batch/temp_root/%s" % (outputname))
    if dosingle:
        break

if dryrun:
    print "Completed dryrun!"
    exit()

            
print "All done!"
