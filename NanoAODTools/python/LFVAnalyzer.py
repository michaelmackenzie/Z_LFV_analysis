#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.LeptonSkimmer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.HTSkimmer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.JetSkimmer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.JetLepCleaner import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.SelectionFilter import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.GenCount import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.GenLepCount import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.GenAnalyzer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.GenZllAnalyzer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.GenIdenticalMothersDiscriminator import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.GenRecoMatcher import *
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *


from importlib import import_module
import os
import sys
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

#read in command line arguments
#Example: python <Analyzer> <input file> <data/MC/Embedded> <year>
inputFile = [ sys.argv[1] ]
isData    = sys.argv[2]
year      = sys.argv[3]

if isData not in ["data", "MC", "Embedded"]:
   print "Unknown data flag %s" % (isData)
   exit()
   
if year not in ["2016", "2017", "2018"]:
   print "Unknown year %s" % (year)
   exit()
   
#Configuration options
maxEntries=None #deactivate(use all evts): None

# branches to read in / write out
branchsel_in  ="python/postprocessing/run/keep_and_drop_in.txt"
branchsel_out ="python/postprocessing/run/keep_and_drop_out.txt"

# filter out untriggered events or with leading lepton below the trigger threshold
if year == "2016":
   TriggerCuts="(HLT_IsoMu24 && nMuon>0 && Muon_pt[0] > 24) || (HLT_Ele27_WPTight_Gsf && nElectron>0 && Electron_pt[0] > 27)"
elif year == "2017":
   TriggerCuts="(HLT_IsoMu27 && nMuon>0 && Muon_pt[0] > 27) || (HLT_Ele32_WPTight_Gsf_L1DoubleEG && nElectron>0 && Electron_pt[0] > 32)"
elif year == "2018":
   TriggerCuts="(HLT_IsoMu24 && nMuon>0 && Muon_pt[0] > 24) || (HLT_Ele32_WPTight_Gsf && nElectron>0 && Electron_pt[0] > 32)"

#Base lepton selection
MuonSelection     = lambda l : l.pt>10 and math.fabs(l.eta)<2.4 and l.mediumId==True
ElectronSelection = lambda l : l.pt>10 and math.fabs(l.eta)<2.5 and l.mvaFall17V2noIso_WP90==True
TauSelection      = lambda l : l.pt>20 and math.fabs(l.eta)<2.3 and l.idDeepTau2017v2p1VSe > 10 and l.idDeepTau2017v2p1VSe > 10 and l.idDeepTau2017v2p1VSjet > 5 and l.idDecayMode
JetSelection      = lambda l : l.pt>20 and math.fabs(l.eta)<3.0 and l.puId>-1 and l.jetId>1 

#configure the modules
modules=[]
GenCounter=GenCount()
modules.append(GenCounter)

ZllBuilder=GenZllAnalyzer(
   variables=['pt','eta','phi','mass','pdgId'],
   motherName='GenZll',
   skip=False,
   verbose=-1
)
modules.append(ZllBuilder)

# RecoElectronMatcher=GenRecoMatcher(
#    genParticles=['GenElectron'],
#    recoCollections=['Electron'],
#    maxDR=0.1
# )
# modules.append(RecoElectronMatcher)
# RecoMuonMatcher=GenRecoMatcher(
#    genParticles=['GenMuon'],
#    recoCollections=['Muon'],
#    maxDR=0.1
# )
# modules.append(RecoMuonMatcher)


# TauToEBuilder=GenAnalyzer(
#    decay='15->11,-12,16',
#    motherName='GenTauToE',
#    daughterNames=['GenElectron','GenNeuE','GenNeuTau'],
#    variables=['pt','eta','phi','pdgId'],
#    grandmother="GenTau_Idx",
#    conjugate=True,
#    mother_has_antipart=True,
#    daughter_has_antipart=[True,True,True],
#    skip=False,
# )
# modules.append(TauToEBuilder)
# TauToMuBuilder=GenAnalyzer(
#    decay='15->13,-14,16',
#    motherName='GenTauToMuon',
#    daughterNames=['GenMuon','GenNeuMu','GenNeuTau'],
#    variables=['pt','eta','phi','pdgId'],
#    grandmother="GenTau_Idx",
#    conjugate=True,
#    mother_has_antipart=True,
#    daughter_has_antipart=[True,True,True],
#    skip=False,
# )
# modules.append(TauToMuBuilder)

MuonSelector= LeptonSkimmer(
   LepFlavour='Muon',
   Selection=MuonSelection,
   Veto=None,
   minNlep=-1,
   maxNlep=2,
   verbose=False
)
modules.append(MuonSelector)
ElectronSelector= LeptonSkimmer(
   LepFlavour='Electron',
   Selection=ElectronSelection,
   Veto=None,
   minNlep=-1,
   maxNlep=2,
   verbose=False
)
modules.append(ElectronSelector)
TauSelector= LeptonSkimmer(
   LepFlavour='Tau',
   Selection=TauSelection,
   Veto=None,
   minNlep=-1,
   maxNlep=-1,
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

#filter events by final state selection
Selection= SelectionFilter(verbose=0)
modules.append(Selection)

#record number of generator-level primary(-ish) leptons in the event
GenTauCount= GenLepCount(Lepton="Tau")
modules.append(GenTauCount)

GenMuonCount= GenLepCount(Lepton="Muon")
modules.append(GenMuonCount)

GenElectronCount= GenLepCount(Lepton="Electron")
modules.append(GenElectronCount)

#configure the pileup module and the json file filtering
if isData == "MC":
   # if year == "2016":
   #    modules.append(puAutoWeight_2016())
   # elif year == "2017":
   #    modules.append(puAutoWeight_2017())
   # elif year == "2018":
   #    modules.append(puAutoWeight_2018())
   jsonFile=None
else:
   if year == "2016" :
      jsonFile="test/json/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt"
   elif year == "2017":
      jsonFile="test/json/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt"
   else:
      jsonFile="test/json/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt"

p=PostProcessor(".",inputFile,cut = TriggerCuts, modules = modules,branchsel = branchsel_in, outputbranchsel = branchsel_out,
                provenance=True,fwkJobReport=True,jsonInput=jsonFile)

###############RUN here######################
p.run()
print "done"

################################# options #############################
#class PostProcessor:
# outputDir, inputFiles, cut=None, branchsel=None, modules=[],compression="LZMA:9", friend=False, postfix=None, jsonInput=None,noOut=False, justcount=False, provenance=False, haddFileName=None,fwkJobReport=False, histFileName=None, histDirName=None, outputbranchsel=None, maxEntries=None, firstEntry=0, prefetch=False, longTermCache=False

