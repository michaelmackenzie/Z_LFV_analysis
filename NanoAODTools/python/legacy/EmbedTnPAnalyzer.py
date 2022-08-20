#!/usr/bin/env python
import os
import sys
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 
from PhysicsTools.NanoAODTools.legacy.embedTnPModule import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *

inputFile = [ sys.argv[1] ]
isData = False
isEmbedded = False
if sys.argv[2].split('=')[1] == "data":
    isData = True
elif sys.argv[2].split('=')[1] == "Embedded":
    isEmbedded = True
year = sys.argv[3].split('=')[1]
maxEvents = -1
startEvent = 1
if len(sys.argv) > 4: #additional parameter of max events
    maxEvents = int(sys.argv[4])
    print "Using maximum read events =", maxEvents
if len(sys.argv) > 5: #additional parameter of start event
    startEvent = int(sys.argv[5])
    print "Using initial event =", startEvent
print "EmbedTnPAnalyzer using input file", inputFile, "isData", isData, "isEmbedded", isEmbedded, "year", year

if year == "2016" :
    jsonFile="test/json/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt"
elif year == "2017":
    jsonFile="test/json/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt"
else:
    jsonFile="test/json/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt"

# p=PostProcessor(".",inputfile,"",modules=[leptonConstr(0)],provenance=True,fwkJobReport=True,outputbranchsel="cmssw_config/keep_and_drop.txt")
if isData or isEmbedded:
    if year == "2016" :
        p=PostProcessor(".",inputFile,None, modules=[leptonConstr(0, maxEvents, startEvent, not isEmbedded)],provenance=True,fwkJobReport=True,jsonInput=jsonFile,outputbranchsel="test/cmssw_config/tnp_keep_and_drop.txt")
    elif year == "2017" :
        p=PostProcessor(".",inputFile,None, modules=[leptonConstr(1, maxEvents, startEvent, not isEmbedded)],provenance=True,fwkJobReport=True,jsonInput=jsonFile,outputbranchsel="test/cmssw_config/tnp_keep_and_drop.txt")
    elif year == "2018" :
        p=PostProcessor(".",inputFile,None, modules=[leptonConstr(2, maxEvents, startEvent, not isEmbedded)],provenance=True,fwkJobReport=True,jsonInput=jsonFile,outputbranchsel="test/cmssw_config/tnp_keep_and_drop.txt")
else :
    if year == "2016" :
        p=PostProcessor(".",inputFile,None, modules=[leptonConstr(0, maxEvents, startEvent, 0),puAutoWeight_2016()],provenance=True,fwkJobReport=True,outputbranchsel="test/cmssw_config/tnp_keep_and_drop.txt")
    elif year == "2017" :
        p=PostProcessor(".",inputFile,None, modules=[leptonConstr(1, maxEvents, startEvent, 0),puAutoWeight_2017()],provenance=True,fwkJobReport=True,outputbranchsel="test/cmssw_config/tnp_keep_and_drop.txt")
    elif year == "2018" :
        p=PostProcessor(".",inputFile,None, modules=[leptonConstr(2, maxEvents, startEvent, 0),puAutoWeight_2018()],provenance=True,fwkJobReport=True,outputbranchsel="test/cmssw_config/tnp_keep_and_drop.txt")

p.run()

print "EmbedTnPAnalyzer has finished file", inputFile[0]
