#! /usr/bin/env python
import PhysicsTools.NanoAODTools.condor.BatchMaster as bm

import os, sys


# -----------------------------
# Specify parameters
# -----------------------------

executable = 'execBatch.sh'
analyzer   = 'LFVAnalyzer'
stage_dir  = 'batch'
output_dir = '/store/user/mimacken/nano_batchout'
location   = 'lpc'



# -----------------------------
# Set job configurations.  
# -----------------------------
samplesDict = {}



nEvtPerJob = 3 # faster jobs, # in unit of 1e6 , 5-10 are good settings. 

#################################################
#                                               #
#---------------  Running data   ---------------#
#                                               #
#################################################
# dataset, nEvtPerJobIn1e6, year, isData, suffix


# Single Electron
samplesDict['2016_SingleElectron'] = [ 
    bm.JobConfig( '/SingleElectron/Run2016B-02Apr2020_ver2-v1/NANOAOD', nEvtPerJob, "2016", True, 'LFVAnalysis_SingleElectronRun2016B_2016'),
    bm.JobConfig( '/SingleElectron/Run2016C-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'LFVAnalysis_SingleElectronRun2016C_2016'),
    bm.JobConfig( '/SingleElectron/Run2016D-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'LFVAnalysis_SingleElectronRun2016D_2016'),
    bm.JobConfig( '/SingleElectron/Run2016E-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'LFVAnalysis_SingleElectronRun2016E_2016'),
    bm.JobConfig( '/SingleElectron/Run2016F-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'LFVAnalysis_SingleElectronRun2016F_2016'),
    bm.JobConfig( '/SingleElectron/Run2016G-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'LFVAnalysis_SingleElectronRun2016G_2016'),
    bm.JobConfig( '/SingleElectron/Run2016H-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'LFVAnalysis_SingleElectronRun2016H_2016')]

samplesDict['2017_SingleElectron'] = [ 
    bm.JobConfig( '/SingleElectron/Run2017B-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'LFVAnalysis_SingleElectronRun2017B_2017'),
    bm.JobConfig( '/SingleElectron/Run2017C-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'LFVAnalysis_SingleElectronRun2017C_2017'),
    bm.JobConfig( '/SingleElectron/Run2017D-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'LFVAnalysis_SingleElectronRun2017D_2017'),
    bm.JobConfig( '/SingleElectron/Run2017E-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'LFVAnalysis_SingleElectronRun2017E_2017'),
    bm.JobConfig( '/SingleElectron/Run2017F-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'LFVAnalysis_SingleElectronRun2017F_2017')]

samplesDict['2018_SingleElectron'] = [
    bm.JobConfig( '/EGamma/Run2018A-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'LFVAnalysis_SingleElectronRun2018A_2018'),
    bm.JobConfig( '/EGamma/Run2018B-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'LFVAnalysis_SingleElectronRun2018B_2018'),
    bm.JobConfig( '/EGamma/Run2018C-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'LFVAnalysis_SingleElectronRun2018C_2018'),
    bm.JobConfig( '/EGamma/Run2018D-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'LFVAnalysis_SingleElectronRun2018D_2018')]



# Single Muon
samplesDict['2016_SingleMuon'] = [ 
    bm.JobConfig( '/SingleMuon/Run2016B-02Apr2020_ver2-v1/NANOAOD', nEvtPerJob, "2016", True, 'LFVAnalysis_SingleMuonRun2016B_2016'),
    bm.JobConfig( '/SingleMuon/Run2016C-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'LFVAnalysis_SingleMuonRun2016C_2016'),
    bm.JobConfig( '/SingleMuon/Run2016D-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'LFVAnalysis_SingleMuonRun2016D_2016'),
    bm.JobConfig( '/SingleMuon/Run2016E-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'LFVAnalysis_SingleMuonRun2016E_2016'),
    bm.JobConfig( '/SingleMuon/Run2016F-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'LFVAnalysis_SingleMuonRun2016F_2016'),
    bm.JobConfig( '/SingleMuon/Run2016G-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'LFVAnalysis_SingleMuonRun2016G_2016'),
    bm.JobConfig( '/SingleMuon/Run2016H-02Apr2020-v1/NANOAOD'     , nEvtPerJob, "2016", True, 'LFVAnalysis_SingleMuonRun2016H_2016')]

samplesDict['2017_SingleMuon'] = [ 
    bm.JobConfig( '/SingleMuon/Run2017B-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'LFVAnalysis_SingleMuonRun2017B_2017'),
    bm.JobConfig( '/SingleMuon/Run2017C-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'LFVAnalysis_SingleMuonRun2017C_2017'),
    bm.JobConfig( '/SingleMuon/Run2017D-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'LFVAnalysis_SingleMuonRun2017D_2017'),
    bm.JobConfig( '/SingleMuon/Run2017E-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'LFVAnalysis_SingleMuonRun2017E_2017'),
    bm.JobConfig( '/SingleMuon/Run2017F-02Apr2020-v1/NANOAOD', nEvtPerJob, "2017", True, 'LFVAnalysis_SingleMuonRun2017F_2017')]

samplesDict['2018_SingleMuon'] = [
    bm.JobConfig( '/SingleMuon/Run2018A-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'LFVAnalysis_SingleMuonRun2018A_2018'),
    bm.JobConfig( '/SingleMuon/Run2018B-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'LFVAnalysis_SingleMuonRun2018B_2018'),
    bm.JobConfig( '/SingleMuon/Run2018C-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'LFVAnalysis_SingleMuonRun2018C_2018'),
    bm.JobConfig( '/SingleMuon/Run2018D-02Apr2020-v1/NANOAOD', nEvtPerJob, "2018", True, 'LFVAnalysis_SingleMuonRun2018D_2018')]





#################################################
#                                               #
#---------- Running Embedded Samples -----------#
#                                               #
#################################################

### redefine N(events/job) for embedding ###
nEvtPerJob = 1 #~25k events per file, ~50-100 files per dataset --> ~5 jobs/dataset

# 2016 Embedded samples
samplesDict['2016_embed_emu'] = [
    bm.JobConfig(
        dataset='/EmbeddingRun2016B/pellicci-EmbeddedElMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Embed-EMu-B_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016C/pellicci-EmbeddedElMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Embed-EMu-C_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016D/pellicci-EmbeddedElMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Embed-EMu-D_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016E/pellicci-EmbeddedElMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Embed-EMu-E_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016F/pellicci-EmbeddedElMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Embed-EMu-F_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016G/pellicci-EmbeddedElMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Embed-EMu-G_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016H/pellicci-EmbeddedElMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Embed-EMu-H_2016', inputDBS="phys03"),

]

samplesDict['2016_embed_etau'] = [
    bm.JobConfig(
        dataset='/EmbeddingRun2016B/pellicci-EmbeddedElTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Embed-ETau-B_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016C/pellicci-EmbeddedElTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Embed-ETau-C_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016D/pellicci-EmbeddedElTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Embed-ETau-D_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016E/pellicci-EmbeddedElTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Embed-ETau-E_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016F/pellicci-EmbeddedElTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Embed-ETau-F_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016G/pellicci-EmbeddedElTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Embed-ETau-G_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016H/pellicci-EmbeddedElTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Embed-ETau-H_2016', inputDBS="phys03"),

]

samplesDict['2016_embed_mutau'] = [
    bm.JobConfig(
        dataset='/EmbeddingRun2016B/pellicci-EmbeddedMuTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Embed-MuTau-B_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016C/pellicci-EmbeddedMuTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Embed-MuTau-C_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016D/pellicci-EmbeddedMuTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Embed-MuTau-D_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016E/pellicci-EmbeddedMuTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Embed-MuTau-E_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016F/pellicci-EmbeddedMuTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Embed-MuTau-F_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016G/pellicci-EmbeddedMuTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Embed-MuTau-G_2016', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2016H/pellicci-EmbeddedMuTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Embed-MuTau-H_2016', inputDBS="phys03"),

]

# 2017 Embedded samples
samplesDict['2017_embed_emu'] = [
    bm.JobConfig(
        dataset='/EmbeddingRun2017B/pellicci-EmbeddedElMu_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_Embed-EMu-B_2017', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2017C/pellicci-EmbeddedElMu_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_Embed-EMu-C_2017', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2017D/pellicci-EmbeddedElMu_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_Embed-EMu-D_2017', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2017E/pellicci-EmbeddedElMu_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_Embed-EMu-E_2017', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2017F/pellicci-EmbeddedElMu_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_Embed-EMu-F_2017', inputDBS="phys03"),
]

samplesDict['2017_embed_etau'] = [
    bm.JobConfig(
        dataset='/EmbeddingRun2017B/pellicci-EmbeddedElTau_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_Embed-ETau-B_2017', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2017C/pellicci-EmbeddedElTau_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_Embed-ETau-C_2017', inputDBS="phys03"),
    bm.JobConfig(
        dataset=' /EmbeddingRun2017D/pellicci-EmbeddedElTau_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_Embed-ETau-D_2017', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2017E/pellicci-EmbeddedElTau_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_Embed-ETau-E_2017', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2017F/pellicci-EmbeddedElTau_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_Embed-ETau-F_2017', inputDBS="phys03"),
]

samplesDict['2017_embed_mutau'] = [
    bm.JobConfig(
        dataset='/EmbeddingRun2017B/pellicci-EmbeddedMuTau_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_Embed-MuTau-B_2017', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2017C/pellicci-EmbeddedMuTau_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_Embed-MuTau-C_2017', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2017D/pellicci-EmbeddedMuTau_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_Embed-MuTau-D_2017', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2017E/pellicci-EmbeddedMuTau_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_Embed-MuTau-E_2017', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2017F/pellicci-EmbeddedMuTau_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_Embed-MuTau-F_2017', inputDBS="phys03"),
]

# 2018 Embedded samples
samplesDict['2018_embed_emu'] = [
    bm.JobConfig(
        dataset='/EmbeddingRun2018A/pellicci-EmbeddedElMu_NANOAOD_2018_10222V1-9b11f648cb233dc346c2d0860bbea8f9/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_Embed-EMu-A_2018', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2018B/pellicci-EmbeddedElMu_NANOAOD_2018_10222V1-9b11f648cb233dc346c2d0860bbea8f9/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_Embed-EMu-B_2018', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2018C/pellicci-EmbeddedElMu_NANOAOD_2018_10222V1-9b11f648cb233dc346c2d0860bbea8f9/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_Embed-EMu-C_2018', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2018D/pellicci-EmbeddedElMu_NANOAOD_2018_10222V1-e181eeebc101019f884cba30e429f851/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_Embed-EMu-D_2018', inputDBS="phys03"),
]

samplesDict['2018_embed_etau'] = [
    bm.JobConfig(
        dataset='/EmbeddingRun2018A/pellicci-EmbeddedElTau_NANOAOD_2018_10222V1-9b11f648cb233dc346c2d0860bbea8f9/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_Embed-ETau-A_2018', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2018B/pellicci-EmbeddedElTau_NANOAOD_2018_10222V1-9b11f648cb233dc346c2d0860bbea8f9/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_Embed-ETau-B_2018', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2018C/pellicci-EmbeddedElTau_NANOAOD_2018_10222V1-9b11f648cb233dc346c2d0860bbea8f9/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_Embed-ETau-C_2018', inputDBS="phys03"),
    bm.JobConfig(
        dataset=' /EmbeddingRun2018D/pellicci-EmbeddedElTau_NANOAOD_2018_10222V1-e181eeebc101019f884cba30e429f851/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_Embed-ETau-D_2018', inputDBS="phys03"),
]

samplesDict['2018_embed_mutau'] = [
    bm.JobConfig(
        dataset='/EmbeddingRun2018A/pellicci-EmbeddedMuTau_NANOAOD_2018_10222V1-9b11f648cb233dc346c2d0860bbea8f9/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_Embed-MuTau-A_2018', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2018B/pellicci-EmbeddedMuTau_NANOAOD_2018_10222V1-9b11f648cb233dc346c2d0860bbea8f9/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_Embed-MuTau-B_2018', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2018C/pellicci-EmbeddedMuTau_NANOAOD_2018_10222V1-9b11f648cb233dc346c2d0860bbea8f9/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_Embed-MuTau-C_2018', inputDBS="phys03"),
    bm.JobConfig(
        dataset='/EmbeddingRun2018D/pellicci-EmbeddedMuTau_NANOAOD_2018_10222V1-e181eeebc101019f884cba30e429f851/USER',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_Embed-MuTau-D_2018', inputDBS="phys03"),
]

#################################################
#                                               #
#--------------- Running 2016 MC ---------------#
#                                               #
#################################################

### redefine N(events/job) for MC ###
nEvtPerJob = 2

# signal
nEvtSigPerJob = 0.008 #only 125 events per file, 40k-80k per dataset, so 5-10 jobs per signal
samplesDict['2016_signal'] = [
    #### z samples ####
    bm.JobConfig( 
        dataset='/ZEMuAnalysis_2016_8028V1/pellicci-ZEMuAnalysis_NANOAOD_10218V1-b1c578360797952dfc156561d5f36519/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='LFVAnalysis_ZEMu_2016', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZETau_2016_8028V1/mimacken-LFVAnalysis_NANOAOD_8028V1-d11e799790792310589ef5ee63b17d7a/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='LFVAnalysis_ZETau_2016', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZMuTau_2016_8028V1/mimacken-LFVAnalysis_NANOAOD_8028V1-d11e799790792310589ef5ee63b17d7a/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='LFVAnalysis_ZMuTau_2016', inputDBS="phys03"),
    #### h samples ####
    bm.JobConfig( 
        dataset='/LFVAnalysis_HEMu_2016_8028V1/mimacken-LFVAnalysis_NANOAOD_8028V1-d11e799790792310589ef5ee63b17d7a/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='LFVAnalysis_HEMu_2016', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_HETau_2016_8028V1/mimacken-LFVAnalysis_NANOAOD_8028V1-d11e799790792310589ef5ee63b17d7a/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='LFVAnalysis_HETau_2016', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_HMuTau_2016_8028V1/mimacken-LFVAnalysis_NANOAOD_8028V1-d11e799790792310589ef5ee63b17d7a/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='LFVAnalysis_HMuTau_2016', inputDBS="phys03"),
]

# top
samplesDict['2016_top'] = [
    # semilep tt 
    bm.JobConfig( 
        dataset='/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_ttbarToSemiLeptonic_2016'),
    # leptonic tt  
    bm.JobConfig( 
        dataset='/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_ttbarlnu_2016'),


    # hadronic tt  
    bm.JobConfig( 
        dataset='/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_ttbarToHadronic_2016'),

    # tW top 
    bm.JobConfig( 
        dataset='/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_SingleToptW_2016'),

    # tW antitop 
    bm.JobConfig(
        dataset='/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_SingleAntiToptW_2016'),

    # t top 
    bm.JobConfig( 
        dataset='/ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v2/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_SingleToptChannel_2016'),

    # t antitop 
    bm.JobConfig( 
        dataset='/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_SingleAntiToptChannel_2016'),
]

# w
samplesDict['2016_w'] = [
    # wjets inclusive
    bm.JobConfig( 
        dataset='/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Wlnu_2016'),

    bm.JobConfig( 
        dataset='/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Wlnu-ext_2016'),

    bm.JobConfig( 
        dataset='/W1JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Wlnu-1J_2016'),

    bm.JobConfig( 
        dataset='/W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Wlnu-2J_2016'),

    bm.JobConfig( 
        dataset='/W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Wlnu-3J_2016'),

    bm.JobConfig( 
        dataset='/W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_Wlnu-4J_2016'),
]

# z
samplesDict['2016_z'] = [
    bm.JobConfig(
        dataset='/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_DY10to50_2016'),

    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_DY50-amc_2016'),

    # bm.JobConfig(
    #     dataset='/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM',
    #     nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_DY50_2016'),

    # bm.JobConfig(
    #     dataset='/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM',
    #     nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_DY50-ext_2016'),    
]

# di(tri)-boson
samplesDict['2016_vv'] = [
    # ww2l2nu
    bm.JobConfig(
        dataset='/WWTo2L2Nu_13TeV-powheg/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_WW_2016'),

    # wwlnu2q
    bm.JobConfig(
        dataset='/WWToLNuQQ_13TeV-powheg/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_WWLNuQQ_2016'),

    # wz
    bm.JobConfig(
        dataset='/WZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_WZ_2016'),

    # zz
    bm.JobConfig(
        dataset='/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_ZZ_2016'),

    # www
    bm.JobConfig(
        dataset='/WWW_4F_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_WWW_2016'),

    # EWK W- + 2j
    bm.JobConfig(
        dataset='/EWKWMinus2Jets_WToLNu_M-50_13TeV-madgraph-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_EWKWminus_2016'),

    # EWK W+ + 2j
    bm.JobConfig(
        dataset='/EWKWPlus2Jets_WToLNu_M-50_13TeV-madgraph-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_EWKWplus_2016'),

    #W+gamma
    bm.JobConfig( 
        dataset='/WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext3-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_WGamma_2016'),

    # EWK Z + 2j
    bm.JobConfig(
        dataset='/EWKZ2Jets_ZToLL_M-50_13TeV-madgraph-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_EWKZ-M50_2016'),
]

# qcd
samplesDict['2016_qcd'] = [
    # 20-30, EM enriched
    bm.JobConfig(
        dataset='/QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDEMEnrich20to30_2016'),

    # 30-50, EM enriched
    bm.JobConfig(
        dataset='/QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDEMEnrich30to50_2016'),

    # 30-50 ext, EM enriched
    bm.JobConfig(
        dataset='/QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDEMEnrich30to50-ext_2016'),

    # 50-80, EM enriched
    bm.JobConfig(
        dataset='/QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDEMEnrich50to80_2016'),

    # 50-80 ext, EM enriched
    bm.JobConfig(
        dataset='/QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDEMEnrich50to80-ext_2016'),

    # 80-120, EM enriched
    bm.JobConfig(
        dataset='/QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDEMEnrich80to120_2016'),

    # 80-120 ext, EM enriched
    bm.JobConfig(
        dataset='/QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDEMEnrich80to120-ext_2016'),

    # 120-170, EM enriched
    bm.JobConfig(
        dataset='/QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDEMEnrich120to170_2016'),

    # 120-170 ext, EM enriched
    bm.JobConfig(
        dataset='/QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDEMEnrich120to170-ext_2016'),

    # 170-300, EM enriched
    bm.JobConfig(
        dataset='/QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDEMEnrich170to300_2016'),

    # 300-inf, EM enriched
    bm.JobConfig(
        dataset='/QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDEMEnrich300toInf_2016'),

    # 30-inf, MGG 40-80, double EM enriched
    bm.JobConfig(
        dataset='/QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich30toInf_2016'),

    # 30-40, MGG 80-inf, double EM enriched
    bm.JobConfig(
        dataset='/QCD_Pt-30to40_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich30to40_2016'),

    # 40-inf, MGG 80-inf, double EM enriched
    bm.JobConfig(
        dataset='/QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich40toInf_2016'),
]

#################################################
#                                               #
#--------------- Running 2017 MC ---------------#
#                                               #
#################################################

# signal
samplesDict['2017_signal'] = [
    #### z samples ####
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZEMu_2017_934V2/pellicci-LFVAnalysis_NANOAOD_10218V2-df769e3b6a68f1e897c86e71b2345849/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='LFVAnalysis_ZEMu_2017', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZETau_2017_934V2/pellicci-LFVAnalysis_NANOAOD_10218V2-df769e3b6a68f1e897c86e71b2345849/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='LFVAnalysis_ZETau_2017', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZMuTau_2017_934V2/pellicci-LFVAnalysis_NANOAOD_10218V2-df769e3b6a68f1e897c86e71b2345849/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='LFVAnalysis_ZMuTau_2017', inputDBS="phys03"),
    #### h samples ####
    bm.JobConfig( 
        dataset='/LFVAnalysis_HEMu_2017_934V2/pellicci-LFVAnalysis_NANOAOD_10218V2-df769e3b6a68f1e897c86e71b2345849/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='LFVAnalysis_HEMu_2017', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_HETau_2017_934V2/pellicci-LFVAnalysis_NANOAOD_10218V2-df769e3b6a68f1e897c86e71b2345849/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='LFVAnalysis_HETau_2017', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_HMuTau_2017_934V2/pellicci-LFVAnalysis_NANOAOD_10218V2-df769e3b6a68f1e897c86e71b2345849/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='LFVAnalysis_HMuTau_2017', inputDBS="phys03"),
]

# top
samplesDict['2017_top'] = [
    # semilep tt 
    bm.JobConfig( 
        dataset='/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_ttbarToSemiLeptonic_2017'),
    # leptonic tt  
    bm.JobConfig( 
        dataset='/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_ttbarlnu_2017'),


    # hadronic tt  
    bm.JobConfig( 
        dataset='/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v2/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_ttbarToHadronic_2017'),

    # tW top 
    bm.JobConfig( 
        dataset='/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_SingleToptW_2017'),

    # tW antitop 
    bm.JobConfig(
        dataset='/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_SingleAntiToptW_2017'),

    # t top 
    bm.JobConfig( 
        dataset='/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_SingleToptChannel_2017'),

    # t antitop 
    bm.JobConfig( 
        dataset='/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_SingleAntiToptChannel_2017'),
]

# w
samplesDict['2017_w'] = [
    # wjets inclusive
    bm.JobConfig( 
        dataset='/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_Wlnu_2017'),

    bm.JobConfig( 
        dataset='/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_Wlnu-ext_2017'),

    bm.JobConfig( 
        dataset='/W1JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_Wlnu-1J_2017'),

    bm.JobConfig( 
        dataset='/W2JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_Wlnu-2J_2017'),

    bm.JobConfig( 
        dataset='/W3JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_Wlnu-3J_2017'),

    bm.JobConfig( 
        dataset='/W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_Wlnu-4J_2017'),
]

# z
samplesDict['2017_z'] = [
    bm.JobConfig(
        dataset='/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_DY10to50_2017'),

    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_DY50_2017'),

    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext3-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_DY50-ext_2017'),    
]

# di(tri)-boson + EWK V + W+Gamma
samplesDict['2017_vv'] = [
    # ww2l2nu
    bm.JobConfig(
        dataset='/WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_WW_2017'),

    # wwlnu2q
    bm.JobConfig(
        dataset='/WWToLNuQQ_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_WWLNuQQ_2017'),

    # wz
    bm.JobConfig(
        dataset='/WZ_TuneCP5_13TeV-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_WZ_2017'),

    # zz
    bm.JobConfig(
        dataset='/ZZ_TuneCP5_13TeV-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_ZZ_2017'),

    # www
    bm.JobConfig(
        dataset='/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_WWW_2017'),

    # EWK W- + 2j
    bm.JobConfig(
        dataset='/EWKWMinus2Jets_WToLNu_M-50_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_EWKWminus_2017'),

    # EWK W+ + 2j
    bm.JobConfig(
        dataset='/EWKWPlus2Jets_WToLNu_M-50_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_EWKWplus_2017'),

    #W+gamma
    bm.JobConfig( 
        dataset='/WGToLNuG_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_WGamma_2017'),

    # EWK Z + 2j
    bm.JobConfig(
        dataset='/EWKZ2Jets_ZToLL_M-50_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_EWKZ-M50_2017'),
]

# qcd
samplesDict['2017_qcd'] = [
    # 30-40
    bm.JobConfig(
        dataset='/QCD_Pt-30to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich30to40_2017'),

    # 30-inf
    bm.JobConfig(
        dataset='/QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich30toInf_2017'),

    # 40-inf
    bm.JobConfig(
        dataset='/QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich40toInf_2017'),
]

#################################################
#                                               #
#--------------- Running 2018 MC ---------------#
#                                               #
#################################################

# signal
samplesDict['2018_signal'] = [
    #### z samples ####
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZEMu_2018_10218V1/pellicci-LFVAnalysis_NANOAOD_10218V1-a7880b551d3b12f0ed185e04212304eb/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='LFVAnalysis_ZEMu_2018', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZETau_2018_10218V1/pellicci-LFVAnalysis_NANOAOD_10218V1-a7880b551d3b12f0ed185e04212304eb/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='LFVAnalysis_ZETau_2018', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZMuTau_2018_10218V1/pellicci-LFVAnalysis_NANOAOD_10218V1-a7880b551d3b12f0ed185e04212304eb/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='LFVAnalysis_ZMuTau_2018', inputDBS="phys03"),
    #### h samples ####
    bm.JobConfig( 
        dataset='/LFVAnalysis_HEMu_2018_10218V1/pellicci-LFVAnalysis_NANOAOD_10218V1-a7880b551d3b12f0ed185e04212304eb/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='LFVAnalysis_HEMu_2018', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_HETau_2018_10218V1/pellicci-LFVAnalysis_NANOAOD_10218V1-a7880b551d3b12f0ed185e04212304eb/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='LFVAnalysis_HETau_2018', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_HMuTau_2018_10218V1/pellicci-LFVAnalysis_NANOAOD_10218V1-a7880b551d3b12f0ed185e04212304eb/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='LFVAnalysis_HMuTau_2018', inputDBS="phys03"),
]

# top
samplesDict['2018_top'] = [
    # semilep tt 
    bm.JobConfig( 
        dataset='/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext3-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_ttbarToSemiLeptonic_2018'),
    # leptonic tt  
    bm.JobConfig( 
        dataset='/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_ttbarlnu_2018'),

    # hadronic tt  
    bm.JobConfig( 
        dataset='/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext2-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_ttbarToHadronic_2018'),

    # tW top 
    bm.JobConfig( 
        dataset='/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_SingleToptW_2018'),

    # tW antitop 
    bm.JobConfig(
        dataset='/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_SingleAntiToptW_2018'),

    # t top 
    bm.JobConfig( 
        dataset='/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_SingleToptChannel_2018'),

    # t antitop 
    bm.JobConfig( 
        dataset='/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_SingleAntiToptChannel_2018'),
]

# w
samplesDict['2018_w'] = [
    # wjets inclusive
    bm.JobConfig( 
        dataset='/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_Wlnu_2018'),

    bm.JobConfig( 
        dataset='/W1JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_Wlnu-1J_2018'),

    bm.JobConfig( 
        dataset='/W2JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_Wlnu-2J_2018'),

    bm.JobConfig( 
        dataset='/W3JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_Wlnu-3J_2018'),

    bm.JobConfig( 
        dataset='/W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_Wlnu-4J_2018'),
]

# z
samplesDict['2018_z'] = [
    bm.JobConfig(
        dataset='/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_DY10to50_2018'),

    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext2-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_DY50-amc_2018'),

    # bm.JobConfig(
    #     dataset='/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
    #     nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_DY50_2018'),
]

# di(tri)-boson + EWK V + W+Gamma
samplesDict['2018_vv'] = [
    # ww2l2nu
    bm.JobConfig(
        dataset='/WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_WW_2018'),

    # wwlnu2q
    bm.JobConfig(
        dataset='/WWToLNuQQ_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_WWLNuQQ_2018'),

    # wz
    bm.JobConfig(
        dataset='/WZ_TuneCP5_13TeV-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_WZ_2018'),

    # zz
    bm.JobConfig(
        dataset='/ZZ_TuneCP5_13TeV-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_ZZ_2018'),

    # www
    bm.JobConfig(
        dataset='/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_WWW_2018'),

    # EWK W- + 2j
    bm.JobConfig(
        dataset='/EWKWMinus2Jets_WToLNu_M-50_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_EWKWminus_2018'),

    # EWK W+ + 2j
    bm.JobConfig(
        dataset='/EWKWPlus2Jets_WToLNu_M-50_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_EWKWplus_2018'),

    #W+gamma
    bm.JobConfig( 
        dataset='/WGToLNuG_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_WGamma_2018'),

    # EWK Z + 2j
    bm.JobConfig(
        dataset='/EWKZ2Jets_ZToLL_M-50_TuneCP5_PSweights_13TeV-madgraph-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_EWKZ-M50_2018'),
]

# qcd
samplesDict['2018_qcd'] = [
    # 15-20, EM enriched
    bm.JobConfig(
        dataset='/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_QCDEMEnrich15to20_2018'),

    # 20-30, EM enriched
    bm.JobConfig(
        dataset='/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_QCDEMEnrich20to30_2018'),

    # 30-50, EM enriched
    bm.JobConfig(
        dataset='/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_QCDEMEnrich30to50_2018'),

    # 50-80, EM enriched
    bm.JobConfig(
        dataset='/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_QCDEMEnrich50to80_2018'),

    # 80-120, EM enriched
    bm.JobConfig(
        dataset='/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_QCDEMEnrich80to120_2018'),

    # 120-170, EM enriched
    bm.JobConfig(
        dataset='/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_QCDEMEnrich120to170_2018'),

    # 170-300, EM enriched
    bm.JobConfig(
        dataset='/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_QCDEMEnrich170to300_2018'),

    # 300-inf, EM enriched
    bm.JobConfig(
        dataset='/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_QCDEMEnrich300toInf_2018'),



    # 30-40
    # bm.JobConfig(
    #     dataset='', #None found in DAS...
    #     nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich30to40_2018'),

    # 30-inf
    bm.JobConfig(
        dataset='/QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich30toInf_2018'),

    # 40-inf
    bm.JobConfig(
        dataset='/QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich40toInf_2018'),
]

# -----------------------------
# submit to batch
# -----------------------------
# samplesToSubmit = [ "2016_signal" ]
# samplesToSubmit = ["2016_signal", "2016_top", "2016_z", "2016_w", "2016_vv", "2016_qcd"]
# samplesToSubmit = ["2016_embed_emu", "2016_embed_etau", "2016_embed_mutau"]
# samplesToSubmit = ["2016_SingleElectron", "2016_SingleMuon"]
# samplesToSubmit = ["2017_signal", "2017_top", "2017_z", "2017_w", "2017_vv", "2017_qcd"]
# samplesToSubmit = ["2018_signal", "2018_top", "2018_z", "2018_w", "2018_vv", "2018_qcd"]
# samplesToSubmit = ["2018_signal", "2018_top", "2018_z", "2018_w", "2018_vv", "2018_qcd", "2018_SingleElectron", "2018_SingleMuon"]
# samplesToSubmit = ["2016_vv", "2017_top", "2017_vv", "2017_z", "2018_top", "2018_vv", "2018_z"]
samplesToSubmit = samplesDict.keys()
samplesToSubmit.sort()
doYears = ["2018"]
# doYears = ["2017"]
# doYears = ["2016", "2017", "2018"]
sampleTag = ""
configs = []

for s in samplesToSubmit:
    if s[:4] in doYears and (sampleTag == "" or sampleTag in s):
        configs += samplesDict[s]

if configs == []:
    print "No datasets to submit!"
    exit()

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

batchMaster.submit_to_batch(doSubmit=True)
