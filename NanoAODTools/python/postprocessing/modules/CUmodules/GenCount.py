from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import os
import itertools

ROOT.PyConfig.IgnoreCommandLineOptions = True

_rootLeafType2rootBranchType = {
    'UChar_t': 'b', 'Char_t': 'B', 'UInt_t': 'i', 'Int_t': 'I', 'Float_t': 'F',
    'Double_t': 'D', 'ULong64_t': 'l', 'Long64_t': 'L', 'Bool_t': 'O'}


class GenCount(Module):
    def __init__(self):
        self.seen = 0
        self.negative = 0
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
 

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        print "GenCount: Saw %i events, %i negative events" % (self.seen, self.negative)
        #store the normalization in an output histogram file
        outputFile.cd()
        h = ROOT.TH1D("events", "events", 10, 1, 11)
        h.Fill(1.5, self.seen)
        h.Fill(10.5, self.negative)
        h.Write()
        pass


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        self.seen = self.seen + 1
        if hasattr(event, "genWeight") and event.genWeight < 0:
            self.negative = self.negative + 1
        return True
