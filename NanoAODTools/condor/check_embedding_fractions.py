#! /usr/bin/env python
from sample_map import *
import os, sys
import shutil
import subprocess
import argparse
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
p.add_argument('--verbose'  , help='Verbose level',default=0, required=False)

args = p.parse_args()

year_tag   = args.year
tags       = args.tag.split(',')
vetos      = args.veto.split(',')
verbose    = args.verbose

#Load currently used samples
sampleMap = SampleMap()
sampleMap.load_samples(sampleMap._data)

for dataset in sampleMap._data.keys():
    if 'embed' not in dataset: continue
    if year_tag != "" and year_tag not in dataset: continue
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

    
