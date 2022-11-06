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
p.add_argument('--tolxplus' , help='Copy to (True) or from (False) lxplus', required=True)
p.add_argument('--directory', help='The ntuple directory', default="lfvanalysis_rootfiles/", required=False)
p.add_argument('--lpcuser'  , help='LPC user EOS space to use', default="", required=False)
p.add_argument('--mc_data'  , help='Type MC or Data for only MC or Data', default="", required=False)
p.add_argument('--year'     , help='Specific year to process',default="", required=False)
p.add_argument('--tag'      , help='Dataset tag to process',default="", required=False)
p.add_argument('--veto'     , help='Comma separated list of tags to not process (e.g. DY,ttbar,Embed)',default="", required=False)
p.add_argument('--dryrun'   , help='Setup merging without running', action='store_true', required=False)
p.add_argument('--dosingle' , help='Merge first dataset only', action='store_true', required=False)
p.add_argument('--segments' , help='Only copy segment directories', action='store_true', required=False)
p.add_argument('--verbose'  , help='Print additional information', action='store_true', required=False)

args = p.parse_args()

tolxplus   = args.tolxplus
directory  = args.directory
lpcuser    = args.lpcuser
mc_data    = args.mc_data
year       = args.year
tag        = args.tag
veto       = args.veto.split(',')
dryrun     = args.dryrun
dosingle   = args.dosingle
segments   = args.segments
verbose    = args.verbose

if tolxplus not in ["True", "False"]:
    print "Unrecognized tolxplus option:", tolxplus, ", use True or False"
    exit()
tolxplus = True if tolxplus == "True" else False

if directory[-1] != "/": directory = directory + '/'

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
    if year not in ["2016", "2017", "2018"]:
        print "Unrecognized year:", year
        exit()
    print "Processing only year tag", year

user = os.environ.get('USER')
hostname = os.environ.get('HOSTNAME')
host = 'lxplus' if 'lxplus' in hostname else 'lpc'

if lpcuser == "": lpcuser = user
if tolxplus:
    inputpath  = 'root://cmseos.fnal.gov//store/user/%s/%s' % (lpcuser, directory)
    outputpath = 'root://eoscms.cern.ch//store/group/phys_smp/ZLFV/%s' % (directory)
else:
    inputpath  = 'root://eoscms.cern.ch//store/group/phys_smp/ZLFV/%s' % (directory)
    outputpath = 'root://cmseos.fnal.gov//store/user/%s/%s' % (lpcuser, directory)

print "Using input path %s and output path %s" % (inputpath, outputpath)

#Make the directory in case it doesn't exist
if not dryrun:
    os.system('eos %s mkdir -p %s' % (outputpath[:outputpath.index('/store')], outputpath[outputpath.index('/store'):]))

command = 'eos %s ls %s' % (inputpath[:inputpath.index('/store')], inputpath[inputpath.index('/store'):])
if verbose:
    print "Running command", command
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
stdout, stderr = process.communicate()
list_dirs = stdout.split('\n')

list_processed = []

#process each input dataset
for dirname in list_dirs:
    if verbose:
        print "Found entry", dirname
    if dirname == "":
        continue
    if segments and '.root' in dirname:
        continue

    #determine if the file is data or embedding for special processing (e.g. lumi files)
    isData = "SingleElectron" in dirname or "SingleMuon" in dirname
    isEmbed = "Embed-" in dirname

    #skip datasets not being considered in the processing
    if (doDataMC < 0 and isData) or (doDataMC > 0 and not isData):
        continue
    if year != "" and year not in dirname:
        continue
    if tag != "" and tag not in dirname:
        continue
    skip_dataset = False
    for veto_tag in veto:
        if veto_tag != "" and veto_tag in dirname:
            skip_dataset = True
            break
    if skip_dataset:
        continue

    #accept the dataset to process
    list_processed.append(dirname)
    print "Processing entry", dirname

    isdirectory = False if '.' in dirname else True

    #clean out the previous directory if needed
    if not dryrun and isdirectory:
        clean_command = 'eos %s rm -r %s%s'  % (outputpath[:outputpath.index('/store')], outputpath[outputpath.index('/store'):], dirname)
        print clean_command
        os.system(clean_command)

    # Copy the data
    copy_command = 'time xrdcp -fr %s%s %s' % (inputpath, dirname, outputpath)
    print copy_command
    if not dryrun:
        os.system(copy_command)

    if dosingle:
        break

print "All done!"
