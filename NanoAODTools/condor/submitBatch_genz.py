#! /usr/bin/env python
import PhysicsTools.NanoAODTools.condor.BatchMaster as bm

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
    #v2 samples using AMC@NLO
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZEMu_2016_8028V1/pellicci-LFVAnalysis_NANOAOD_10222V1-07f11a9f6612f8436de459459102e3f2/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='GenZAnalysis_ZEMu-v2_2016', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZETau_2016_8028V1/pellicci-LFVAnalysis_NANOAOD_10222V1-07f11a9f6612f8436de459459102e3f2/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='GenZAnalysis_ZETau-v2_2016', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZMuTau_2016_8028V1/pellicci-LFVAnalysis_NANOAOD_10222V1-07f11a9f6612f8436de459459102e3f2/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='GenZAnalysis_ZMuTau-v2_2016', inputDBS="phys03"),
    #EXO group UL sample
    bm.JobConfig( 
        dataset='/LFV_ZToLL_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16NanoAODv9-106X_mcRun2_asymptotic_v17-v1/NANOAODSIM',
        nEvtPerJobIn1e6=0.5, year="2016", isData=False, suffix='GenZAnalysis_UL-LFVZ_2016'),
    #v3 samples using EXO group input
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZLL_2016_949V1_22prodV2/pellicci-LFVAnalysis_ZLL_NANO_2016_10222V1-07f11a9f6612f8436de459459102e3f2/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2016", isData=False, suffix='GenZAnalysis_LFVZ-v2_2016', inputDBS="phys03"),
]

samplesDict['2017_signal'] = [
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZEMu_2017_934V2/pellicci-LFVAnalysis_NANOAOD_10218V2-df769e3b6a68f1e897c86e71b2345849/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='GenZAnalysis_ZEMu_2017', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZETau_2017_934V2/pellicci-LFVAnalysis_NANOAOD_10218V2-df769e3b6a68f1e897c86e71b2345849/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='GenZAnalysis_ZETau_2017', inputDBS="phys03"),
    bm.JobConfig( 
        dataset='/LFVAnalysis_ZMuTau_2017_934V2/pellicci-LFVAnalysis_NANOAOD_10218V2-df769e3b6a68f1e897c86e71b2345849/USER',
        nEvtPerJobIn1e6=nEvtSigPerJob, year="2017", isData=False, suffix='GenZAnalysis_ZMuTau_2017', inputDBS="phys03"),
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
]

# -----------------------------
# submit to batch
# -----------------------------

samplesToSubmit = [ '2016_signal' ]
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
