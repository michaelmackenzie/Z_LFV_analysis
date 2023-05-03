#! /usr/bin/env python
import PhysicsTools.NanoAODTools.condor.BatchMaster as bm
from sample_map import *

import os, sys

dryRun = False

# -----------------------------
# Specify parameters
# -----------------------------

user = os.getenv('USER')
host = os.getenv('HOSTNAME')

print 'Using user %s on host %s' % (user, host)

executable = 'execBatch_MINI_Count.sh'
analyzer   = 'LumiCount'
stage_dir  = 'batch'
if 'lxplus' in host: #use SMP space
    output_dir = '/store/group/phys_smp/ZLFV/lumi_count'
    # output_dir = '/eos/cms/store/group/phys_smp/ZLFV/batch'
    location   = 'lxplus'
elif user == 'mmackenz':
    output_dir = '/store/user/mimacken/lumi_count'
    location   = 'lpc'
else:
    output_dir = '/store/user/%s/lumi_count' % (user)
    location   = 'lpc'

print 'location = %s, output_dir = %s' % (location, output_dir)


# -----------------------------
# Set job configurations.  
# -----------------------------
samplesDict = {}

#Load currently used samples
sampleMap = SampleMap()
sampleMap.load_samples(sampleMap._data, True)


nEvtPerJob  = 1e6 # limit by file number, ignoring N(events)
maxFiles    = 1500

#################################################
#                                               #
#---------- Running Embedded Samples -----------#
#                                               #
#################################################

for dataset in sampleMap._data.keys():
    if 'embed' not in dataset: continue
    if 'mini' not in dataset: continue
    samplesDict[dataset] = []
    for sample in sampleMap._data[dataset]:
        samplesDict[dataset].append(bm.JobConfig(dataset = sample._path, nEvtPerJobIn1e6 = nEvtPerJob, year = sample._year,
                                                 isData = sample._isdata, suffix = 'LumiCount_%s_%i' % (sample._name, sample._year),
                                                 inputDBS = sample._inputDBS))

# -----------------------------
# submit to batch
# -----------------------------

# samplesToSubmit = samplesDict.keys()
samplesToSubmit = ["2017_embed_mini_mumu"]
samplesToSubmit.sort()
doYears = ["2017"]
# doYears = ["2016", "2017", "2018"]
sampleTag = ""
sampleVeto = ""
configs = []

for s in samplesToSubmit:
    if s[:4] in doYears and (sampleTag == "" or sampleTag in s) and (sampleVeto == "" or sampleVeto not in s):
        configs += samplesDict[s]

if configs == []:
    print "No datasets to submit!"
    exit()

batchMaster = bm.BatchMaster(
    analyzer       = analyzer,
    config_list    = configs,
    stage_dir      = stage_dir,
    output_dir     = output_dir,
    executable     = executable,
    location       = location,
    maxFilesPerJob = maxFiles
)

#ensure there's a symbolic link 'batch' to put the tarball in
if not os.path.exists("batch") :
    if 'lxplus' in host:
        if not os.path.exists("~/private/batch") :
            os.makedirs("~/private/batch")
        os.symlink("~/private/batch", "batch")
    else: #LPC
        if not os.path.exists("~/nobackup/batch") :
            os.makedirs("~/nobackup/batch")
        os.symlink("~/nobackup/batch", "batch")
    print "Created symbolic link to ~/nobackup/batch"

if not os.path.isfile('%s/batch_exclude.txt' % (os.getenv('CMSSW_BASE'))):
    os.system('cp batch_exclude.txt ${CMSSW_BASE}/')

batchMaster.submit_to_batch(doSubmit=(not dryRun))
