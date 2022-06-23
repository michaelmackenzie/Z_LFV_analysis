#! /usr/bin/env python
import PhysicsTools.NanoAODTools.condor.BatchMaster as bm

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



nEvtPerJob = 5 # faster jobs, # in unit of 1e6 , 5-10 are good settings. 

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
nEvtPerJob = 1 #~25k events per file, ~50-100 files per dataset --> ~5-10 jobs/dataset

# 2016 Embedded samples
samplesDict['2016_embed_ee'] = [
    bm.JobConfig(
        dataset='/EmbeddingRun2016B/pellicci-EmbeddedElEl_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='EmbedTnPAnalysis_Embed-EE-B_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016C/pellicci-EmbeddedElEl_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='EmbedTnPAnalysis_Embed-EE-C_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016D/pellicci-EmbeddedElEl_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='EmbedTnPAnalysis_Embed-EE-D_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016E/pellicci-EmbeddedElEl_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='EmbedTnPAnalysis_Embed-EE-E_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016F/pellicci-EmbeddedElEl_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='EmbedTnPAnalysis_Embed-EE-F_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016G/pellicci-EmbeddedElEl_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='EmbedTnPAnalysis_Embed-EE-G_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016H/pellicci-EmbeddedElEl_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='EmbedTnPAnalysis_Embed-EE-H_2016', inputDBS="phys03"),
]

samplesDict['2016_embed_mumu'] = [
    bm.JobConfig(
        dataset='/EmbeddingRun2016B/pellicci-EmbeddedMuMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='EmbedTnPAnalysis_Embed-MuMu-B_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016C/pellicci-EmbeddedMuMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='EmbedTnPAnalysis_Embed-MuMu-C_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016D/pellicci-EmbeddedMuMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='EmbedTnPAnalysis_Embed-MuMu-D_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016E/pellicci-EmbeddedMuMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='EmbedTnPAnalysis_Embed-MuMu-E_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016F/pellicci-EmbeddedMuMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='EmbedTnPAnalysis_Embed-MuMu-F_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016G/pellicci-EmbeddedMuMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='EmbedTnPAnalysis_Embed-MuMu-G_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016H/pellicci-EmbeddedMuMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='EmbedTnPAnalysis_Embed-MuMu-H_2016', inputDBS="phys03"),
]

# 2017 Embedded samples
samplesDict['2017_embed_ee'] = [
    bm.JobConfig(
        dataset='/EmbeddingRun2017B/pellicci-EmbeddedElEl_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='EmbedTnPAnalysis_Embed-EE-B_2017', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2017C/pellicci-EmbeddedElEl_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='EmbedTnPAnalysis_Embed-EE-C_2017', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2017D/pellicci-EmbeddedElEl_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='EmbedTnPAnalysis_Embed-EE-D_2017', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2017E/pellicci-EmbeddedElEl_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='EmbedTnPAnalysis_Embed-EE-E_2017', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2017F/pellicci-EmbeddedElEl_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='EmbedTnPAnalysis_Embed-EE-F_2017', inputDBS="phys03"),
]

samplesDict['2017_embed_mumu'] = [
    bm.JobConfig(
        dataset='/EmbeddingRun2017B/pellicci-EmbeddedMuMu_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='EmbedTnPAnalysis_Embed-MuMu-B_2017', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2017C/pellicci-EmbeddedMuMu_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='EmbedTnPAnalysis_Embed-MuMu-C_2017', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2017D/pellicci-EmbeddedMuMu_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='EmbedTnPAnalysis_Embed-MuMu-D_2017', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2017E/pellicci-EmbeddedMuMu_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='EmbedTnPAnalysis_Embed-MuMu-E_2017', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2017F/pellicci-EmbeddedMuMu_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='EmbedTnPAnalysis_Embed-MuMu-F_2017', inputDBS="phys03"),
]

# 2018 Embedded samples
samplesDict['2018_embed_ee'] = [
    bm.JobConfig(
        dataset='/EmbeddingRun2018A/pellicci-EmbeddedElEl_NANOAOD_2018_10222V1-9b11f648cb233dc346c2d0860bbea8f9/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='EmbedTnPAnalysis_Embed-EE-A_2018', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2018B/pellicci-EmbeddedElEl_NANOAOD_2018_10222V1-9b11f648cb233dc346c2d0860bbea8f9/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='EmbedTnPAnalysis_Embed-EE-B_2018', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2018C/pellicci-EmbeddedElEl_NANOAOD_2018_10222V1-9b11f648cb233dc346c2d0860bbea8f9/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='EmbedTnPAnalysis_Embed-EE-C_2018', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2018D/pellicci-EmbeddedElEl_NANOAOD_2018_10222V1-e181eeebc101019f884cba30e429f851/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='EmbedTnPAnalysis_Embed-EE-D_2018', inputDBS="phys03"),
]

samplesDict['2018_embed_mumu'] = [
    bm.JobConfig(
        dataset='/EmbeddingRun2018A/pellicci-EmbeddedMuMu_NANOAOD_2018_10222V1-9b11f648cb233dc346c2d0860bbea8f9/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='EmbedTnPAnalysis_Embed-MuMu-A_2018', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2018B/pellicci-EmbeddedMuMu_NANOAOD_2018_10222V1-9b11f648cb233dc346c2d0860bbea8f9/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='EmbedTnPAnalysis_Embed-MuMu-B_2018', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2018C/pellicci-EmbeddedMuMu_NANOAOD_2018_10222V1-9b11f648cb233dc346c2d0860bbea8f9/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='EmbedTnPAnalysis_Embed-MuMu-C_2018', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2018D/pellicci-EmbeddedMuMu_NANOAOD_2018_10222V1-e181eeebc101019f884cba30e429f851/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='EmbedTnPAnalysis_Embed-MuMu-D_2018', inputDBS="phys03"),
]


# -----------------------------
# submit to batch
# -----------------------------

samplesToSubmit = samplesDict.keys()
samplesToSubmit.sort()
# samplesToSubmit = ["2018_embed_ee", "2018_embed_mumu"]

doYears = ["2016", "2017", "2018"]
# doYears = ["2017", "2018"]
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
