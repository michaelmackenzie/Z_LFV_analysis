# Studies related to LFV Z Analysis

## Main ntupling

Ntuple create ntuples for the LFV Z analysis

### Create local ntuples for using the [LFVAnalyzer.py](python/LFVAnalyzer.py) analyzer:

Create initial skim of the NANOAOD:
```
cd $CMSSW_BASE/src/PhysicsTools/NanoAODTools/
DATASET="<dataset to analyze, e.g. /SingleMuon/Run2016H-02Apr2020-v1/NANOAOD>"
FILE=`das_client -query="file dataset=${DATASET} <instance=prod/phys03 if needed>" | head -n 1`
xrdcp -f ${FILE} ./NanoAOD.root
python python/analyzers/LFVAnalyzer.py NanoAOD.root <"data", "MC", or "Embedded"> <"2016", "2017", or "2018">
```

Split into final state selection trees:
```
FILEIN=tree.root
FILEOUT=tree-split.root
root.exe -q -b -l "condor/split_output_tree.C(\"${FILEIN}\", \"${FILEOUT}\")"
rm tree.root
```

Add normalization information from the original NANOAOD to the output skim:
```
FILE=tree-split.root
NANO=NanoAOD.root
root.exe -q -b -l "condor/add_norm.C(\"${NANO}\", \"${FILE}\")"
```

### Submitting to condor:

Configure [submitBatch_Legacy.py](condor/submitBatch_Legacy.py) to submit the desired datasets.
Submit jobs:
```
voms-proxy-init --rfc --voms cms --hours 192
cd $CMSSW_BASE/src/PhysicsTools/NanoAODTools/condor/
./submitBatch_Legacy.py
```

Check condor job status:
```
cd $CMSSW_BASE/src/PhysicsTools/NanoAODTools/condor/
./query_grid.sh [--summary (-s) for less information] [--running (-r) for running job info]
```

When the batch job finishes, check job success:
```
cd $CMSSW_BASE/src/PhysicsTools/NanoAODTools/condor/
./check_batch_job.sh batch/<job directory>/ [--ignorerunning to ignore jobs likely not finished]
#if there are failed jobs, resubmit them with:
./check_batch_job.sh batch/<job directory>/ --resubmit [--tag dataset tag]
#use --help (-h) for more options
```

Merge the output files into single file datasets:
```
cd $CMSSW_BASE/src/PhysicsTools/NanoAODTools/condor/
python prepare_batch.py <batch output dir on eos>/<job directory>/ <--mc_data ["MC" or "data"]> <--veto [veto tag]> <--tag [to process tag]> <--year [e.g. 2016]> <--dryrun>
#use --help (-h) for more options
```

## Gen-level Z analysis

Ntuple gen-level information for Drell-Yan and Z signal samples, without cuts

### Create local ntuples for using the [GenZAnalyzer.py](python/GenZAnalyzer.py) analyzer:

Create initial skim of the NANOAOD:
```
cd $CMSSW_BASE/src/PhysicsTools/NanoAODTools/
DATASET="<dataset to analyze, e.g. /DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM>"
FILE=`das_client -query="file dataset=${DATASET} <instance=prod/phys03 if needed>" | head -n 1`
xrdcp -f ${FILE} ./NanoAOD.root
python python/analyzers/GenZAnalyzer.py NanoAOD.root <""MC", or "Embedded"> <"2016", "2017", or "2018">
```

### Submitting to condor:

Configure [submitBatch_genz.py](condor/submitBatch_genz.py) to submit the desired datasets.
Submit jobs:
```
voms-proxy-init --rfc --voms cms --hours 192
cd $CMSSW_BASE/src/PhysicsTools/NanoAODTools/condor/
./submitBatch_genz.py
```

Check condor job status:
```
cd $CMSSW_BASE/src/PhysicsTools/NanoAODTools/condor/
./query_grid.sh [--summary (-s) for less information] [--running (-r) for running job info]
```

When the batch job finishes, check job success:
```
cd $CMSSW_BASE/src/PhysicsTools/NanoAODTools/condor/
./check_batch_job.sh batch/<job directory>/ --eosdir gen_z [--ignorerunning to ignore jobs likely not finished]
#if there are failed jobs, resubmit them with:
./check_batch_job.sh batch/<job directory>/ --eosdir gen_z --resubmit [--tag dataset tag]
#use --help (-h) for more options
```

Merge the output files into single file datasets:
```
cd $CMSSW_BASE/src/PhysicsTools/NanoAODTools/condor/
python prepare_batch.py gen_z/<job directory>/ --outdir gen_z/files/ <--veto [veto tag]> <--tag [to process tag]><--year [e.g. 2016]> <--dryrun> 
#use --help (-h) for more options
```
