#!/usr/bin/env python
from PhysicsTools.NanoAODTools.postprocessing.modules.CUmodules.GenZllAnalyzer import *
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
inputFile = sys.argv[1].split(',')
isData    = sys.argv[2]
year      = sys.argv[3]

inputFile = [ f for f in inputFile if f != '' ]

if isData == "data":
   print "Module not defined for data!"
   exit()
if isData not in ["MC", "Embedded"]:
   print "Unknown sample flag %s" % (isData)
   exit()
   
if year not in ["2016", "2017", "2018"]:
   print "Unknown year %s" % (year)
   exit()

print "Input arguments: files =", inputFile, "isdata =", isData, " year =", year

#debug configuration options
maxEntries=None #deactivate(use all evts): None
firstEntry=0

# branches to read in / write out
branchsel_in  ="python/postprocessing/run/genz_keep_and_drop_in.txt"
branchsel_out ="python/postprocessing/run/genz_keep_and_drop_out.txt"

# no cuts since study (hopefully) unbiased gen-level info
TriggerCuts = None
# TriggerCuts = None
print "Trigger cuts:", TriggerCuts

#configure the modules
modules=[]

#generator info of simulated leptons
ZllBuilder=GenZllAnalyzer(
   variables=['pt','eta','phi','mass','pdgId'],
   motherName='GenZll',
   skip=False,
   verbose=-1
)
modules.append(ZllBuilder)

#configure the json file filtering (if needed)
if isData == "MC":
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

