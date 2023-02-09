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

    
    
#---------------------------------#
p = argparse.ArgumentParser(description='Retrieve data and embedded sample json files from DAS')
p.add_argument('--year'     , help='Specific year to process',default=None, required=False)
p.add_argument('--tag'      , help='Dataset tag list to process',default="", required=False)
p.add_argument('--veto'     , help='Comma separated list of tags to not process (e.g. SingleMuon,Embed-MuMu)',default="", required=False)
p.add_argument('--dryrun'   , help='Setup processing without running', action='store_true', required=False)
p.add_argument('--dosingle' , help='Process first dataset only', action='store_true', required=False)
p.add_argument('--verbose'  , help='Print additional information', action='store_true', required=False)

args = p.parse_args()

year_tag   = args.year
tag        = args.tag.split(',')
veto       = args.veto.split(',')
dryrun     = args.dryrun
dosingle   = args.dosingle
verbose    = args.verbose

samples = SampleMap()
samples.load_samples(samples._data, include_mini = True)


#---------------------------------#

user = os.environ.get('USER')
hostname = os.environ.get('HOSTNAME')
host = 'lxplus' if 'lxplus' in hostname else 'lpc'


for super_name in samples._data.keys():
    for dataset in samples._data[super_name]:
        year = dataset._year
        name = dataset._name

        tagged = False if len(tag) > 0 else True
        for tag_i in tag:
            if tag_i in name or tag_i == "":
                tagged = True
        if not tagged:
            continue
        skip_dataset = False
        for veto_tag in veto:
            if veto_tag != "" and veto_tag in name:
                skip_dataset = True
                break
        if skip_dataset:
            continue

        if year_tag is not None and year_tag != '%i' % (year):
            continue

        print "Processing dataset", name

        base_out = "json/%s_%i_json" % (dataset._name, year)
        query = 'dasgoclient -query="run,lumi dataset=%s instance=prod/%s" -format json >| %s_raw.txt' % (dataset._path, dataset._inputDBS, base_out)
        if verbose:
            print "DAS query:", query        
        if not dryrun:
            cmdline(query)

        if year == 2016:
            json="../json/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt"
        elif year == 2017:
            json="../json/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt"
        else:
            json="../json/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt"
        if verbose:
            print "Using json mask %s" % (json)

        command = "python ../scripts/configure_json.py --input %s_raw.txt --output %s.txt --mask %s" % (base_out, base_out, json)
        if verbose:
            print "Configure: %s" % (command)
        if not dryrun:
            cmdline(command)


        if dosingle:
            exit()
