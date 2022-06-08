#!/usr/bin/env python
# Analyzer to reproduce the selection used in github.com/michaelmackenz/ZEMuAnalysis.git
# See also legacy/LFVAnalyzer.py where this was copied to

from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.LeptonSkimmer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.HTSkimmer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.JetSkimmer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.JetLepCleaner import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.SelectionFilter import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.GenCount import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.GenLepCount import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.GenAnalyzer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.GenZllAnalyzer import *
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
isData    =   sys.argv[2]
year      =   sys.argv[3]

prefetch  = False

# inputFile = [
#     "root://cms-xrd-global.cern.ch//store/user/pellicci/ZEMuAnalysis_2016_8028V1/ZEMuAnalysis_NANOAOD_10218V1/200211_105742/0000/ZEMuAnalysis_pythia8_NANOAOD_2016_1.root",\
#     "root://cms-xrd-global.cern.ch//store/user/pellicci/ZEMuAnalysis_2016_8028V1/ZEMuAnalysis_NANOAOD_10218V1/200211_105742/0000/ZEMuAnalysis_pythia8_NANOAOD_2016_2.root",\
# ]
# inputFile = [
#     "condor/tmp_data/ZEMu_2016_01.root", \
#     "condor/tmp_data/ZEMu_2016_02.root", \
# ]


if isData not in ["data", "MC", "Embedded"]:
   print "Unknown data flag %s" % (isData)
   exit()
   
if year not in ["2016", "2017", "2018"]:
   print "Unknown year %s" % (year)
   exit()
   
#debug configuration options
maxEntries=None #deactivate(use all evts): None
firstEntry=0

# branches to read in / write out
branchsel_in  ="python/postprocessing/run/keep_and_drop_in.txt"
branchsel_out ="python/postprocessing/run/keep_and_drop_out.txt"

# filter out untriggered events or with leading lepton below the trigger threshold
if year == "2016":
   TriggerCuts="((HLT_IsoMu24 || HLT_Mu50) && nMuon > 0) || (HLT_Ele27_WPTight_Gsf && nElectron > 0)"
elif year == "2017":
   TriggerCuts="((HLT_IsoMu27 || HLT_Mu50) && nMuon>0) || (HLT_Ele32_WPTight_Gsf_L1DoubleEG && nElectron>0)"
elif year == "2018":
   TriggerCuts="((HLT_IsoMu24 || HLT_Mu50) && nMuon>0) || (HLT_Ele32_WPTight_Gsf && nElectron>0)"

TriggerCuts = None
print "Trigger cuts:", TriggerCuts

#Base lepton selection
MuonSelection     = lambda l : l.pt>10 and math.fabs(l.eta)<2.2 and l.looseId and l.pfRelIso04_all < 0.5
ElectronSelection = lambda l : l.pt>10 and math.fabs(l.eta)<2.2 and (math.fabs(l.eta + l.deltaEtaSC) < 1.4442 or math.fabs(l.eta + l.deltaEtaSC) > 1.556) and l.mvaFall17V2Iso_WPL
TauSelection      = lambda l : l.pt>20 and math.fabs(l.eta)<2.2 and l.idDeepTau2017v2p1VSmu > 10 and l.idDeepTau2017v2p1VSe > 10 and l.idDeepTau2017v2p1VSjet > 5 and l.idDecayMode

#configure the modules
modules=[]
GenCounter=GenCount()
modules.append(GenCounter)

#lepton selection
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

TauSelector= LeptonSkimmer(
   LepFlavour='Tau',
   Selection=TauSelection,
   Veto=None,
   minNlep=-1,
   maxNlep=-1,
   verbose=False
)
modules.append(TauSelector)

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

#filter events by final state selection
Selection= SelectionFilter(year=year,prev_ids=1,verbose=0)
modules.append(Selection)

#Add additional event info
if not isData == "data":
   ZllBuilder=GenZllAnalyzer(
      variables=['pt','eta','phi','mass','pdgId'],
      motherName='GenZll',
      skip=False,
      verbose=-1
   )
   modules.append(ZllBuilder)

#record number of generator-level primary(-ish) leptons in the event
GenTauCount= GenLepCount(Lepton="Tau")
modules.append(GenTauCount)

GenMuonCount= GenLepCount(Lepton="Muon")
modules.append(GenMuonCount)

GenElectronCount= GenLepCount(Lepton="Electron")
modules.append(GenElectronCount)

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
                prefetch=prefetch, longTermCache=prefetch,
                provenance = True, fwkJobReport = False, jsonInput = jsonFile, maxEntries = maxEntries, firstEntry = firstEntry)

###############RUN here######################
p.run()
print "done"

################################# options #############################
#class PostProcessor:
# outputDir, inputFiles, cut=None, branchsel=None, modules=[],compression="LZMA:9", friend=False, postfix=None, jsonInput=None,noOut=False, justcount=False, provenance=False, haddFileName=None,fwkJobReport=False, histFileName=None, histDirName=None, outputbranchsel=None, maxEntries=None, firstEntry=0, prefetch=False, longTermCache=False

