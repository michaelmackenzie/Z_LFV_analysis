#!/usr/bin/env python
import os
import sys
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.legacy.runSkimModule import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *

inputFile = [ sys.argv[1] ]
# inputFile = [
#     "root://cms-xrd-global.cern.ch//store/user/pellicci/ZEMuAnalysis_2016_8028V1/ZEMuAnalysis_NANOAOD_10218V1/200211_105742/0000/ZEMuAnalysis_pythia8_NANOAOD_2016_1.root",\
#     "root://cms-xrd-global.cern.ch//store/user/pellicci/ZEMuAnalysis_2016_8028V1/ZEMuAnalysis_NANOAOD_10218V1/200211_105742/0000/ZEMuAnalysis_pythia8_NANOAOD_2016_2.root",\
# ]
# inputFile = [
#     "condor/tmp_data/ZEMu_2016_01.root", \
#     "condor/tmp_data/ZEMu_2016_02.root", \
# ]
prefetch = False

isData = False
isEmbedded = False
if sys.argv[2].split('=')[1] == "data":
    isData = True
elif sys.argv[2].split('=')[1] == "Embedded":
    isEmbedded = True
year = sys.argv[3].split('=')[1]
saveZ = False #for saving Drell-Yan (or signal) Z info
if sys.argv[4].split('=')[1] == "True":
    saveZ = True
maxEvents = -1
startEvent = 1
if len(sys.argv) > 5: #additional parameter of max events
    maxEvents = int(sys.argv[5])
    print "Using maximum read events =", maxEvents
if len(sys.argv) > 6: #additional parameter of start event
    startEvent = int(sys.argv[6])
    print "Using initial event =", startEvent
print "LFVAnalyzer using input file", inputFile, "isData", isData, "isEmbedded", isEmbedded, "year", year, "saveZ", saveZ

if year == "2016" :
    jsonFile="json/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt"
elif year == "2017":
    jsonFile="json/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt"
else:
    jsonFile="json/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt"

# p=PostProcessor(".",inputfile,"",modules=[leptonConstr(0)],provenance=True,fwkJobReport=True,outputbranchsel="cmssw_config/keep_and_drop.txt")
if isData or isEmbedded :
    if year == "2016" :
        p=PostProcessor(".",inputFile,None, modules=[leptonConstr(0, maxEvents, startEvent, not isEmbedded, saveZ)],
                        prefetch=prefetch, longTermCache=prefetch,
                        provenance=True,fwkJobReport=True,jsonInput=jsonFile,outputbranchsel="python/legacy/keep_and_drop.txt")
    elif year == "2017" :
        p=PostProcessor(".",inputFile,None, modules=[leptonConstr(1, maxEvents, startEvent, not isEmbedded, saveZ)],
                        prefetch=prefetch, longTermCache=prefetch,
                        provenance=True,fwkJobReport=True,jsonInput=jsonFile,outputbranchsel="python/legacy/keep_and_drop.txt")
    elif year == "2018" :
        p=PostProcessor(".",inputFile,None, modules=[leptonConstr(2, maxEvents, startEvent, not isEmbedded, saveZ)],
                        prefetch=prefetch, longTermCache=prefetch,
                        provenance=True,fwkJobReport=True,jsonInput=jsonFile,outputbranchsel="python/legacy/keep_and_drop.txt")
else :
    if year == "2016" :
        p=PostProcessor(".",inputFile,None, modules=[leptonConstr(0, maxEvents, startEvent, 0, saveZ),puAutoWeight_2016()],
                        prefetch=prefetch, longTermCache=prefetch,
                        provenance=True,fwkJobReport=True,outputbranchsel="python/legacy/keep_and_drop.txt")
    elif year == "2017" :
        p=PostProcessor(".",inputFile,None, modules=[leptonConstr(1, maxEvents, startEvent, 0, saveZ),puAutoWeight_2017()],
                        prefetch=prefetch, longTermCache=prefetch,
                        provenance=True,fwkJobReport=True,outputbranchsel="python/legacy/keep_and_drop.txt")
    elif year == "2018" :
        p=PostProcessor(".",inputFile,None, modules=[leptonConstr(2, maxEvents, startEvent, 0, saveZ),puAutoWeight_2018()],
                        prefetch=prefetch, longTermCache=prefetch,
                        provenance=True,fwkJobReport=True,outputbranchsel="python/legacy/keep_and_drop.txt")

p.run()

print "LFVAnalyzer has finished file", inputFile[0]
