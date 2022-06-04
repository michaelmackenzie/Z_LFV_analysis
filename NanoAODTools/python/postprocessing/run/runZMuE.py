#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.LeptonSkimmer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.HTSkimmer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.JetSkimmer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.JetLepCleaner import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.GenAnalyzer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.GenRecoMatcher import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.TriggerAnalyzer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.LeptonPairCreator import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.FunctionWrapper import *
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles


from importlib import import_module
import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

#cfg in txt because crab helper is not perfect (to be mild)
production=False
outputFolder="." #used only for non-production
outputName="test_new" #default "Skim"
data=True
build_GenSignalDecay_ZMuE=False
build_GenSignalDecay_ZMuTau=False
build_GenSignalDecay_ZETau=False
maxEntries=None #deactivate(use all evts): None


if production:
   from options_ZMuE import options
   outputName = options["outputName"]
   build_GenSignalDecay_ZMuE = options["build_GenSignalDecay_ZMuE"]
   build_GenSignalDecay_ZMuTau = options["build_GenSignalDecay_ZMuTau"]
   build_GenSignalDecay_ZETau = options["build_GenSignalDecay_ZETau"]
   data = options["data"] 

if outputName==None:
   outputName="Skim"   


fnames=[
  #Data
#  "root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v1/130000/02945FF5-75FA-D14B-ADDC-68A0F71E6F5E.root"
  #Z->mue
 'root://cms-xrd-global.cern.ch//store/user/pellicci/ZEMuAnalysis_2016_8028V1/ZEMuAnalysis_NANOAOD_10218V1/200211_105742/0000/ZEMuAnalysis_pythia8_NANOAOD_2016_1.root',\
 'root://cms-xrd-global.cern.ch//store/user/pellicci/ZEMuAnalysis_2016_8028V1/ZEMuAnalysis_NANOAOD_10218V1/200211_105742/0000/ZEMuAnalysis_pythia8_NANOAOD_2016_2.root',\
#     'root://cms-xrd-global.cern.ch//store/user/pellicci/ZEMuAnalysis_2016_8028V1/ZEMuAnalysis_NANOAOD_10218V1/200211_105742/0000/ZEMuAnalysis_pythia8_NANOAOD_2016_3.root',\

]


# only read the branches in this file - for speed deactivate unescairy stuff
branchsel_in ="keep_and_drop_in.txt"
# only write the branches in this file
branchsel_out ="keep_and_drop_out.txt"

if data:
  branchsel_in ="keep_and_drop_data_in.txt"
  branchsel_out ="keep_and_drop_data_out.txt"


#Pre-selection cuts
TriggerCuts="(HLT_IsoMu24 || HLT_IsoMu27 || HLT_Mu50)  && nMuon>0 && nElectron>0"
#TriggerCuts="(HLT_Mu27_Ele37_CaloIdL_MW || HLT_Mu37_Ele27_CaloIdL_MW || HLT_IsoMu24) && nMuon>0 && nElectron>0"
MuonSelection = lambda l : l.pt>10 and abs(l.eta)<2.4 and l.mediumPromptId==True
ElectronSelection = lambda l : l.pt>10 and abs(l.eta)<2.5 and l.mvaFall17V2noIso_WP90==True and abs(l.dxy)<0.5 and abs(l.dz)<1.0
TauSelection = lambda l : l.pt>20 and abs(l.eta)<2.4 and l.idAntiMu>0
JetSelection = lambda l : l.pt>20.0 and abs(l.eta)<3.0 and l.puId>4 and l.jetId>1
 


modules=[]

ZttBuilder=GenAnalyzer(
                  decay='23->15,-15',
                  motherName='GenZTauTau',
                  daughterNames=['GenTau','GenAntiTau'],
                  variables=['pt','eta','phi','pdgId'],
                  conjugate=True,
                  mother_has_antipart=False,
                  daughter_has_antipart=[True,True],
                  skip=False,
                  )
#modules.append(ZttBuilder)

if build_GenSignalDecay_ZMuE:
   ZmueBuilder=GenAnalyzer(
                  decay='23->-13,11',
                  motherName='GenZMuE',
                  daughterNames=['GenMuon','GenElectron'],
                  variables=['pt','eta','phi','pdgId'],
                  conjugate=True,
                  mother_has_antipart=False,
                  daughter_has_antipart=[True,True],
                  skip=False,
                  )
   modules.append(ZmueBuilder)
   RecoElectronMatcher=GenRecoMatcher(
                  genParticles=['GenElectron'],
                  recoCollections=['Electron'],
                  maxDR=0.1
                  )
   modules.append(RecoElectronMatcher)
   RecoMuonMatcher=GenRecoMatcher(
                  genParticles=['GenMuon'],
                  recoCollections=['Muon'],
                  maxDR=0.1
                  )
   modules.append(RecoMuonMatcher)


if build_GenSignalDecay_ZMuTau:
   ZmutauBuilder=GenAnalyzer(
                  decay='23->-13,15',
                  motherName='GenZMuTau',
                  daughterNames=['GenMuon','GenTau'],
                  variables=['pt','eta','phi','pdgId'],
                  conjugate=True,
                  mother_has_antipart=False,
                  daughter_has_antipart=[True,True],
                  skip=False,
                  )
   modules.append(ZmutauBuilder)

   TauToEBuilder=GenAnalyzer(
                  decay='15->11,-12,16',
                  motherName='GenTauToE',
                  daughterNames=['GenElectron','GenNeuE','GenNeuTau'],
                  variables=['pt','eta','phi','pdgId'],
                  grandmother="GenTau_Idx",
                  conjugate=True,
                  mother_has_antipart=True,
                  daughter_has_antipart=[True,True,True],
                  skip=True,
                  )
   modules.append(TauToEBuilder)
   RecoElectronMatcher=GenRecoMatcher(
                  genParticles=['GenElectron'],
                  recoCollections=['Electron'],
                  maxDR=0.1
                  )
   modules.append(RecoElectronMatcher)
   RecoMuonMatcher=GenRecoMatcher(
                  genParticles=['GenMuon'],
                  recoCollections=['Muon'],
                  maxDR=0.1
                  )
   modules.append(RecoMuonMatcher)
# mu tau gen closes


if build_GenSignalDecay_ZETau:
   ZetauBuilder=GenAnalyzer(
                  decay='23->-15,11',
                  motherName='GenZETau',
                  daughterNames=['GenTau','GenElectron'],
                  variables=['pt','eta','phi','pdgId'],
                  conjugate=True,
                  mother_has_antipart=False,
                  daughter_has_antipart=[True,True],
                  skip=True,
                  )
   modules.append(ZetauBuilder)
   TauToMuBuilder=GenAnalyzer(
                  decay='15->13,-14,16',
                  motherName='GenTauToMuon',
                  daughterNames=['GenMuon','GenNeuMu','GenNeuTau'],
                  variables=['pt','eta','phi','pdgId'],
                  grandmother="GenTau_Idx",
                  conjugate=True,
                  mother_has_antipart=True,
                  daughter_has_antipart=[True,True,True],
                  skip=True,
                  )
   modules.append(TauToMuBuilder)
   RecoElectronMatcher=GenRecoMatcher(
                  genParticles=['GenElectron'],
                  recoCollections=['Electron'],
                  maxDR=0.1
                  )
   modules.append(RecoElectronMatcher)
   RecoMuonMatcher=GenRecoMatcher(
                  genParticles=['GenMuon'],
                  recoCollections=['Muon'],
                  maxDR=0.1
                  )
   modules.append(RecoMuonMatcher)
   
#gen e tau closes

MuonSelector= LeptonSkimmer(
                  LepFlavour='Muon',
                  Selection=MuonSelection,
                  Veto=None,
                  minNlep=1,
                  verbose=False
                  )
modules.append(MuonSelector)
ElectronSelector= LeptonSkimmer(
                  LepFlavour='Electron',
                  Selection=ElectronSelection,
                  Veto=None,
                  minNlep=1,
                  verbose=False
                  )
modules.append(ElectronSelector)
TauSelector= LeptonSkimmer(
                  LepFlavour='Tau',
                  Selection=TauSelection,
                  Veto=None,
                  minNlep=-1,
                  verbose=False
                  )
modules.append(TauSelector)

TriggerSelector = TriggerAnalyzer(
                   particlePdgId=13,
                   triggerBits=[1,10],
                   branchNames=["IsoMu24","Mu50"],
                   recoCollection="Muon",
                   maxDR=0.03,
                   maxRelDpt=10.
                  
                   )
modules.append(TriggerSelector)

JetSelector=JetSkimmer( 
                  BtagWPs=[0.1274, 0.4229, 0.7813 ], 
                  nGoodJetMin=-1, 
                  nBJetMax=20 , 
                  Selection=JetSelection,
                  Veto=None
                  )
modules.append(JetSelector)
JetMuonCleaner=JetLepCleaner( 
                  Lepton='Muon',
                  Jet='Jet',
                  dRJet=0.3,
                  RemoveOverlappingJets=True, 
                  RemoveOverlappingLeptons=False
               )
modules.append(JetMuonCleaner)   
JetElectronCleaner=JetLepCleaner(
                  Lepton='Electron',
                  Jet='Jet',
                  dRJet=0.3,
                  RemoveOverlappingJets=True, 
                  RemoveOverlappingLeptons=False
               )
modules.append(JetElectronCleaner)
HTCalculator= HTSkimmer(
                  minJetPt=20,
                  minJetEta=3.0,
                  minJetPUid=-1,
                  minHT=-1,
                  collection="Jet",
                  HTname="HT"
                  )
modules.append(HTCalculator)
DiLeps = LeptonPairCreator(
                  LepCollectionA='Muon', 
                  LepCollectionB='Electron', 
                  LepAmass=0.105,
                  LepBmass=0.000511, 
                  pairName="MuEle", 
                  minLep1Pt=0, 
                  minLep2Pt=0, 
                  minPairPt=0, 
                  minPairMass=50, 
                  maxPairMass=120, 
                  OppCharge=True, 
                  SameCharge=False, 
                  minN=-1
                  )
modules.append(DiLeps)

MTmuon = FunctionWrapper(
      functionName="MT",
      collections=["Muon","MET_pt","MET_phi"],
      createdBranches=["Muon_MT"],
      nCol="nMuon"
)
modules.append(MTmuon)

MTelectron = FunctionWrapper(
      functionName="MT",
      collections=["Electron","MET_pt","MET_phi"],
      createdBranches=["Electron_MT"],
      nCol="nElectron"
)
modules.append(MTelectron)


if not production:
   p = PostProcessor(outputFolder, fnames, postfix=outputName, cut=TriggerCuts,  modules=modules,branchsel = branchsel_in, outputbranchsel = branchsel_out, prefetch = True, longTermCache = True, provenance=True, maxEntries=maxEntries)
else:
   p = PostProcessor(".", inputFiles(),postfix=ouputName, cut=TriggerCuts,  modules=modules,branchsel = branchsel_in, outputbranchsel = branchsel_out, provenance=True, fwkJobReport=True)  

###############RUN here######################
p.run()
print "done"

################################# options #############################
#class PostProcessor:
# outputDir, inputFiles, cut=None, branchsel=None, modules=[],compression="LZMA:9", friend=False, postfix=None, jsonInput=None,noOut=False, justcount=False, provenance=False, haddFileName=None,fwkJobReport=False, histFileName=None, histDirName=None, outputbranchsel=None, maxEntries=None, firstEntry=0, prefetch=False, longTermCache=False

