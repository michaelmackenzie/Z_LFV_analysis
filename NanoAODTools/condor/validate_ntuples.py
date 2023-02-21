import ROOT
import os, sys
import shutil
import subprocess
import argparse
from importlib import import_module
from subprocess import PIPE, Popen

from sample_map import *

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

ROOT.PyConfig.IgnoreCommandLineOptions = True


def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]

def check_selection(file, selection):
    if not file.GetListOfKeys().Contains("events_selection"):
        return True
    h = file.Get("event_selection")
    if not file.GetListOfKeys().Contains(selection):
        return True
    tree = file.Get(selection)
    nevents = tree.GetEntries()
    if   selection == 'emu'  : bin = 2
    elif selection == 'etau' : bin = 3
    elif selection == 'mutau': bin = 4
    elif selection == 'ee'   : bin = 5
    elif selection == 'mumu' : bin = 6
    else: return 0
    nhist = h.GetBinContent(bin)
    if nhist != nevents:
        print "--> Error! Selection %5s has %10i ntuple events and %10i filter events (difference = %i)" % (selection, nevents, nhist, nevents-nhist)
        return False
    return True
    
    
#---------------------------------#
p = argparse.ArgumentParser(description='Select whether to download MC or data')
p.add_argument('--year'     , help='Specific year to process',default=None, required=False)
p.add_argument('--tag'      , help='Dataset tag list to process',default="", required=False)
p.add_argument('--veto'     , help='Comma separated list of tags to not process (e.g. DY,ttbar,Embed)',default="", required=False)
p.add_argument('--dryrun'   , help='Setup merging without running', action='store_true', required=False)
p.add_argument('--dosingle' , help='Merge first dataset only', action='store_true', required=False)
p.add_argument('--usedirect', help='Use the direct EOS path instead of XROOTD', action='store_true', required=False)
p.add_argument('--segments' , help='Use job segments rather than a merged ntuple', action='store_true', required=False)
p.add_argument('--verbose'  , help='Print additional information', action='store_true', required=False)

args = p.parse_args()

year_tag   = args.year
tag        = args.tag.split(',')
veto       = args.veto.split(',')
dryrun     = args.dryrun
dosingle   = args.dosingle
usedirect  = args.usedirect
segments   = args.segments
verbose    = args.verbose

samples = SampleMap()
samples.load_samples(samples._data)


#---------------------------------#

user = os.environ.get('USER')
hostname = os.environ.get('HOSTNAME')
host = 'lxplus' if 'lxplus' in hostname else 'lpc'

#Get the list of files in the ntuple directory
if usedirect:
    if host == 'lxplus':
        eospath = '/eos/cms/store/group/phys_smp/ZLFV/lfvanalysis_rootfiles/'
    else:
        eospath = '/eos/uscms/store/user/%s/lfvanalysis_rootfiles/' % (user)
else:
    if host == 'lxplus':
        eospath = 'root://eoscms.cern.ch//store/group/phys_smp/ZLFV/lfvanalysis_rootfiles/'
    else:
        eospath = 'root://cmseos.fnal.gov//store/user/%s/lfvanalysis_rootfiles/' % (user)

if host == 'lxplus':
    command = 'eos root://eoscms.cern.ch ls /store/group/phys_smp/ZLFV/lfvanalysis_rootfiles/'
else:
    command = 'eos root://cmseos.fnal.gov ls /store/user/%s/lfvanalysis_rootfiles/' % (user)

if verbose:
    print "Running command", command
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
stdout, stderr = process.communicate()
list_samples = stdout.split('\n')

for sample in list_samples:
    if not '.root' in sample:
        continue

    tagged = False if len(tag) > 0 else True
    for tag_i in tag:
        if tag_i in sample or tag_i == "":
            tagged = True
    if not tagged:
        continue
    skip_dataset = False
    for veto_tag in veto:
        if veto_tag != "" and veto_tag in sample:
            skip_dataset = True
            break
    if skip_dataset:
        continue

    root_name = sample[sample.find('_')+1:sample.rfind('_')]
    year = int(sample[sample.rfind('_')+1:sample.find('.root')])

    if year_tag is not None and year_tag != '%i' % (year):
        continue

    if verbose:
        print "Found file", sample
        print " Sample name:", root_name, "year:", year

    sample_info = None
    for key in samples._data:
        for info in samples._data[key]:
            if info._name == root_name and year == info._year:
                sample_info = info
                break
        if sample_info is not None:
            break
    if sample_info is None or sample_info._path == '':
        # print "Sample %s not found!\n" % (sample)
        continue
        
    # file = ROOT.TFile(eospath + sample, 'READ')
    file = ROOT.TFile.Open(eospath + sample, 'READ')
    if file is None:
        continue
    if verbose:
        print "Retrieved file", sample
    Norm = file.Get('Norm')
    nevents = 0
    for entry in Norm:
        nevents = nevents + entry.NEvents
    file.Close()
    if verbose:
        print "Dataset %s has %i entries" % (sample, nevents)

    query = 'das_client -query="dataset=%s instance=prod/%s | grep dataset.nevents"' % (sample_info._path, sample_info._inputDBS)
    if verbose:
        print "DAS query:", query
    ndas = int(cmdline(query).strip())
    print "Dataset %30s for %i has %10i DAS entries, %10i tree entries (difference = %i)" % (root_name, year, ndas, nevents, ndas-nevents)
    if ndas > nevents:
        print "--> Error! Sample file %s is missing %i events!" % (sample, ndas-nevents)

    for selection in ['emu', 'etau', 'mutau', 'ee', 'mumu']:
        if check_selection(file, selection) and verbose:
            print "--> Passed %5s selection check" % (selection)
        
            

    if dosingle:
        exit()
