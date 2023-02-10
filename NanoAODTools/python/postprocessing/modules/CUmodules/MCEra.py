from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import os
import itertools

ROOT.PyConfig.IgnoreCommandLineOptions = True

_rootLeafType2rootBranchType = {
    'UChar_t': 'b', 'Char_t': 'B', 'UInt_t': 'i', 'Int_t': 'I', 'Float_t': 'F',
    'Double_t': 'D', 'ULong64_t': 'l', 'Long64_t': 'L', 'Bool_t': 'O'}


class MCEra(Module):
    def __init__(self, lumis = [], seed = 90):
        self.rnd = ROOT.TRandom3(seed)
        self.fractions = []
        tot_lumi = sum(lumis)
        seen = 0.
        for lumi in lumis:
            seen += lumi
            self.fractions.append(seen / tot_lumi)
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch('MCEra', 'I')
        pass
 

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        mcera = 0 #default to first era
        val = self.rnd.Uniform()
        #find which era this random number corresponds to
        for fraction in self.fractions:
            if val < fraction: break
            mcera += 1
        self.out.fillBranch('MCEra', mcera)
        return True
