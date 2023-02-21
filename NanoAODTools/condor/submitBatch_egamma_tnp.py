#! /usr/bin/env python
import PhysicsTools.NanoAODTools.condor.BatchMaster as bm

import os, sys

dryRun = False

# -----------------------------
# Specify parameters
# -----------------------------

executable = 'execBatch_egamma_tnp.sh'
analyzer   = 'EGammaTnPAnalyzer'
stage_dir  = 'batch'
output_dir = '/store/user/mimacken/egamma_tnp'
location   = 'lpc'



# -----------------------------
# Set job configurations.  
# -----------------------------
samplesDict = {}



nEvtPerJob = 5 # faster jobs, # in unit of 1e6 , 5-10 are good settings. 

#################################################
#                                               #
#---------------  Running data   ---------------#
#                                               #
#################################################
# dataset, nEvtPerJobIn1e6, year, isData, suffix


# Single Electron
samplesDict['2016_SingleElectron'] = [ 
    bm.JobConfig( '/SingleElectron/Run2016B-02Apr2020_ver2-v1/NANOAOD', nEvtPerJob, "2016", True, 'EGammaTnPAnalysis_SingleElectronRun2016B_2016'),
    bm.JobConfig( '/SingleElectron/Run2016C-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'EGammaTnPAnalysis_SingleElectronRun2016C_2016'),
    bm.JobConfig( '/SingleElectron/Run2016D-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'EGammaTnPAnalysis_SingleElectronRun2016D_2016'),
    bm.JobConfig( '/SingleElectron/Run2016E-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'EGammaTnPAnalysis_SingleElectronRun2016E_2016'),
    bm.JobConfig( '/SingleElectron/Run2016F-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'EGammaTnPAnalysis_SingleElectronRun2016F_2016'),
    bm.JobConfig( '/SingleElectron/Run2016G-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'EGammaTnPAnalysis_SingleElectronRun2016G_2016'),
    bm.JobConfig( '/SingleElectron/Run2016H-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'EGammaTnPAnalysis_SingleElectronRun2016H_2016')]

samplesDict['2017_SingleElectron'] = [ 
    bm.JobConfig( '/SingleElectron/Run2017B-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'EGammaTnPAnalysis_SingleElectronRun2017B_2017'),
    bm.JobConfig( '/SingleElectron/Run2017C-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'EGammaTnPAnalysis_SingleElectronRun2017C_2017'),
    bm.JobConfig( '/SingleElectron/Run2017D-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'EGammaTnPAnalysis_SingleElectronRun2017D_2017'),
    bm.JobConfig( '/SingleElectron/Run2017E-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'EGammaTnPAnalysis_SingleElectronRun2017E_2017'),
    bm.JobConfig( '/SingleElectron/Run2017F-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'EGammaTnPAnalysis_SingleElectronRun2017F_2017')]

samplesDict['2018_SingleElectron'] = [
    bm.JobConfig( '/EGamma/Run2018A-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'EGammaTnPAnalysis_SingleElectronRun2018A_2018'),
    bm.JobConfig( '/EGamma/Run2018B-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'EGammaTnPAnalysis_SingleElectronRun2018B_2018'),
    bm.JobConfig( '/EGamma/Run2018C-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'EGammaTnPAnalysis_SingleElectronRun2018C_2018'),
    bm.JobConfig( '/EGamma/Run2018D-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'EGammaTnPAnalysis_SingleElectronRun2018D_2018')]

### redefine N(events/job) for MC ###
nEvtPerJob = 3

#################################################
#                                               #
#--------------- Running 2016 MC ---------------#
#                                               #
#################################################


# z
samplesDict['2016_z'] = [
    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='EGammaTnPAnalysis_DY50-amcnlo_2016'),

    # bm.JobConfig(
    #     dataset='/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM',
    #     nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='EGammaTnPAnalysis_DY50-madgraph_2016'),    
]

#################################################
#                                               #
#--------------- Running 2017 MC ---------------#
#                                               #
#################################################

# z
samplesDict['2017_z'] = [
    # bm.JobConfig(
    #     dataset='/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
    #     nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='EGammaTnPAnalysis_DY50-amcnlo_2017'), #smaller sample, ignore for now

    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext3-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='EGammaTnPAnalysis_DY50-amcnlo_2017'),    
]


#################################################
#                                               #
#--------------- Running 2018 MC ---------------#
#                                               #
#################################################


# z
samplesDict['2018_z'] = [
    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext2-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='EGammaTnPAnalysis_DY50-amcnlo_2018'),

    # bm.JobConfig(
    #     dataset='/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
    #     nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='EGammaTnPAnalysis_DY50-madgraph_2018'),
]


# -----------------------------
# submit to batch
# -----------------------------
samplesToSubmit = samplesDict.keys()
samplesToSubmit.sort()
# doYears = ["2016", "2018"]
doYears = ["2016", "2017", "2018"]
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

batchMaster.submit_to_batch(doSubmit=(not dryRun))
