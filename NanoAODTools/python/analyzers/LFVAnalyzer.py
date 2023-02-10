#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.LeptonSkimmer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.HTSkimmer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.JetSkimmer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.JetLepCleaner import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.JetPUIDWeight import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.ZpTWeight import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.SignalpTWeight import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.MCEra import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.LeptonSF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.EmbeddingUnfolding import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.SelectionFilter import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.GenCount import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.GenLepCount import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.GenAnalyzer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.GenZllAnalyzer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.GenRecoMatcher import *
# from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.TriggerAnalyzer import *
# from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.LeptonPairCreator import *
# from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.FunctionWrapper import *
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *


from importlib import import_module
import os
import sys
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

#read in command line arguments
#Example: python <Analyzer> <input file> <data/MC/Embedded> <year>

nargs = len(sys.argv)
if nargs < 4 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
   print "At least 3 arguments required: <input file> <data/MC/Embedded> <year> [optional Max Entries, -1 for all] [optional Start Entry]"
   exit()

inputFile = sys.argv[1].split(',') #[ sys.argv[1] ]
isData    =   sys.argv[2]
year      =   sys.argv[3]
#debug configuration options
maxEntries= int(sys.argv[4]) if nargs > 4 else None
firstEntry= int(sys.argv[5]) if nargs > 5 else 0
if maxEntries < 0: maxEntries = None


#Whether or not to prefetch the file
prefetch  = False

if isData not in ["data", "MC", "Embedded"]:
   print "Unknown data flag %s" % (isData)
   print "Defined flags are: data, MC, and Embedded"
   exit()
   
if year not in ["2016", "2017", "2018"]:
   print "Unknown year %s" % (year)
   print "Defined years are: 2016, 2017, and 2018"
   exit()
   

# branches to read in / write out
branchsel_in  ="python/postprocessing/run/keep_and_drop_in.txt"
branchsel_out ="python/postprocessing/run/keep_and_drop_out.txt"

# filter out untriggered events or with leading lepton below the trigger threshold
if year == "2016":
   TriggerCuts="((HLT_IsoMu24 && nMuon > 0) || (HLT_Ele27_WPTight_Gsf && nElectron > 0))"
elif year == "2017":
   TriggerCuts="(HLT_IsoMu27 && nMuon > 0) || (HLT_Ele32_WPTight_Gsf_L1DoubleEG && nElectron > 0)"
elif year == "2018":
   TriggerCuts="(HLT_IsoMu24 && nMuon > 0) || (HLT_Ele32_WPTight_Gsf && nElectron > 0)"

# TriggerCuts = None
print "Trigger cuts:", TriggerCuts

# Jet ID parameters
jet_pu_id = 6
jet_id = 6 # 7 = tight lep veto in 2016, 6 in 2017/2018, so >=6 for either

#Base lepton/jet selection
MuonSelection     = lambda l : l.pt>10 and math.fabs(l.eta)<2.4 and l.mediumId and l.pfRelIso04_all < 0.5
ElectronSelection = lambda l : l.pt>10 and math.fabs(l.eta)<2.5 and l.mvaFall17V2noIso_WP90 and l.pfRelIso03_all < 0.5
TauSelection      = lambda l : l.pt>20 and math.fabs(l.eta)<2.3 and l.idDeepTau2017v2p1VSmu > 10 and l.idDeepTau2017v2p1VSe > 10 and l.idDeepTau2017v2p1VSjet > 5 and l.idDecayModeNewDMs
JetSelection      = lambda l : l.pt>20 and math.fabs(l.eta)<3.0 and (l.pt >= 50. or l.puId>=jet_pu_id) and l.jetId>=jet_id

#Loose light lepton selection, to remove overlap with taus
LooseMuonSelection     = lambda l : l.pt>10 and math.fabs(l.eta)<2.4 and l.looseId and l.pfRelIso04_all < 0.5
LooseElectronSelection = lambda l : l.pt>10 and math.fabs(l.eta)<2.5 and l.mvaFall17V2noIso_WPL and l.pfRelIso03_all < 0.5
#Loose jet selection, to calculate PU ID weight
LooseJetSelection      = lambda l : l.pt>20 and math.fabs(l.eta)<3.0 and (l.pt >= 50. or l.puId>-1) and l.jetId>=jet_id

#Event selection cuts
MaxMass   = 175 #-1 = no cut
MinMass   =  35 #wider window to estimate event migration systematic uncertainties
MinDeltaR = 0.3 # delta R between the leptons

#configure the modules
modules=[]
GenCounter=GenCount()
modules.append(GenCounter)

#Randomly assign a data era to MC
if isData == "MC":
   if year == "2016":
      lumis = [19.72, 16.14]
   elif year == "2018":
      lumis = [27.66, 31.93]
   else: #don't split 2017 for now
      lumis = []
   MCera = MCEra(lumis = lumis)
   modules.append(MCera)
   
#prefire probability, before jet/photon/electron collection is skimmed
if isData == "MC": #only do on MC, 2016 and 2017
   if year == "2016":
      PrefireCorr = PrefCorr(jetroot="L1prefiring_jetpt_2016BtoH.root",
                             jetmapname="L1prefiring_jetpt_2016BtoH",
                             photonroot="L1prefiring_photonpt_2016BtoH.root",
                             photonmapname="L1prefiring_photonpt_2016BtoH"
      )
      modules.append(PrefireCorr)
   elif year == "2017":
      PrefireCorr = PrefCorr(jetroot="L1prefiring_jetpt_2017BtoF.root",
                             jetmapname="L1prefiring_jetpt_2017BtoF",
                             photonroot="L1prefiring_photonpt_2017BtoF.root",
                             photonmapname="L1prefiring_photonpt_2017BtoF"
      )
      modules.append(PrefireCorr)      
   

#loose light lepton selection
LooseMuonSelector= LeptonSkimmer(
   LepFlavour='Muon',
   Selection=LooseMuonSelection,
   Veto=None,
   minNlep=-1,
   maxNlep=-1,
   verbose=False
)
modules.append(LooseMuonSelector)
LooseElectronSelector= LeptonSkimmer(
   LepFlavour='Electron',
   Selection=LooseElectronSelection,
   Veto=None,
   minNlep=-1,
   maxNlep=-1,
   verbose=False
)
modules.append(LooseElectronSelector)

#tau selection
TauSelector= LeptonSkimmer(
   LepFlavour='Tau',
   Selection=TauSelection,
   Veto=None,
   minNlep=-1,
   maxNlep=-1,
   verbose=False
)
modules.append(TauSelector)

#remove taus overlapping leptons
TauMuonCleaner=JetLepCleaner( 
   Lepton='Muon',
   Jet='Tau',
   dRJet=0.3,
   RemoveOverlappingJets=True, 
   RemoveOverlappingLeptons=False
)
modules.append(TauMuonCleaner)   

TauElectronCleaner=JetLepCleaner(
   Lepton='Electron',
   Jet='Tau',
   dRJet=0.3,
   RemoveOverlappingJets=True, 
   RemoveOverlappingLeptons=False
)
modules.append(TauElectronCleaner)

#tigher muon/electron selection
MuonSelector= LeptonSkimmer(
   LepFlavour='Muon',
   Selection=MuonSelection,
   Veto=None,
   minNlep=-1,
   maxNlep=-1,
   verbose=False
)
modules.append(MuonSelector)
ElectronSelector= LeptonSkimmer(
   LepFlavour='Electron',
   Selection=ElectronSelection,
   Veto=None,
   minNlep=-1,
   maxNlep=-1,
   verbose=False
)
modules.append(ElectronSelector)

# TriggerSelector = TriggerAnalyzer(
#                    particlePdgId=13,
#                    triggerBits=[1,10],
#                    branchNames=["IsoMu24","Mu50"],
#                    recoCollection="Muon",
#                    maxDR=0.03,
#                    maxRelDpt=10.
                  
#                    )
# modules.append(TriggerSelector)

#filter events by final state selection
Selection= SelectionFilter(year=year,
                           min_mass = MinMass,
                           max_mass = MaxMass,
                           min_dr = MinDeltaR,
                           verbose=0)
modules.append(Selection)

# Rochester corrections for muons
if year == "2016":
   modules.append(muonScaleRes2016())
elif year == "2017":
   modules.append(muonScaleRes2017())
elif year == "2018":
   modules.append(muonScaleRes2018())

# # JET MET corrections, before jet cleaning is applied
# #FIXME: Get correct run period for Data/Embedding
# jmeCorrections = createJMECorrector(isData == "MC", year, "B", "Total", True, "AK4PFchs", False)
# modules.append(jmeCorrections())

# JET MET uncertainties, before jet cleaning is applied
if isData == "MC": #FIXME: Can this be done with PuppiMET?
   if year == "2016":
      modules.append(jetmetUncertainties2016())
   elif year == "2017":
      modules.append(jetmetUncertainties2017())
   elif year == "2018":
      modules.append(jetmetUncertainties2018())

#Add additional object cleaning

#First skim without Jet PU ID, calculate PU ID weight, then remove those that fail PU ID
#FIXME: Add each year b-tag WP cuts
if year == "2016":
   btagWPs = [0.2217, 0.6321, 0.8953]
elif year == "2017":
   btagWPs = [0.1522, 0.4941, 0.8001]
elif year == "2018":
   btagWPs = [0.1241, 0.4184, 0.7527]

LooseJetSelector=JetSkimmer( 
   BtagWPs=[], 
   nGoodJetMin=-1, 
   nBJetMax=-1, 
   Selection=LooseJetSelection,
   Veto=None
)
modules.append(LooseJetSelector)

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

JetTauCleaner=JetLepCleaner( 
   Lepton='Tau',
   Jet='Jet',
   dRJet=0.3,
   RemoveOverlappingJets=True, 
   RemoveOverlappingLeptons=False
)
modules.append(JetTauCleaner)   

jetPUIDWeight=JetPUIDWeight(year = year)
modules.append(jetPUIDWeight)

JetSelector=JetSkimmer( 
   BtagWPs=btagWPs, 
   nGoodJetMin=-1, 
   nBJetMax=-1, 
   Selection=JetSelection,
   Veto=None
)
modules.append(JetSelector)

HTCalculator= HTSkimmer(
   minJetPt=20,
   minJetEta=3.0, #FIXME: Should be max jet eta I believe
   minJetPUid=jet_pu_id,
   minHT=-1,
   collection="Jet",
   HTname="HT"
)
modules.append(HTCalculator)

if isData == "MC": #only for MC
   BTagScale= btagSFProducer(era = ('Legacy2016' if year == "2016" else year), algo = 'deepcsv', selectedWPs=['L','T'])
   modules.append(BTagScale)

if not isData == "data":
   ZllBuilder=GenZllAnalyzer(
      variables=['pt','eta','phi','mass','pdgId'],
      motherName='GenZll',
      skip=False,
      verbose=-1
   )
   modules.append(ZllBuilder)

   ZptCorrection=ZpTWeight(year = year, branch = "GenZll")
   modules.append(ZptCorrection)

   SignalptCorrection=SignalpTWeight(year = year, branch = "GenZll")
   modules.append(SignalptCorrection)

   MuonIDWeight=LeptonSF(year = year, Lepton = 'Muon', Correction = 'ID', working_point = 'Medium', Embed = isData == 'Embedded')
   modules.append(MuonIDWeight)

   #Iso ID working point is fixed to Tight, working point here refers to Muon ID working point
   MuonIsoIDWeight=LeptonSF(year = year, Lepton = 'Muon', Correction = 'IsoID', working_point = 'Medium', Embed = isData == 'Embedded')
   modules.append(MuonIsoIDWeight)

   ElectronIDWeight=LeptonSF(year = year, Lepton = 'Electron', Correction = 'ID', working_point = 'Medium', Embed = isData == 'Embedded')
   modules.append(ElectronIDWeight)

   #Iso ID working point is fixed to Tight, working point here refers to WP90 ID
   ElectronIsoIDWeight=LeptonSF(year = year, Lepton = 'Electron', Correction = 'IsoID', working_point = 'Medium', Embed = isData == 'Embedded')
   modules.append(ElectronIsoIDWeight)

   ElectronRecoIDWeight=LeptonSF(year = year,  Lepton = 'Electron', Correction = 'RecoID', working_point = 'Medium', Embed = isData == 'Embedded')
   modules.append(ElectronRecoIDWeight)

   if isData == 'Embedded':
      EmbeddingWeight=EmbeddingUnfolding(year = year)
      modules.append(EmbeddingWeight)

   # RecoElectronMatcher=GenRecoMatcher(
   #                genParticles=['GenElectron'],
   #                recoCollections=['Electron'],
   #                maxDR=0.1
   #                )
   # modules.append(RecoElectronMatcher)
   # RecoMuonMatcher=GenRecoMatcher(
   #                genParticles=['GenMuon'],
   #                recoCollections=['Muon'],
   #                maxDR=0.1
   #                )
   # modules.append(RecoMuonMatcher)

#record number of generator-level primary(-ish) leptons in the event
GenTauCount= GenLepCount(Lepton="Tau")
modules.append(GenTauCount)

GenMuonCount= GenLepCount(Lepton="Muon")
modules.append(GenMuonCount)

GenElectronCount= GenLepCount(Lepton="Electron")
modules.append(GenElectronCount)

## FIXME: add back gen-reco matching
# if not isData == "data":
#    TauToEBuilder=GenAnalyzer(
#       decay='15->11,-12,16',
#       motherName='GenTauToE',
#       daughterNames=['GenTauElectron','GenNeuE','GenNeuTau'],
#       variables=['pt','eta','phi','pdgId'],
#       grandmother="GenTau_Idx",
#       conjugate=True,
#       mother_has_antipart=True,
#       daughter_has_antipart=[True,True,True],
#       skip=False,
#    )
#    modules.append(TauToEBuilder)
#    TauToMuBuilder=GenAnalyzer(
#       decay='15->13,-14,16',
#       motherName='GenTauToMuon',
#       daughterNames=['GenTauMuon','GenNeuMu','GenNeuTau'],
#       variables=['pt','eta','phi','pdgId'],
#       grandmother="GenTau_Idx",
#       conjugate=True,
#       mother_has_antipart=True,
#       daughter_has_antipart=[True,True,True],
#       skip=False,
#    )
#    modules.append(TauToMuBuilder)




#configure the pileup module and the json file filtering
if isData == "MC":
   if year == "2016":
      modules.append(puAutoWeight_2016())
   elif year == "2017":
      modules.append(puAutoWeight_2017())
   elif year == "2018":
      modules.append(puAutoWeight_2018())
   jsonFile=None
else: #data/embedding
   if year == "2016" :
      jsonFile="json/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt"
   elif year == "2017":
      jsonFile="json/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt"
   else:
      jsonFile="json/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt"

p=PostProcessor(".", inputFile, cut = TriggerCuts, modules = modules, branchsel = branchsel_in, outputbranchsel = branchsel_out,
                provenance = True, fwkJobReport = True, jsonInput = jsonFile, maxEntries = maxEntries, firstEntry = firstEntry)

###############RUN here######################
p.run()
print "done"

################################# options #############################
#class PostProcessor:
# outputDir, inputFiles, cut=None, branchsel=None, modules=[],compression="LZMA:9", friend=False, postfix=None, jsonInput=None,noOut=False, justcount=False, provenance=False, haddFileName=None,fwkJobReport=False, histFileName=None, histDirName=None, outputbranchsel=None, maxEntries=None, firstEntry=0, prefetch=False, longTermCache=False

