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

executable = 'execBatch.sh'
analyzer   = 'LFVAnalyzer'
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
sampleMap.load_samples(sampleMap._data)


nEvtPerJob = 3 # faster jobs, # in unit of 1e6 , 5-10 are good settings. 

#################################################
#                                               #
#---------------  Running data   ---------------#
#                                               #
#################################################
# dataset, nEvtPerJobIn1e6, year, isData, suffix

for dataset in sampleMap._data.keys():
    if not ('SingleMuon' in dataset or 'SingleElectron' in dataset): continue
    samplesDict[dataset] = []
    for sample in sampleMap._data[dataset]:
        if not sample._isdata: continue
        samplesDict[dataset].append(bm.JobConfig(dataset = sample._path, nEvtPerJobIn1e6 = nEvtPerJob, year = sample._year,
                                                 isData = sample._isdata, suffix = 'LFVAnalysis_%s_%i' % (sample._name, sample._year)))



#################################################
#                                               #
#---------- Running Embedded Samples -----------#
#                                               #
#################################################

### redefine N(events/job) for embedding ###
nEvtPerJob = 1 #~25k events per file, ~50-100 files per dataset --> ~5 jobs/dataset

for dataset in sampleMap._data.keys():
    if 'embed' not in dataset: continue
    samplesDict[dataset] = []
    for sample in sampleMap._data[dataset]:
        samplesDict[dataset].append(bm.JobConfig(dataset = sample._path, nEvtPerJobIn1e6 = nEvtPerJob, year = sample._year,
                                                 isData = sample._isdata, suffix = 'LFVAnalysis_%s_%i' % (sample._name, sample._year),
                                                 inputDBS = sample._inputDBS))


#################################################
#                                               #
#--------------- Running 2016 MC ---------------#
#                                               #
#################################################

### redefine N(events/job) for MC ###
nEvtPerJob = 2

# signal
nEvtSigPerJob = 0.006 #only 125 events per file, 40k-80k per dataset, so 5-10 jobs per signal
samplesDict['2016_signal'] = [
    #### z samples ####
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2016/ZEMu_NANO_200k/CRAB_UserFiles/ZLFVAnalysis_NANO_8028V2/221024_122309/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='LFVAnalysis_ZEMu-v2_2016', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 1, user_tag = 'Sum'),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2016/ZETau_NANO_200k/CRAB_UserFiles/ZLFVAnalysis_NANO_8028V2/221024_122331/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='LFVAnalysis_ZETau-v2_2016', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 1, user_tag = 'Sum'),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2016/ZMuTau_NANO_200k/CRAB_UserFiles/ZLFVAnalysis_NANO_8028V2/221024_122352/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='LFVAnalysis_ZMuTau-v2_2016', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 1, user_tag = 'Sum'),
    # extension samples
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2016_ext/ZEMu_NANO_2016_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2016_400k/230409_095223/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='LFVAnalysis_ZEMu-v3_2016', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2016_ext/ZETau_NANO_2016_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2016_400k/230409_095230/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='LFVAnalysis_ZETau-v3_2016', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2016_ext/ZMuTau_NANO_2016_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2016_400k/230409_095239/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='LFVAnalysis_ZMuTau-v3_2016', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    # # #### h samples ####
    # bm.JobConfig( 
    #     dataset='/LFVAnalysis_HEMu_2016_8028V1/mimacken-LFVAnalysis_NANOAOD_8028V1-d11e799790792310589ef5ee63b17d7a/USER',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='LFVAnalysis_HEMu_2016', inputDBS="phys03"),
    # bm.JobConfig( 
    #     dataset='/LFVAnalysis_HETau_2016_8028V1/mimacken-LFVAnalysis_NANOAOD_8028V1-d11e799790792310589ef5ee63b17d7a/USER',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='LFVAnalysis_HETau_2016', inputDBS="phys03"),
    # bm.JobConfig( 
    #     dataset='/LFVAnalysis_HMuTau_2016_8028V1/mimacken-LFVAnalysis_NANOAOD_8028V1-d11e799790792310589ef5ee63b17d7a/USER',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='LFVAnalysis_HMuTau_2016', inputDBS="phys03"),
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

# # qcd
# samplesDict['2016_qcd'] = [
#     # 20-30, EM enriched
#     bm.JobConfig(
#         dataset='/QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDEMEnrich20to30_2016'),

#     # 30-50, EM enriched
#     bm.JobConfig(
#         dataset='/QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDEMEnrich30to50_2016'),

#     # 30-50 ext, EM enriched
#     bm.JobConfig(
#         dataset='/QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDEMEnrich30to50-ext_2016'),

#     # 50-80, EM enriched
#     bm.JobConfig(
#         dataset='/QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDEMEnrich50to80_2016'),

#     # 50-80 ext, EM enriched
#     bm.JobConfig(
#         dataset='/QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDEMEnrich50to80-ext_2016'),

#     # 80-120, EM enriched
#     bm.JobConfig(
#         dataset='/QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDEMEnrich80to120_2016'),

#     # 80-120 ext, EM enriched
#     bm.JobConfig(
#         dataset='/QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDEMEnrich80to120-ext_2016'),

#     # 120-170, EM enriched
#     bm.JobConfig(
#         dataset='/QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDEMEnrich120to170_2016'),

#     # 120-170 ext, EM enriched
#     bm.JobConfig(
#         dataset='/QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDEMEnrich120to170-ext_2016'),

#     # 170-300, EM enriched
#     bm.JobConfig(
#         dataset='/QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDEMEnrich170to300_2016'),

#     # 300-inf, EM enriched
#     bm.JobConfig(
#         dataset='/QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDEMEnrich300toInf_2016'),

#     # 30-inf, MGG 40-80, double EM enriched
#     bm.JobConfig(
#         dataset='/QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCUETP8M1_13TeV_Pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich30toInf_2016'),

#     # 30-40, MGG 80-inf, double EM enriched
#     bm.JobConfig(
#         dataset='/QCD_Pt-30to40_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich30to40_2016'),

#     # 40-inf, MGG 80-inf, double EM enriched
#     bm.JobConfig(
#         dataset='/QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_13TeV_Pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2016", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich40toInf_2016'),
# ]

#################################################
#                                               #
#--------------- Running 2017 MC ---------------#
#                                               #
#################################################

# signal
samplesDict['2017_signal'] = [
    #### z samples ####
    # samples with mass cut bug
    # bm.JobConfig( 
    #     dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017/ZEMu_NANO_2017_200k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_200k/221030_185439/0000/',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='LFVAnalysis_ZEMu-v2_2017', user_redir = 'root://eoscms.cern.ch/',
    #     user_nfiles = 1, user_tag = 'Sum'),
    # bm.JobConfig( 
    #     dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017/ZETau_NANO_2017_200k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_200k/221030_185449/0000/',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='LFVAnalysis_ZETau-v2_2017', user_redir = 'root://eoscms.cern.ch/',
    #     user_nfiles = 1, user_tag = 'Sum'),
    # bm.JobConfig( 
    #     dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017/ZMuTau_NANO_2017_200k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_200k/221030_185500/0000/',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='LFVAnalysis_ZMuTau-v2_2017', user_redir = 'root://eoscms.cern.ch/',
    #     user_nfiles = 1, user_tag = 'Sum'),
    # extensions/fixed mass cut
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017_ext/ZEMu_NANO_2017_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_400k/230424_161514/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='LFVAnalysis_ZEMu-v3a_2017', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017_ext/ZEMu_NANO_2017_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_400k/230424_161514/0001/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='LFVAnalysis_ZEMu-v3b_2017', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017_ext/ZETau_NANO_2017_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_400k/230424_161523/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='LFVAnalysis_ZETau-v3a_2017', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017_ext/ZETau_NANO_2017_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_400k/230424_161523/0001/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='LFVAnalysis_ZETau-v3b_2017', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017_ext/ZMuTau_NANO_2017_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_400k/230424_161532/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='LFVAnalysis_ZMuTau-v3a_2017', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2017_ext/ZMuTau_NANO_2017_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2017_400k/230424_161532/0001/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='LFVAnalysis_ZMuTau-v3b_2017', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    # #### h samples ####
    # bm.JobConfig( 
    #     dataset='/LFVAnalysis_HEMu_2017_934V2/pellicci-LFVAnalysis_NANOAOD_10218V2-df769e3b6a68f1e897c86e71b2345849/USER',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='LFVAnalysis_HEMu_2017', inputDBS="phys03"),
    # bm.JobConfig( 
    #     dataset='/LFVAnalysis_HETau_2017_934V2/pellicci-LFVAnalysis_NANOAOD_10218V2-df769e3b6a68f1e897c86e71b2345849/USER',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='LFVAnalysis_HETau_2017', inputDBS="phys03"),
    # bm.JobConfig( 
    #     dataset='/LFVAnalysis_HMuTau_2017_934V2/pellicci-LFVAnalysis_NANOAOD_10218V2-df769e3b6a68f1e897c86e71b2345849/USER',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='LFVAnalysis_HMuTau_2017', inputDBS="phys03"),
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

# # qcd
# samplesDict['2017_qcd'] = [
#     # 30-40
#     bm.JobConfig(
#         dataset='/QCD_Pt-30to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich30to40_2017'),

#     # 30-inf
#     bm.JobConfig(
#         dataset='/QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich30toInf_2017'),

#     # 40-inf
#     bm.JobConfig(
#         dataset='/QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2017", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich40toInf_2017'),
# ]

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
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='LFVAnalysis_ZEMu-v2_2018', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 1, user_tag = 'Sum'),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2018/ZETau_NANO_2018_200k/CRAB_UserFiles/ZLFVAnalysis_NANO_2018_200k/221108_132542/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='LFVAnalysis_ZETau-v2_2018', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 1, user_tag = 'Sum'),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2018/ZMuTau_NANO_2018_200k/CRAB_UserFiles/ZLFVAnalysis_NANO_2018_200k/221108_132555/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='LFVAnalysis_ZMuTau-v2_2018', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 1, user_tag = 'Sum'),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2018_ext/ZEMu_NANO_2018_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2018_400k/230503_130955/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='LFVAnalysis_ZEMu-v3a_2018', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2018_ext/ZEMu_NANO_2018_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2018_400k/230503_130955/0001/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='LFVAnalysis_ZEMu-v3b_2018', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2018_ext/ZETau_NANO_2018_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2018_400k/230503_131032/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='LFVAnalysis_ZETau-v3a_2018', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2018_ext/ZETau_NANO_2018_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2018_400k/230503_131032/0001/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='LFVAnalysis_ZETau-v3b_2018', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2018_ext/ZMuTau_NANO_2018_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2018_400k/230503_131050/0000/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='LFVAnalysis_ZMuTau-v3a_2018', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    bm.JobConfig( 
        dataset='/store/group/phys_smp/ZLFV/MC_generation/Legacy2018_ext/ZMuTau_NANO_2018_400k/CRAB_UserFiles/ZLFVAnalysis_NANO_2018_400k/230503_131050/0001/',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='LFVAnalysis_ZMuTau-v3b_2018', user_redir = 'root://eoscms.cern.ch/',
        user_nfiles = 50),
    # #### h samples ####
    # bm.JobConfig( 
    #     dataset='/LFVAnalysis_HEMu_2018_10218V1/pellicci-LFVAnalysis_NANOAOD_10218V1-a7880b551d3b12f0ed185e04212304eb/USER',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='LFVAnalysis_HEMu_2018', inputDBS="phys03"),
    # bm.JobConfig( 
    #     dataset='/LFVAnalysis_HETau_2018_10218V1/pellicci-LFVAnalysis_NANOAOD_10218V1-a7880b551d3b12f0ed185e04212304eb/USER',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='LFVAnalysis_HETau_2018', inputDBS="phys03"),
    # bm.JobConfig( 
    #     dataset='/LFVAnalysis_HMuTau_2018_10218V1/pellicci-LFVAnalysis_NANOAOD_10218V1-a7880b551d3b12f0ed185e04212304eb/USER',
    #     nEvtPerJobIn1e6=nEvtSigPerJob, year="2018", isData=False, suffix='LFVAnalysis_HMuTau_2018', inputDBS="phys03"),
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

# # qcd
# samplesDict['2018_qcd'] = [
#     # 15-20, EM enriched
#     bm.JobConfig(
#         dataset='/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_QCDEMEnrich15to20_2018'),

#     # 20-30, EM enriched
#     bm.JobConfig(
#         dataset='/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_QCDEMEnrich20to30_2018'),

#     # 30-50, EM enriched
#     bm.JobConfig(
#         dataset='/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_QCDEMEnrich30to50_2018'),

#     # 50-80, EM enriched
#     bm.JobConfig(
#         dataset='/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_QCDEMEnrich50to80_2018'),

#     # 80-120, EM enriched
#     bm.JobConfig(
#         dataset='/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_QCDEMEnrich80to120_2018'),

#     # 120-170, EM enriched
#     bm.JobConfig(
#         dataset='/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_QCDEMEnrich120to170_2018'),

#     # 170-300, EM enriched
#     bm.JobConfig(
#         dataset='/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_QCDEMEnrich170to300_2018'),

#     # 300-inf, EM enriched
#     bm.JobConfig(
#         dataset='/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_QCDEMEnrich300toInf_2018'),



#     # 30-40
#     # bm.JobConfig(
#     #     dataset='', #None found in DAS...
#     #     nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich30to40_2018'),

#     # 30-inf
#     bm.JobConfig(
#         dataset='/QCD_Pt-30toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich30toInf_2018'),

#     # 40-inf
#     bm.JobConfig(
#         dataset='/QCD_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM',
#         nEvtPerJobIn1e6=nEvtPerJob, year="2018", isData=False, suffix='LFVAnalysis_QCDDoubleEMEnrich40toInf_2018'),
# ]

# -----------------------------
# submit to batch
# -----------------------------

# samplestosubmit = ["2016_signal", "2016_top", "2016_z", "2016_w", "2016_vv", "2016_qcd"]
# samplesToSubmit = ["2016_embed_emu", "2016_embed_etau", "2016_embed_mutau"]
# samplesToSubmit = ["2017_embed_mumu", "2017_embed_ee", "2018_embed_mumu", "2018_embed_ee"]
# samplesToSubmit = ["2016_SingleElectron", "2016_SingleMuon"]
# samplesToSubmit = ["2017_signal", "2017_top", "2017_z", "2017_w", "2017_vv", "2017_qcd"]
# samplesToSubmit = ["2018_signal", "2018_top", "2018_z", "2018_w", "2018_vv", "2018_qcd"]
# samplesToSubmit = ["2018_signal", "2018_top", "2018_z", "2018_w", "2018_vv", "2018_qcd", "2018_SingleElectron", "2018_SingleMuon"]
# samplesToSubmit = ["2016_vv", "2017_top", "2017_vv", "2017_z", "2018_top", "2018_vv", "2018_z"]
samplesToSubmit = samplesDict.keys()

samplesToSubmit.sort()
doYears = ["2018"]
# doYears = ["2016", "2017", "2018"]
sampleTag = "signal"
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
