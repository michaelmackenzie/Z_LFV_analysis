#! /usr/bin/env python
import PhysicsTools.NanoAODTools.condor.BatchMaster as bm
from sample_map import *

import os, sys

dryRun = False

# -----------------------------
# Specify parameters
# -----------------------------

executable = 'execBatch_emu_study.sh'
analyzer   = 'EmbeddingEMuAnalyzer'
stage_dir  = 'batch'
output_dir = '/store/user/mimacken/emu_study'
location   = 'lpc'



# -----------------------------
# Set job configurations.  
# -----------------------------
samplesDict = {}

#Load currently used samples
sampleMap = SampleMap()
sampleMap.load_samples(sampleMap._data)

nEvtPerJob = 8 # faster jobs, # in unit of 1e6 , 5-10 are good settings. 


#################################################
#                                               #
#---------- Running Embedded Samples -----------#
#                                               #
#################################################

### redefine N(events/job) for embedding ###
nEvtPerJob = 0.5 #~25k events per file, ~50-100 files per dataset --> ~5-10 jobs/dataset

for dataset in sampleMap._data.keys():
    if 'embed_emu' in dataset:
        samplesDict[dataset] = []
        for sample in sampleMap._data[dataset]:
            samplesDict[dataset].append(bm.JobConfig(dataset = sample._path, nEvtPerJobIn1e6 = nEvtPerJob, year = sample._year,
                                                     isData = sample._isdata, suffix = 'EMuStudy_%s_%i' % (sample._name, sample._year),
                                                     inputDBS = sample._inputDBS))

#################################################
#                                               #
#------------- Running MC Samples --------------#
#                                               #
#################################################

### redefine N(events/job) for MC ###
nEvtPerJob = 5

samplesDict['2016_z'] = [
    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='EMuStudy_DY50_2016'),
]
samplesDict['2017_z'] = [
    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext3-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='EMuStudy_DY50_2017'),    
]
samplesDict['2018_z'] = [
    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext2-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='EMuStudy_DY50_2018'),
]

# -----------------------------
# submit to batch
# -----------------------------

samplesToSubmit = samplesDict.keys()
samplesToSubmit.sort()
# samplesToSubmit = ["2018_embed_emu"]

doYears = ["2016", "2017", "2018"]
# doYears = ["2018"]
configs = []

for s in samplesToSubmit:
    if s[:4] in doYears:
        configs += samplesDict[s]

batchMaster = bm.BatchMaster(
    analyzer    = analyzer,
    config_list = configs, 
    stage_dir   = stage_dir,
    output_dir  = output_dir,
    executable  = executable,
    location    = location
)

#ensure there's a symbolic link 'batch' to put the tarball in
if not os.path.exists("batch") :
    if not os.path.exists("~/nobackup/batch") :
        os.makedirs("~/nobackup/batch")
    os.symlink("~/nobackup/batch", "batch")
    print "Created symbolic link to ~/nobackup/batch"

if configs == []:
    print "No jobs to submit!\n"
else :
    batchMaster.submit_to_batch(doSubmit=(not dryRun))
