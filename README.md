# LFV Z Analysis

## Description:
  A modularized ntuplizer that reads standard NanoAOD and provides a slimmer version with cleaned objects and complex variables.
  The output is again a standard NanoAOD format file, and can be processed with any compatible histogramming tool. It is based on NanoAOD tools. 

  The modules are:
    -GenAnalyzer.py = scans the GenParticle collection and creates the configured decay. eg Z->mue is 23->13,11. For cascade decays we can add
    several modules together.
    -GenZllAnalyzer.py = scans the GenParticle collection and attempts to find a Z->ll' decay. If a Z boson isn't found, it will
    look for exactly two primary charged leptons
    -GenIdenticalMothersDiscriminator.py = in case of two identical particles this can be used to disentangle them.
    -GenRecoMatcher.py = takes genparticles as inputs and matches them with reco
    -HTSkimmer.py = creates the HT variable based on configuration.
    -JetLepCleaner.py = removes overlapping jets (or leptons) with leptons (or jets).
    -JetSkimmer.py = skims the jet collection
    -LeptonSkimmer.py = skims the lepton collections
    -SelectionFilter.py = applies some selection logic to filter events to different channels (e.g. e+mu vs mu+tau) and filter
    out events that don't satisfy any channel selections

## Building instructions:
```
cmsrel CMSSW_10_6_29
cd CMSSW_10_6_29/src
cmsenv
git clone https://github.com/michaelmackenzie/Z_LFV_analysis PhysicsTools
scram b -j8
```

## Run Locally:
```
cd $CMSSW_BASE/src/PhysicsTools/NanoAODTools/
DATASET="<dataset to analyze, e.g. /SingleMuon/Run2016H-02Apr2020-v1/NANOAOD>"
FILE=`das_client -query="file dataset=${DATASET} <instance=prod/phys03 if needed>" | head -n 1`
xrdcp -f ${FILE} ./NanoAOD.root
python python/LFVAnalyzer.py NanoAOD.root <"data", "MC", or "Embedded"> <"2016", "2017", or "2018">
root.exe tree.root
```
  
## Run on CRAB:
```
cd $CMSSW_BASE/src
cd PhysicsTools/NanoAODTools/crab/
python multi_submit.py
```

## Run on LPC:
Submit jobs:
```
cd $CMSSW_BASE/src/PhysicsTools/NanoAODTools/condor/
#configure submitBatch_Legacy.py samplesToSubmit and doYears lists
./submitBatch_Legacy.py
```
Check job statuses:
```
cd $CMSSW_BASE/src/PhysicsTools/NanoAODTools/condor/
./query_grid.sh
```
When the batch job finishes, check job success:
```
cd $CMSSW_BASE/src/PhysicsTools/NanoAODTools/condor/
./check_batch_job.sh batch/<job directory>/
#if there are failed jobs, resubmit them with:
./check_batch_job.sh batch/<job directory>/ "" d
#try opening each job's root file
./check_batch_job.sh batch/<job directory>/ d
#Only check/resubmit jobs with names containing a tag:
./check_batch_job.sh batch/<job directory>/ "" <"" or d for resubmit> "<tag>"
```
Merge the output files into single file datasets:
```
cd $CMSSW_BASE/src/PhysicsTools/NanoAODTools/condor/
python prepare_batch.py nano_batchout/<job directory>/ <--mc_data ["MC" or "data"]> <--veto [veto tag]> <--tag [to process tag]> <--dryrun> <--year [e.g. 2016]>
```
