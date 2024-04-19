from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import os
import itertools

ROOT.PyConfig.IgnoreCommandLineOptions = True

_rootLeafType2rootBranchType = {
    'UChar_t': 'b', 'Char_t': 'B', 'UInt_t': 'i', 'Int_t': 'I', 'Float_t': 'F',
    'Double_t': 'D', 'ULong64_t': 'l', 'Long64_t': 'L', 'Bool_t': 'O'}


class ObjectCounter(Module):
    def __init__(self, Objects, Tag):
        self.Objects = Objects
        self.Tag = Tag
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for Object in self.Objects:
            self.out.branch("n%s%s" % (Object, self.Tag), 'I')
        pass
 

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        for Object in self.Objects:
            nObj = getattr(event, "n%s" % (Object)) if hasattr(event, "n%s" % (Object)) else 0
            self.out.fillBranch("n%s%s" % (Object, self.Tag), nObj)
        return True
