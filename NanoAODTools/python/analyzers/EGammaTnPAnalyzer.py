#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.LeptonSkimmer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.EGammaTnPFilter import *
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *


from importlib import import_module
import os
import sys
import math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

#read in command line arguments
#Example: python <Analyzer> <input file> <year>
inputFile = [ sys.argv[1] ]
isData    =   sys.argv[2]
year      =   sys.argv[3]
   
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
branchsel_in  ="python/postprocessing/run/embed_tnp_keep_and_drop_in.txt"
branchsel_out ="python/postprocessing/run/embed_tnp_keep_and_drop_out.txt"

# filter out untriggered events and events with less than 2 electrons
if year == "2016":
   TriggerCuts="HLT_Ele27_WPTight_Gsf && nElectron > 1"
elif year == "2017":
   TriggerCuts="HLT_Ele32_WPTight_Gsf_L1DoubleEG && nElectron > 1"
elif year == "2018":
   TriggerCuts="HLT_Ele32_WPTight_Gsf && nElectron > 1"

# TriggerCuts = None
print "Trigger cuts:", TriggerCuts

#Base lepton selection
ElectronSelection = lambda l : l.pt>25 and math.fabs(l.eta)<2.5 and l.mvaFall17V2noIso_WP90 and l.pfRelIso03_all < 0.15

#configure the modules
modules=[]

ElectronSelector= LeptonSkimmer(
   LepFlavour='Electron',
   Selection=ElectronSelection,
   Veto=None,
   minNlep=2,
   maxNlep=2,
   verbose=False
)
modules.append(ElectronSelector)

#filter events by final state selection
Selection= EGammaTnPFilter(year=year,verbose=0)
modules.append(Selection)


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

