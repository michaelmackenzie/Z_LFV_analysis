#!/usr/bin/env python
from Z_LFV_analysis.NanoAODTools.postprocessing.modules.CUmodules.LeptonSkimmer import *
from Z_LFV_analysis.NanoAODTools.postprocessing.modules.CUmodules.HTSkimmer import *
from Z_LFV_analysis.NanoAODTools.postprocessing.modules.CUmodules.JetSkimmer import *
from Z_LFV_analysis.NanoAODTools.postprocessing.modules.CUmodules.JetLepCleaner import *
from Z_LFV_analysis.NanoAODTools.postprocessing.modules.CUmodules.GenAnalyzer import *
from Z_LFV_analysis.NanoAODTools.postprocessing.modules.CUmodules.GenIdenticalMothersDiscriminator import *
from Z_LFV_analysis.NanoAODTools.postprocessing.modules.CUmodules.GenRecoMatcher import *
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles


from importlib import import_module
import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

#import argparse
from os import listdir
from os.path import isfile, join

#cfg in txt because crab helper is not perfect (to be mild)
production=False
outputFolder="id_Jet" #used only for non-production
build_GenSignalDecay_ZMuE=True
build_GenSignalDecay_ZMuTau=False
build_GenSignalDecay_ZETau=False
maxEntries=None #deactivate(use all evts): None


fnames=[
  #Data
#  "root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v1/130000/02945FF5-75FA-D14B-ADDC-68A0F71E6F5E.root"
  #"root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v1/130000/02E7A5CB-7E72-DD45-A973-BA4114267C73.root"
#  "root:://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v1/130000/E4DA4798-B1EF-0C49-A4C5-B1EE627BDA97.root"
#  "root:://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v1/280000/F0C7CAE9-D602-9D40-B9EE-CCDE7C14D6A5.root"

#Z->tt
#  "root:://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv7/DYJetsToTauTau_ForcedMuEleDecay_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/100000/892D0A20-8B3F-A94F-B168-FA309C3BB3C1.root"

##ttbar
  #"root:://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv7/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/60000/BF63D9D2-AA6F-1948-86E6-ABFEA793C3D2.root"
#  "root:://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv7/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/Nano02Apr2020_102X_upgrade2018_realistic_v21_ext2-v1/60000/D959CE19-AE07-3446-B6AD-B5E08740F18F.root"

  #Z->mue
 'root://cms-xrd-global.cern.ch//store/user/pellicci/ZEMuAnalysis_2016_8028V1/ZEMuAnalysis_NANOAOD_10218V1/200211_105742/0000/ZEMuAnalysis_pythia8_NANOAOD_2016_1.root',\
#     'root://cms-xrd-global.cern.ch//store/user/pellicci/ZEMuAnalysis_2016_8028V1/ZEMuAnalysis_NANOAOD_10218V1/200211_105742/0000/ZEMuAnalysis_pythia8_NANOAOD_2016_2.root',\
#     'root://cms-xrd-global.cern.ch//store/user/pellicci/ZEMuAnalysis_2016_8028V1/ZEMuAnalysis_NANOAOD_10218V1/200211_105742/0000/ZEMuAnalysis_pythia8_NANOAOD_2016_3.root',\
#     'root://cms-xrd-global.cern.ch//store/user/pellicci/ZEMuAnalysis_2016_8028V1/ZEMuAnalysis_NANOAOD_10218V1/200211_105742/0000/ZEMuAnalysis_pythia8_NANOAOD_2016_4.root',\
#     'root://cms-xrd-global.cern.ch//store/user/pellicci/ZEMuAnalysis_2016_8028V1/ZEMuAnalysis_NANOAOD_10218V1/200211_105742/0000/ZEMuAnalysis_pythia8_NANOAOD_2016_5.root',\
#      'root://cms-xrd-global.cern.ch//store/user/pellicci/ZEMuAnalysis_2016_8028V1/ZEMuAnalysis_NANOAOD_10218V1/200211_105742/0000/ZEMuAnalysis_pythia8_NANOAOD_2016_6.root',\
#      'root://cms-xrd-global.cern.ch//store/user/pellicci/ZEMuAnalysis_2016_8028V1/ZEMuAnalysis_NANOAOD_10218V1/200211_105742/0000/ZEMuAnalysis_pythia8_NANOAOD_2016_7.root',\
#      'root://cms-xrd-global.cern.ch//store/user/pellicci/ZEMuAnalysis_2016_8028V1/ZEMuAnalysis_NANOAOD_10218V1/200211_105742/0000/ZEMuAnalysis_pythia8_NANOAOD_2016_8.root',\
#      'root://cms-xrd-global.cern.ch//store/user/pellicci/ZEMuAnalysis_2016_8028V1/ZEMuAnalysis_NANOAOD_10218V1/200211_105742/0000/ZEMuAnalysis_pythia8_NANOAOD_2016_9.root',\
#     'root://cms-xrd-global.cern.ch//store/user/pellicci/ZEMuAnalysis_2016_8028V1/ZEMuAnalysis_NANOAOD_10218V1/200211_105742/0000/ZEMuAnalysis_pythia8_NANOAOD_2016_10.root',\
#  'root://cms-xrd-global.cern.ch//store/user/pellicci/ZEMuAnalysis_2016_8028V1/ZEMuAnalysis_NANOAOD_10218V1/200211_105742/0000/ZEMuAnalysis_pythia8_NANOAOD_2016_11.root',\
#     'root://cms-xrd-global.cern.ch//store/user/pellicci/ZEMuAnalysis_2016_8028V1/ZEMuAnalysis_NANOAOD_10218V1/200211_105742/0000/ZEMuAnalysis_pythia8_NANOAOD_2016_12.root',\
#     'root://cms-xrd-global.cern.ch//store/user/pellicci/ZEMuAnalysis_2016_8028V1/ZEMuAnalysis_NANOAOD_10218V1/200211_105742/0000/ZEMuAnalysis_pythia8_NANOAOD_2016_13.root',\
#     'root://cms-xrd-global.cern.ch//store/user/pellicci/ZEMuAnalysis_2016_8028V1/ZEMuAnalysis_NANOAOD_10218V1/200211_105742/0000/ZEMuAnalysis_pythia8_NANOAOD_2016_14.root',\
#     'root://cms-xrd-global.cern.ch//store/user/pellicci/ZEMuAnalysis_2016_8028V1/ZEMuAnalysis_NANOAOD_10218V1/200211_105742/0000/ZEMuAnalysis_pythia8_NANOAOD_2016_15.root',\
#'root://cms-xrd-global.cern.ch///store/user/pellicci/LFVAnalysis_ZMuTau_2018_10218V1/LFVAnalysis_NANOAOD_10218V1/201014_123454/0000/ZEMuAnalysis_pythia8_NANOAOD_2018_1.root',
#'root://cms-xrd-global.cern.ch///store/user/pellicci/LFVAnalysis_ZMuTau_2018_10218V1/LFVAnalysis_NANOAOD_10218V1/201014_123454/0000/ZEMuAnalysis_pythia8_NANOAOD_2018_2.root',
#'root://cms-xrd-global.cern.ch///store/user/pellicci/LFVAnalysis_ZMuTau_2018_10218V1/LFVAnalysis_NANOAOD_10218V1/201014_123454/0000/ZEMuAnalysis_pythia8_NANOAOD_2018_3.root'

]


# only read the branches in this file - for speed deactivate unescairy stuff
branchsel_in ="keep_and_drop_in.txt"

# only write the branches in this file in ADDITION of what is produce by module
branchsel_out ="keep_and_drop_out.txt"
#TriggerCuts="HL"
TriggerCuts="(HLT_IsoMu24 || HLT_Ele27_WPTight_Gsf) && nMuon>0 && nElectron>0"
#TriggerCuts="(HLT_Mu27_Ele37_CaloIdL_MW || HLT_Mu37_Ele27_CaloIdL_MW || HLT_IsoMu24) && nMuon>0 && nElectron>0"
#TriggerCuts=""
#MuonSelection = lambda l : l.pt>10 and l.mediumPromptId==True and abs(l.eta)<2.4 and l.pfRelIso03_all<0.3 and  abs(l.dz)<1.0 and abs(l.dxy)<0.5
#TightMuonSelection = lambda l : l.pt>10 and l.mediumPromptId==True and abs(l.eta)<2.4 and l.pfRelIso03_all<0.3 and  abs(l.dz)<1.0 and abs(l.dxy)<0.5
#ElectronSelection = lambda l : l.pt>10 and abs(l.eta)<2.4 and l.pfRelIso03_all<0.3 and abs(l.dz)<1.25 and abs(l.dxy)<0.5  
MuonSelection = lambda l : l.pt>5 and abs(l.eta)<2.4 and l.mediumId==True
ElectronSelection = lambda l : l.pt>5 and abs(l.eta)<2.5 and l.mvaFall17V2noIso_WP90==True
TauSelection = lambda l : l.pt>5 and abs(l.eta)<2.4 and l.idAntiMu>0
JetSelection = lambda l : l.pt>20.0 and abs(l.eta)<3.0 and l.puId>4 and l.jetId>1
 


modules=[]

ZttBuilder=GenAnalyzer(
                  decay='23->15,-15',
                  motherName='GenZTauTau',
                  daughterNames=['GenTau','GenAntiTau'],
                  variables=['pt','eta','phi','mass','pdgId'],
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
                  variables=['pt','eta','phi','mass','pdgId'],
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
                  variables=['pt','eta','phi','mass','pdgId'],
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
                  variables=['pt','eta','phi','mass','pdgId'],
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
looseHTCalculator= HTSkimmer(
                  minJetPt=20,
                  minJetEta=4.7,
                  minJetPUid=-1,
                  minHT=-1,
                  collection="Jet",
                  HTname="looseHT"
                  )
modules.append(looseHTCalculator)
looseCntrHTCalculator= HTSkimmer(
                  minJetPt=20,
                  minJetEta=3.0,
                  minJetPUid=-1,
                  minHT=-1,
                  collection="Jet",
                  HTname="looseCntrHT"
                  )
modules.append(looseCntrHTCalculator)

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


if not production:
   p = PostProcessor(outputFolder, fnames, cut=TriggerCuts,  modules=modules,branchsel = branchsel_in, outputbranchsel = branchsel_out,
                     prefetch = True, longTermCache = True, provenance=True, maxEntries=maxEntries)
else:
   p = PostProcessor(".", inputFiles(), cut=TriggerCuts,  modules=modules,branchsel = branchsel_in, outputbranchsel = branchsel_out,
                     provenance=True, fwkJobReport=True)  

###############RUN here######################
p.run()
print "done"

################################# options #############################
#class PostProcessor:
# outputDir, inputFiles, cut=None, branchsel=None, modules=[],compression="LZMA:9", friend=False, postfix=None, jsonInput=None,noOut=False, justcount=False, provenance=False, haddFileName=None,fwkJobReport=False, histFileName=None, histDirName=None, outputbranchsel=None, maxEntries=None, firstEntry=0, prefetch=False, longTermCache=False

