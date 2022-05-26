Description:
  A modularized ntuplizer that reads standard NanoAOD and provides a slimmer version with cleaned objects and complex variables. The output is again a standard NanoAOD format file, and can be processed with any compatible histogramming tool. It is based on NanoAOD tools. 

  The modules are:
    -GenAnalyzer.py = scans the GenParticle collection and creates the configured decay. eg Z->mue is 23->13,11. For cascade decays we can add several modules together.
    -GenIdenticalMothersDiscriminator.py = in case of two identical particles this can be used to disentangle them.
    -GenRecoMatcher.py = takes genparticles as inputs and matches them with reco
    -HTSkimmer.py = creates the HT variable based on configuration.
    -JetLepCleaner.py = removes overlapping jets (or leptons) with leptons (or jets).
    -JetSkimmer.py = skims the jet collection
    -LeptonSkimmer.py = skims the lepton collections

Instructions:
  cmsrel CMSSW_10_2_16_UL
  cd CMSSW_10_2_16_UL/src
  cmsenv
  git clone https://github.com/gkaratha/Z_LFV_analysis PhysicsTools
  scram b -j 8  

Run Locally:
  cd $CMSSW_BASE/src
  cd PhysicsTools/NanoAODTools/python/postprocessing/run/
  python runZMuE.py
  
Run on CRAB:
  cd $CMSSW_BASE/src
  cd PhysicsTools/NanoAODTools/crab/
  python multi_submit.py


