#! /usr/bin/env python
from sample_map import *
import os, sys
import shutil
import subprocess
import argparse
import ROOT
from importlib import import_module
from subprocess import PIPE, Popen

def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]

#---------------------------------------------------------------------------------------------

p = argparse.ArgumentParser(description='Check event counts in MINI vs NANO Embedded samples')
p.add_argument('--year'     , help='Specific year to process',default=None, required=False)
p.add_argument('--tag'      , help='Dataset tag list to process',default="", required=False)
p.add_argument('--veto'     , help='Comma separated list of tags to not process (e.g. EMu,ETau)',default="", required=False)
p.add_argument('--usecount' , help='Get MINIAOD count information from eos skimming', action='store_true', required=False)
p.add_argument('--verbose'  , help='Verbose level',default=0, required=False)

args = p.parse_args()

year_tag   = args.year
tags       = args.tag.split(',')
vetos      = args.veto.split(',')
usecount   = args.usecount
verbose    = int(args.verbose)

if verbose > 0: print "Running with verbosity level %i" % verbose


user = os.environ.get('USER')
hostname = os.environ.get('HOSTNAME')
host = 'lxplus' if 'lxplus' in hostname else 'lpc'


if host == 'lxplus':
    path = 'root://eoscms.cern.ch//store/group/phys_smp/ZLFV/lumi_count/files/'
else:
    path = 'root://cmseos.fnal.gov//store/user/%s/lumi_count/files/' % (user)

#Load currently used samples
sampleMap = SampleMap()
sampleMap.load_samples(sampleMap._data)

for dataset in sampleMap._data.keys():
    if 'embed' not in dataset: continue
    if year_tag is not None and year_tag not in dataset: continue
    if verbose > 0: print 'Checking datasets under: %s' % (dataset)
    for sample in sampleMap._data[dataset]:
        tagged = False
        for tag in tags:
            tagged = tag == '' or tag in sample._name
        if not tagged: continue
        if verbose > 0: print 'Checking dataset: %i %s' % (sample._year, sample._name)

        name = sample._name
        year = sample._year
        run = name[-1]
        final_state = 'MuTau'
        if 'ETau' in name: final_state = 'ElTau'
        elif 'EMu' in name: final_state = 'ElMu'
        elif 'EE' in name: final_state = 'ElEl'
        elif 'MuMu' in name: final_state = 'MuMu'

        ################################################################
        #Get the MINIAOD dataset info

        if not usecount: #Query DAS
            mini_tag = '/EmbeddingRun%i%s/' % (year, run)
            if final_state == 'ElEl':
                mini_tag = mini_tag + 'ElectronEmbedding*/USER'
            elif final_state == 'MuMu':
                mini_tag = mini_tag + 'MuonEmbedding*/USER'
            else:
                if sample._year == 2016:
                    mini_tag = mini_tag + '%sFinalState-inputDoubleMu_94X_Legacy_miniAOD-v5*/USER' % (final_state)
                elif sample._year == 2017:
                    mini_tag = mini_tag + '%sFinalState-inputDoubleMu_94X*/USER' % (final_state)
                elif sample._year == 2018:
                    mini_tag = mini_tag + '%sFinalState-inputDoubleMu_102X*/USER' % (final_state)
        
            query = 'das_client -query="dataset=%s instance=prod/phys03" 2>/dev/null | tail -n 1' % (mini_tag)
            if verbose > 1: print ' ' + query
            file = cmdline(query).strip()
            if verbose > 1: print ' ' + file
            query = 'das_client -query="dataset=%s instance=prod/phys03 | grep dataset.nevents"' % (file)
            result = cmdline(query).strip()
            if verbose > 1: print ' ' + result
            nmini = int(result)
            if verbose > 0: print "MINI dataset %15s for %i has %10i DAS entries" % (sample._name, sample._year, nmini)
        else: #Read lumi skimming info
            file_path = ('LumiCount_%s_%i.root' % (sample._name, sample._year))
            file_path = file_path.replace("Embed-", "Embed-MINI-")
            file_path = path + file_path
            f = ROOT.TFile.Open(file_path, "READ")
            if f is None:
                continue
            events = f.Get('events')
            ntot  = events.GetBinContent(1)
            nmini = events.GetBinContent(2)
            if verbose > 0: print "MINI dataset %15s for %i has %10i entries (%10i unmasked, %.2f%%)" % (sample._name, sample._year, nmini, ntot, (nmini*100.)/ntot)


        ################################################################
        #Get the NANOAOD dataset info

        query = 'das_client -query="dataset=%s instance=prod/%s" 2>/dev/null | tail -n 1' % (sample._path, sample._inputDBS)
        if verbose > 1: print ' ' + query
        file = cmdline(query).strip()
        if verbose > 1: print ' ' + file
        query = 'das_client -query="dataset=%s instance=prod/phys03 | grep dataset.nevents"' % (file)
        result = cmdline(query).strip()
        if verbose > 1: print ' ' + result
        nnano = int(result)
        if verbose > 0: print "NANO dataset %15s for %i has %10i DAS entries" % (sample._name, sample._year, nnano)

        print "Dataset %15s for %i MINI / NANO = %8i / %8i = %.4f" % (sample._name, sample._year, nmini, nnano, nmini/(1.*nnano))

    
