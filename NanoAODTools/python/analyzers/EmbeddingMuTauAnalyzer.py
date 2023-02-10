#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.GenZllAnalyzer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.EmbeddingEMuStudy import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.LeptonSkimmer import *
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

nargs = len(sys.argv)
if nargs < 4:
   print "At least 3 arguments required: <input file> <data/MC/Embedded> <year>"
   exit()

inputFile = sys.argv[1].split(',') #[ sys.argv[1] ]
isData    = sys.argv[2]
year      = sys.argv[3]
maxEntries= int(sys.argv[4]) if nargs > 4 else None

prefetch  = False

if isData not in ["data", "MC", "Embedded"]:
   print "Unknown data flag %s" % (isData)
   exit()
   
if year not in ["2016", "2017", "2018"]:
   print "Unknown year %s" % (year)
   exit()

if maxEntries != None:
   print "Using maxEntries =", maxEntries

#debug configuration options
firstEntry=0 #0 to start at the first event

# branches to read in / write out
branchsel_in  ="python/postprocessing/run/emu_study_keep_and_drop_in.txt"
branchsel_out ="python/postprocessing/run/emu_study_keep_and_drop_out.txt"

TriggerCuts = None
print "Trigger cuts:", TriggerCuts

#for studying the ID efficiencies
# MuonSelection     = lambda l : l.pt>10 and math.fabs(l.eta)<2.2 and l.mediumId and l.pfRelIso04_all < 0.5
TauSelection      = lambda l : l.pt>20 and math.fabs(l.eta)<2.2 and l.idDeepTau2017v2p1VSmu > 10 and l.idDeepTau2017v2p1VSe > 10 and l.idDeepTau2017v2p1VSjet > -1 and l.idDecayModeNewDMs

#configure the modules
modules=[]

#match reco products to gen-level products
ZllBuilder=GenZllAnalyzer(
   variables=['pt','eta','phi','mass','pdgId'],
   motherName='GenZll',
   skip=False,
   verbose=-1
)
modules.append(ZllBuilder)

#Efficiency study for mutau
MuTauStudy= EmbeddingEMuStudy(year = year, final_state = "mutau")
modules.append(MuTauStudy)

#Lepton ID efficiency studies
# MuonSelector= LeptonSkimmer(
#    LepFlavour='Muon',
#    Selection=MuonSelection,
#    Veto=None,
#    minNlep=-1,
#    maxNlep=-1,
#    verbose=False
# )
# modules.append(MuonSelector)
TauSelector= LeptonSkimmer(
   LepFlavour='Tau',
   Selection=TauSelection,
   Veto=None,
   minNlep=-1,
   maxNlep=-1,
   verbose=False
)
modules.append(TauSelector)

jsonFile = None
if isData != "MC": #data/embedding
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

