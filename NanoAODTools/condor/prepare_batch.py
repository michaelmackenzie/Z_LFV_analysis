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
p.add_argument('input_dir' , help='Type e.g. input file path')
p.add_argument('--outdir'  , help='Type e.g. output file path', default="", required=False)
p.add_argument('--mc_data' , help='Type MC or Data for only MC or Data', default="", required=False)
p.add_argument('--year'    , help='Specific year to process',default="", required=False)
p.add_argument('--dryrun'  , help='Setup merging without running', action='store_true', required=False)
p.add_argument('--dosingle', help='Merge first dataset only', action='store_true', required=False)

args = p.parse_args()

inputpath  = args.input_dir
outputpath = args.outdir
mc_data    = args.mc_data
year       = args.year
dryrun     = args.dryrun
dosingle   = args.dosingle

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
if os.path.exists("batch/temp_root/") :
    shutil.rmtree("batch/temp_root/")
os.makedirs("batch/temp_root")
    

user = os.environ.get('USER')
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

    list_processed.append(outputname)
    print "Processing dataset", outputname
    
    inputname  = outputname + "_*.root"
    outputname = outputname.replace("output_" ,"")
    tmpoutput  = outputname + "-tmp.root"
    outputname = outputname + ".root"
    lscommand  = 'eos root://cmseos.fnal.gov ls ' + '/store/user/'+user+'/' + inputpath + inputname
    process = subprocess.Popen(lscommand.split(), stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    inputlist = stdout.split('\n')
    inputlist = ['root://cmseos.fnal.gov//store/user/'+user+'/'+inputpath+s for s in inputlist]
    hadd_command = "../haddnano.py " + "batch/temp_root/" + tmpoutput
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

    # print "Splitting output dataset selections:", outputname
    # split_command = "root.exe -q -b \"split_output_tree.C(\\\"batch/temp_root/%s\\\",\\\"batch/temp_root/%s\\\")\"" % (tmpoutput, outputname)
    # print split_command
    # os.system(split_command)
    # os.remove("batch/temp_root/%s" % (tmpoutput))
    os.system("mv batch/temp_root/%s batch/temp_root/%s" % (tmpoutput, outputname))

    if dosingle:
        break
if dryrun:
    print "Completed dryrun!"
    exit()

# Copy back the merged data:
copy_command = 'xrdcp -f batch/temp_root/*.root root://cmseos.fnal.gov//store/user/'+user+'/'+outputpath
print copy_command
os.system(copy_command)
    

# print "Finishing initial merging! Now merging data run sections..."
# # Now treat and merge samples
# for year in ["2016", "2017", "2018"]:
#     doSingleMu = False
#     for dataset in list_processed:
#         if "SingleMuonRun"+year in dataset:
#             doSingleMu = True
#             break
#     doSingleEle = False
#     for dataset in list_processed:
#         if "SingleElectronRun"+year in dataset:
#             doSingleEle = True
#             break
#     if doSingleMu:
#         hadd_command = "date +\"%r\"; ./haddnano.py " + dir_output_data + "LFVAnalysis_SingleMu_" + year + ".root " + dir_output_data + "LFVAnalysis_SingleMuonRun" + year + "*.root"
#         rm_command = "rm -rf " + dir_output_data + "LFVAnalysis_SingleMuonRun" + year + "*.root"
#         print hadd_command
#         # print rm_command
#         os.system(hadd_command)
#         # os.system(rm_command)
#     if doSingleEle:
#         hadd_command = "./haddnano.py " + dir_output_data + "LFVAnalysis_SingleEle_" + year + ".root " + dir_output_data + "LFVAnalysis_SingleElectronRun" + year + "*.root"
#         rm_command = "rm -rf " + dir_output_data + "LFVAnalysis_SingleElectronRun" + year + "*.root"

#         print hadd_command
#         # print rm_command
#         os.system(hadd_command)
#         # os.system(rm_command)
        
        
print "All done!"
