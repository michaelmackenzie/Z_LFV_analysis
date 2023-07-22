#! /usr/bin/env python
import PhysicsTools.NanoAODTools.condor.BatchMaster as bm
from sample_map import *

import os, sys

dryRun = False

# -----------------------------
# Specify parameters
# -----------------------------

executable = 'execBatch_genz.sh'
analyzer   = 'GenZAnalyzer'
stage_dir  = 'batch'
output_dir = '/store/user/mimacken/gen_z'
location   = 'lpc'



# -----------------------------
# Set job configurations.  
# -----------------------------
samplesDict = {}



#################################################
#                                               #
#----------------- Running MC ------------------#
#                                               #
#################################################

nEvtPerJob = 2

samplesDict['2016_z'] = [
    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='GenZAnalysis_DY50_2016'),
]

samplesDict['2017_z'] = [
    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext3-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='GenZAnalysis_DY50_2017'),    
]

samplesDict['2018_z'] = [
    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext2-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='GenZAnalysis_DY50_2018'),
]

# LO Drell-Yan samples for LO PDF uncertainties
samplesDict['2016_lo_z'] = [
    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, maxEvtPerDataset = 1e7, year="2016", isData=False, suffix='GenZAnalysis_LO-DY50_2016'),
]

# samplesDict['2017_lo_z'] = [
#     bm.JobConfig(
#         dataset='/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext3-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, maxEvtPerDataset = 1e7, year="2017", isData=False, suffix='GenZAnalysis_LO-DY50_2017'),    
# ]

samplesDict['2018_lo_z'] = [
    bm.JobConfig(
        dataset='/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
        nEvtPerJobIn1e6=nEvtPerJob, maxEvtPerDataset = 1e7, year="2018", isData=False, suffix='GenZAnalysis_LO-DY50_2018'),
]

#################################################
#                                               #
#--------------- Running Signal ----------------#
#                                               #
#################################################

nEvtSigPerJob = 0.006 #only 125 events per file, 40k-80k per dataset, so 5-10 jobs per signal
samplesDict['2016_signal'] = [
    #original samples
    bm.JobConfig( 
        dataset='/ZEMuAnalysis_2016_8028V1/pellicci-ZEMuAnalysis_NANOAOD_10218V1-b1c578360797952dfc156561d5f36519/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='GenZAnalysis_ZEMu_2016', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZETau_2016_8028V1/mimacken-LFVAnalysis_NANOAOD_8028V1-d11e799790792310589ef5ee63b17d7a/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='GenZAnalysis_ZETau_2016', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZMuTau_2016_8028V1/mimacken-LFVAnalysis_NANOAOD_8028V1-d11e799790792310589ef5ee63b17d7a/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='GenZAnalysis_ZMuTau_2016', inputDBS="phys03"),
    #v4 samples with higher statistics
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2016/ZEMu_NANO_200k/CRAB_UserFiles/ZLFVAnalysis_NANO_8028V2/221024_122309/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='GenZAnalysis_ZEMu-v3_2016', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 1, user_tag = 'Sum'),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2016/ZETau_NANO_200k/CRAB_UserFiles/ZLFVAnalysis_NANO_8028V2/221024_122331/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='GenZAnalysis_ZETau-v3_2016', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 1, user_tag = 'Sum'),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2016/ZMuTau_NANO_200k/CRAB_UserFiles/ZLFVAnalysis_NANO_8028V2/221024_122352/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='GenZAnalysis_ZMuTau-v3_2016', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 1, user_tag = 'Sum'),

]

samplesDict['2017_signal'] = [
    # # v1 signals with low stats and mass cut problem
    # bm.JobConfig( 
    #     dataset='/LFVAnalysis_ZEMu_2017_934V2/pellicci-LFVAnalysis_NANOAOD_10218V2-df769e3b6a68f1e897c86e71b2345849/USER',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='GenZAnalysis_ZEMu_2017', inputDBS="phys03"),
    # bm.JobConfig( 
    #     dataset='/LFVAnalysis_ZETau_2017_934V2/pellicci-LFVAnalysis_NANOAOD_10218V2-df769e3b6a68f1e897c86e71b2345849/USER',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='GenZAnalysis_ZETau_2017', inputDBS="phys03"),
    # bm.JobConfig( 
    #     dataset='/LFVAnalysis_ZMuTau_2017_934V2/pellicci-LFVAnalysis_NANOAOD_10218V2-df769e3b6a68f1e897c86e71b2345849/USER',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='GenZAnalysis_ZMuTau_2017', inputDBS="phys03"),
    # #v4 samples with higher statistics and mass cut problem
    # bm.JobConfig( 
    #     dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017/ZEMu_NANO_2017_200k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_200k/221030_185439/0000/',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='GenZAnalysis_ZEMu-v3_2017', user_redir = 'root://eoscms.cern.ch/',
    #     user_nfiles = 1, user_tag = 'Sum'),
    # bm.JobConfig( 
    #     dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017/ZETau_NANO_2017_200k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_200k/221030_185449/0000/',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='GenZAnalysis_ZETau-v3_2017', user_redir = 'root://eoscms.cern.ch/',
    #     user_nfiles = 1, user_tag = 'Sum'),
    # bm.JobConfig( 
    #     dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017/ZMuTau_NANO_2017_200k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_200k/221030_185500/0000/',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='GenZAnalysis_ZMuTau-v3_2017', user_redir = 'root://eoscms.cern.ch/',
    #     user_nfiles = 1, user_tag = 'Sum'),
    # v5 samples with high statistics and no mass cut problem
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017_ext/ZEMu_NANO_2017_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_400k/230424_161514/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='GenZAnalysis_ZEMu-v4a_2017', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017_ext/ZEMu_NANO_2017_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_400k/230424_161514/0001/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='GenZAnalysis_ZEMu-v4b_2017', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017_ext/ZETau_NANO_2017_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_400k/230424_161523/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='GenZAnalysis_ZETau-v4a_2017', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017_ext/ZETau_NANO_2017_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_400k/230424_161523/0001/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='GenZAnalysis_ZETau-v4b_2017', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017_ext/ZMuTau_NANO_2017_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_400k/230424_161532/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='GenZAnalysis_ZMuTau-v4a_2017', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017_ext/ZMuTau_NANO_2017_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_400k/230424_161532/0001/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='GenZAnalysis_ZMuTau-v4b_2017', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),

]

samplesDict['2018_signal'] = [
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZEMu_2018_10218V1/pellicci-LFVAnalysis_NANOAOD_10218V1-a7880b551d3b12f0ed185e04212304eb/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='GenZAnalysis_ZEMu_2018', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZETau_2018_10218V1/pellicci-LFVAnalysis_NANOAOD_10218V1-a7880b551d3b12f0ed185e04212304eb/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='GenZAnalysis_ZETau_2018', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZMuTau_2018_10218V1/pellicci-LFVAnalysis_NANOAOD_10218V1-a7880b551d3b12f0ed185e04212304eb/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='GenZAnalysis_ZMuTau_2018', inputDBS="phys03"),
    #v4 samples with higher statistics
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2018/ZEMu_NANO_2018_200k/CRAB_UserFiles/ZLFVAnalysis_NANO_2018_200k/221108_132529/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='GenZAnalysis_ZEMu-v3_2018', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 1, user_tag = 'Sum'),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2018/ZETau_NANO_2018_200k/CRAB_UserFiles/ZLFVAnalysis_NANO_2018_200k/221108_132542/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='GenZAnalysis_ZETau-v3_2018', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 1, user_tag = 'Sum'),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2018/ZMuTau_NANO_2018_200k/CRAB_UserFiles/ZLFVAnalysis_NANO_2018_200k/221108_132555/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='GenZAnalysis_ZMuTau-v3_2018', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 1, user_tag = 'Sum'),
]

# -----------------------------
# submit to batch
# -----------------------------

samplesToSubmit = ['2016_lo_z', '2018_lo_z']
# samplesToSubmit = samplesDict.keys()
samplesToSubmit.sort()

doYears = ["2016", "2017", "2018"]
configs = []

for s in samplesToSubmit:
    if s[:4] in doYears:
        configs += samplesDict[s]

batchMaster = bm.BatchMaster(
    analyzer       = analyzer,
    config_list    = configs, 
    stage_dir      = stage_dir,
    output_dir     = output_dir,
    executable     = executable,
    location       = location,
    maxFilesPerJob = 100
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
