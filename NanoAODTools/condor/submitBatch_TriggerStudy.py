#! /usr/bin/env python

# Trigger study, only ntuple signal and ignore triggers

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

executable = 'execBatch.sh'
analyzer   = 'TriggerStudy'
stage_dir  = 'batch'
if 'lxplus' in host: #use SMP space
    output_dir = '/store/group/phys_smp/ZLFV/batch'
    # output_dir = '/eos/cms/store/group/phys_smp/ZLFV/batch'
    location   = 'lxplus'
elif user == 'mmackenz':
    output_dir = '/store/user/mimacken/nano_batchout'
    location   = 'lpc'
else:
    output_dir = '/store/user/%s/batch' % (user)
    location   = 'lpc'

print 'location = %s, output_dir = %s' % (location, output_dir)


# -----------------------------
# Set job configurations.  
# -----------------------------
samplesDict = {}

#Load currently used samples
sampleMap = SampleMap()

nEvtPerJob = 3 # faster jobs, # in unit of 1e6 , 5-10 are good settings. 


#################################################
#                                               #
#--------------- Running 2016 MC ---------------#
#                                               #
#################################################

# signal
nEvtSigPerJob = 0.006 #only 125 events per file, 40k-80k per dataset, so 5-10 jobs per signal
samplesDict['2016_signal'] = [
    #### z samples ####
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2016/ZEMu_NANO_200k/CRAB_UserFiles/ZLFVAnalysis_NANO_8028V2/221024_122309/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='TriggerStudy_ZEMu-v2_2016', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 1, user_tag = 'Sum'),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2016/ZETau_NANO_200k/CRAB_UserFiles/ZLFVAnalysis_NANO_8028V2/221024_122331/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='TriggerStudy_ZETau-v2_2016', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 1, user_tag = 'Sum'),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2016/ZMuTau_NANO_200k/CRAB_UserFiles/ZLFVAnalysis_NANO_8028V2/221024_122352/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='TriggerStudy_ZMuTau-v2_2016', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 1, user_tag = 'Sum'),
    # extension samples
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2016_ext/ZEMu_NANO_2016_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2016_400k/230409_095223/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='TriggerStudy_ZEMu-v3_2016', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2016_ext/ZETau_NANO_2016_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2016_400k/230409_095230/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='TriggerStudy_ZETau-v3_2016', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2016_ext/ZMuTau_NANO_2016_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2016_400k/230409_095239/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='TriggerStudy_ZMuTau-v3_2016', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    # # #### h samples ####
    # bm.JobConfig( 
    #     dataset='/LFVAnalysis_HEMu_2016_8028V1/mimacken-LFVAnalysis_NANOAOD_8028V1-d11e799790792310589ef5ee63b17d7a/USER',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='TriggerStudy_HEMu_2016', inputDBS="phys03"),
    # bm.JobConfig( 
    #     dataset='/LFVAnalysis_HETau_2016_8028V1/mimacken-LFVAnalysis_NANOAOD_8028V1-d11e799790792310589ef5ee63b17d7a/USER',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='TriggerStudy_HETau_2016', inputDBS="phys03"),
    # bm.JobConfig( 
    #     dataset='/LFVAnalysis_HMuTau_2016_8028V1/mimacken-LFVAnalysis_NANOAOD_8028V1-d11e799790792310589ef5ee63b17d7a/USER',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='TriggerStudy_HMuTau_2016', inputDBS="phys03"),
]


#################################################
#                                               #
#--------------- Running 2017 MC ---------------#
#                                               #
#################################################

# signal
samplesDict['2017_signal'] = [
    #### z samples ####
    # samples with mass cut bug
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017/ZEMu_NANO_2017_200k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_200k/221030_185439/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='TriggerStudy_ZEMu-v2_2017', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 1, user_tag = 'Sum'),
    # bm.JobConfig( 
    #     dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017/ZETau_NANO_2017_200k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_200k/221030_185449/0000/',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='TriggerStudy_ZETau-v2_2017', user_redir = 'root://eoscms.cern.ch/',
    #     user_nfiles = 1, user_tag = 'Sum'),
    # bm.JobConfig( 
    #     dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017/ZMuTau_NANO_2017_200k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_200k/221030_185500/0000/',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='TriggerStudy_ZMuTau-v2_2017', user_redir = 'root://eoscms.cern.ch/',
    #     user_nfiles = 1, user_tag = 'Sum'),
    # extensions/fixed mass cut
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017_ext/ZEMu_NANO_2017_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_400k/230424_161514/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='TriggerStudy_ZEMu-v3a_2017', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017_ext/ZEMu_NANO_2017_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_400k/230424_161514/0001/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='TriggerStudy_ZEMu-v3b_2017', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017_ext/ZETau_NANO_2017_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_400k/230424_161523/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='TriggerStudy_ZETau-v3a_2017', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017_ext/ZETau_NANO_2017_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_400k/230424_161523/0001/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='TriggerStudy_ZETau-v3b_2017', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017_ext/ZMuTau_NANO_2017_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_400k/230424_161532/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='TriggerStudy_ZMuTau-v3a_2017', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017_ext/ZMuTau_NANO_2017_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_400k/230424_161532/0001/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='TriggerStudy_ZMuTau-v3b_2017', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    # #### h samples ####
    # bm.JobConfig( 
    #     dataset='/LFVAnalysis_HEMu_2017_934V2/pellicci-LFVAnalysis_NANOAOD_10218V2-df769e3b6a68f1e897c86e71b2345849/USER',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='TriggerStudy_HEMu_2017', inputDBS="phys03"),
    # bm.JobConfig( 
    #     dataset='/LFVAnalysis_HETau_2017_934V2/pellicci-LFVAnalysis_NANOAOD_10218V2-df769e3b6a68f1e897c86e71b2345849/USER',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='TriggerStudy_HETau_2017', inputDBS="phys03"),
    # bm.JobConfig( 
    #     dataset='/LFVAnalysis_HMuTau_2017_934V2/pellicci-LFVAnalysis_NANOAOD_10218V2-df769e3b6a68f1e897c86e71b2345849/USER',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='TriggerStudy_HMuTau_2017', inputDBS="phys03"),
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
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2018/ZEMu_NANO_2018_200k/CRAB_UserFiles/ZLFVAnalysis_NANO_2018_200k/221108_132529/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='TriggerStudy_ZEMu-v2_2018', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 1, user_tag = 'Sum'),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2018/ZETau_NANO_2018_200k/CRAB_UserFiles/ZLFVAnalysis_NANO_2018_200k/221108_132542/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='TriggerStudy_ZETau-v2_2018', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 1, user_tag = 'Sum'),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2018/ZMuTau_NANO_2018_200k/CRAB_UserFiles/ZLFVAnalysis_NANO_2018_200k/221108_132555/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='TriggerStudy_ZMuTau-v2_2018', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 1, user_tag = 'Sum'),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2018_ext/ZEMu_NANO_2018_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2018_400k/230503_130955/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='TriggerStudy_ZEMu-v3a_2018', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2018_ext/ZEMu_NANO_2018_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2018_400k/230503_130955/0001/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='TriggerStudy_ZEMu-v3b_2018', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2018_ext/ZETau_NANO_2018_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2018_400k/230503_131032/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='TriggerStudy_ZETau-v3a_2018', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2018_ext/ZETau_NANO_2018_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2018_400k/230503_131032/0001/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='TriggerStudy_ZETau-v3b_2018', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2018_ext/ZMuTau_NANO_2018_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2018_400k/230503_131050/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='TriggerStudy_ZMuTau-v3a_2018', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2018_ext/ZMuTau_NANO_2018_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2018_400k/230503_131050/0001/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='TriggerStudy_ZMuTau-v3b_2018', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    # #### h samples ####
    # bm.JobConfig( 
    #     dataset='/LFVAnalysis_HEMu_2018_10218V1/pellicci-LFVAnalysis_NANOAOD_10218V1-a7880b551d3b12f0ed185e04212304eb/USER',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='TriggerStudy_HEMu_2018', inputDBS="phys03"),
    # bm.JobConfig( 
    #     dataset='/LFVAnalysis_HETau_2018_10218V1/pellicci-LFVAnalysis_NANOAOD_10218V1-a7880b551d3b12f0ed185e04212304eb/USER',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='TriggerStudy_HETau_2018', inputDBS="phys03"),
    # bm.JobConfig( 
    #     dataset='/LFVAnalysis_HMuTau_2018_10218V1/pellicci-LFVAnalysis_NANOAOD_10218V1-a7880b551d3b12f0ed185e04212304eb/USER',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='TriggerStudy_HMuTau_2018', inputDBS="phys03"),
]


# -----------------------------
# submit to batch
# -----------------------------

# samplesToSubmit = ["2017_signal"]
samplesToSubmit = samplesDict.keys()

samplesToSubmit.sort()
doYears = ["2018"]
# doYears = ["2016", "2017", "2018"]
sampleTag = ""
sampleVeto = ""
configs = []

for s in samplesToSubmit:
    if s[:4] in doYears and (sampleTag == "" or sampleTag in s) and (sampleVeto == "" or sampleVeto not in s):
        configs += samplesDict[s]
        if dryRun:
            for sample in samplesDict[s]:
                print "Adding sample", sample._suffix, "to the processing list"

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
    maxFilesPerJob = 100
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
