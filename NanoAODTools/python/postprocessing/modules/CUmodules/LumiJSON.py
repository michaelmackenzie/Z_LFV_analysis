from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import os
import itertools

ROOT.PyConfig.IgnoreCommandLineOptions = True

_rootLeafType2rootBranchType = {
    'UChar_t': 'b', 'Char_t': 'B', 'UInt_t': 'i', 'Int_t': 'I', 'Float_t': 'F',
    'Double_t': 'D', 'ULong64_t': 'l', 'Long64_t': 'L', 'Bool_t': 'O'}


class LumiJSON(Module):
    def __init__(self):
        self.lumi_map = dict()
        self.seen = 0
        self.lumis = 0
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
 
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        print "LumiJSON: Saw %i events, %i lumis" % (self.seen, self.lumis)
        self.write_lumis()
        pass

    def write_lumis(self):
        f = open('file_lumis_JSON.txt', 'w')
        f.write('{\n')
        runs = self.lumi_map.keys()
        runs.sort()
        for index,run in enumerate(runs):
            lumi_list = self.lumi_map[run]
            lumi_list.sort()
            f.write("  \"%i\": [" % (run))
            prev_lumi = -99
            nlumis = 0
            for lumi in lumi_list:
                if prev_lumi == lumi - 1: # sequential lumis
                    nlumis = nlumis + 1
                elif prev_lumi > -1: #end of a lumi sequence/entry
                    f.write(", %i], [%i" % (prev_lumi, lumi))
                    nlumis = 1
                else: #first lumi, so none to close
                    f.write("[%i" % (lumi))
                    nlumis = 1
                prev_lumi = lumi
            #close the last line
            if index < len(runs) - 1:
                f.write(", %i]],\n" % (prev_lumi))
            else:
                f.write(", %i]]\n" % (prev_lumi))
        #close the run list
        f.write("}")
        f.close()

    def add_lumi(self, run, lumi):
        if not run in self.lumi_map:
            lumi_list = [lumi]
            self.lumi_map[run] = lumi_list
            return True
        if lumi in self.lumi_map[run]:
            return False
        self.lumi_map[run].append(lumi)
        return True
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        self.seen = self.seen + 1
        if self.add_lumi(event.run, event.luminosityBlock):
            self.lumis = self.lumis + 1

        return True
