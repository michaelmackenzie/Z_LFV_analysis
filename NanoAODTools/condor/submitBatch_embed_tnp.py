#! /usr/bin/env python
import PhysicsTools.NanoAODTools.condor.BatchMaster as bm
from sample_map import *

import os, sys

dryRun = False

# -----------------------------
# Specify parameters
# -----------------------------

executable = 'execBatch_embed_tnp.sh'
analyzer   = 'EmbedTnPAnalyzer'
stage_dir  = 'batch'
output_dir = '/store/user/mimacken/embed_tnp'
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
#---------------  Running data   ---------------#
#                                               #
#################################################
# dataset, nEvtPerJobIn1e6, year, isData, suffix


# Single Electron
samplesDict['2016_SingleElectron'] = [ 
    bm.JobConfig( '/SingleElectron/Run2016B-02Apr2020_ver2-v1/NANOAOD', nEvtPerJob, "2016", True, 'EmbedTnPAnalysis_SingleElectronRun2016B_2016'),
    bm.JobConfig( '/SingleElectron/Run2016C-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'EmbedTnPAnalysis_SingleElectronRun2016C_2016'),
    bm.JobConfig( '/SingleElectron/Run2016D-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'EmbedTnPAnalysis_SingleElectronRun2016D_2016'),
    bm.JobConfig( '/SingleElectron/Run2016E-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'EmbedTnPAnalysis_SingleElectronRun2016E_2016'),
    bm.JobConfig( '/SingleElectron/Run2016F-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'EmbedTnPAnalysis_SingleElectronRun2016F_2016'),
    bm.JobConfig( '/SingleElectron/Run2016G-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'EmbedTnPAnalysis_SingleElectronRun2016G_2016'),
    bm.JobConfig( '/SingleElectron/Run2016H-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'EmbedTnPAnalysis_SingleElectronRun2016H_2016')
]

samplesDict['2017_SingleElectron'] = [ 
    bm.JobConfig( '/SingleElectron/Run2017B-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'EmbedTnPAnalysis_SingleElectronRun2017B_2017'),
    bm.JobConfig( '/SingleElectron/Run2017C-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'EmbedTnPAnalysis_SingleElectronRun2017C_2017'),
    bm.JobConfig( '/SingleElectron/Run2017D-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'EmbedTnPAnalysis_SingleElectronRun2017D_2017'),
    bm.JobConfig( '/SingleElectron/Run2017E-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'EmbedTnPAnalysis_SingleElectronRun2017E_2017'),
    bm.JobConfig( '/SingleElectron/Run2017F-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'EmbedTnPAnalysis_SingleElectronRun2017F_2017')
]

samplesDict['2018_SingleElectron'] = [
    bm.JobConfig( '/EGamma/Run2018A-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'EmbedTnPAnalysis_SingleElectronRun2018A_2018'),
    bm.JobConfig( '/EGamma/Run2018B-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'EmbedTnPAnalysis_SingleElectronRun2018B_2018'),
    bm.JobConfig( '/EGamma/Run2018C-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'EmbedTnPAnalysis_SingleElectronRun2018C_2018'),
    bm.JobConfig( '/EGamma/Run2018D-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'EmbedTnPAnalysis_SingleElectronRun2018D_2018')
]

# Single Muon
samplesDict['2016_SingleMuon'] = [ 
    bm.JobConfig( '/SingleMuon/Run2016B-02Apr2020_ver2-v1/NANOAOD', nEvtPerJob, "2016", True, 'EmbedTnPAnalysis_SingleMuonRun2016B_2016'),
    bm.JobConfig( '/SingleMuon/Run2016C-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'EmbedTnPAnalysis_SingleMuonRun2016C_2016'),
    bm.JobConfig( '/SingleMuon/Run2016D-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'EmbedTnPAnalysis_SingleMuonRun2016D_2016'),
    bm.JobConfig( '/SingleMuon/Run2016E-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'EmbedTnPAnalysis_SingleMuonRun2016E_2016'),
    bm.JobConfig( '/SingleMuon/Run2016F-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'EmbedTnPAnalysis_SingleMuonRun2016F_2016'),
    bm.JobConfig( '/SingleMuon/Run2016G-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'EmbedTnPAnalysis_SingleMuonRun2016G_2016'),
    bm.JobConfig( '/SingleMuon/Run2016H-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'EmbedTnPAnalysis_SingleMuonRun2016H_2016')
]

samplesDict['2017_SingleMuon'] = [ 
    bm.JobConfig( '/SingleMuon/Run2017B-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'EmbedTnPAnalysis_SingleMuonRun2017B_2017'),
    bm.JobConfig( '/SingleMuon/Run2017C-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'EmbedTnPAnalysis_SingleMuonRun2017C_2017'),
    bm.JobConfig( '/SingleMuon/Run2017D-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'EmbedTnPAnalysis_SingleMuonRun2017D_2017'),
    bm.JobConfig( '/SingleMuon/Run2017E-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'EmbedTnPAnalysis_SingleMuonRun2017E_2017'),
    bm.JobConfig( '/SingleMuon/Run2017F-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'EmbedTnPAnalysis_SingleMuonRun2017F_2017')
]

samplesDict['2018_SingleMuon'] = [
    bm.JobConfig( '/SingleMuon/Run2018A-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'EmbedTnPAnalysis_SingleMuonRun2018A_2018'),
    bm.JobConfig( '/SingleMuon/Run2018B-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'EmbedTnPAnalysis_SingleMuonRun2018B_2018'),
    bm.JobConfig( '/SingleMuon/Run2018C-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'EmbedTnPAnalysis_SingleMuonRun2018C_2018'),
    bm.JobConfig( '/SingleMuon/Run2018D-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'EmbedTnPAnalysis_SingleMuonRun2018D_2018')
]

#################################################
#                                               #
#---------- Running Embedded Samples -----------#
#                                               #
#################################################

### redefine N(events/job) for embedding ###
nEvtPerJob = 0.5 #~25k events per file, ~50-100 files per dataset --> ~5-10 jobs/dataset

for dataset in sampleMap._data.keys():
    if 'embed_ee' in dataset or 'embed_mumu' in dataset:
        samplesDict[dataset] = []
        for sample in sampleMap._data[dataset]:
            samplesDict[dataset].append(bm.JobConfig(dataset = sample._path, nEvtPerJobIn1e6 = nEvtPerJob, year = sample._year,
                                                     isData = sample._isdata, suffix = 'EmbedTnPAnalysis_%s_%i' % (sample._name, sample._year),
                                                     inputDBS = sample._inputDBS))


#################################################
#                                               #
#------------- Running MC Samples --------------#
#                                               #
#################################################

### redefine N(events/job) for MC ###
nEvtPerJob = 3

samplesDict['2016_z'] = [
    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='EmbedTnPAnalysis_DY50_2016'),
]
samplesDict['2017_z'] = [
    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext3-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='EmbedTnPAnalysis_DY50_2017'),    
]
samplesDict['2018_z'] = [
    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext2-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='EmbedTnPAnalysis_DY50_2018'),
]

# UL samples
samplesDict['2018_ul_z'] = [
    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM',
        nEvtPerJobIn1e6=1, maxEvtPerDataset = 5e7, year="2018", isData=False, suffix='EmbedTnPAnalysis_ULDY50_2018'),
]


# -----------------------------
# submit to batch
# -----------------------------

samplesToSubmit = samplesDict.keys()
# samplesToSubmit = ["2018_embed_ee", "2018_embed_mumu"]
samplesToSubmit.sort()

# doYears = ["2016", "2017", "2018"]
doYears = ["2018"]
tags = ["ul_z"]
vetoes = []
configs = []

for s in samplesToSubmit:
    if s[:4] in doYears:
        tagged = True if len(tags) == 0 else False
        for tag in tags: tagged = tagged or tag in s
        if not tagged: continue
        vetoed = False
        for veto in vetoes: vetoed = vetoed or veto in s
        if vetoed: continue
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
