from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import os
import itertools

ROOT.PyConfig.IgnoreCommandLineOptions = True

_rootLeafType2rootBranchType = {
    'UChar_t': 'b', 'Char_t': 'B', 'UInt_t': 'i', 'Int_t': 'I', 'Float_t': 'F',
    'Double_t': 'D', 'ULong64_t': 'l', 'Long64_t': 'L', 'Bool_t': 'O'}


class GenLepCount(Module):
    def __init__(self, Lepton="Muon"):
        self.Lepton=Lepton
        if self.Lepton == "Tau":
            self.lep_id = 15
        elif self.Lepton == "Muon":
            self.lep_id = 13
        elif self.Lepton == "Electron":
            self.lep_id = 11
        else:
            print "GenLepCount: Unknown lepton name %s, defaulting to Tau" % (self.Lepton)
            self.Lepton = "Tau"
            self.lep_id = 15

        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("nGen%s"        % (self.Lepton),'I')
        pass
 

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if not hasattr(event, "nGenPart"): #check if it's data
            self.out.fillBranch("nGen%s" % (self.Lepton), 0)
            return True
        gens = Collection(event, "GenPart")
        ngens = len(gens)
        nGenLep = 0
        motherParticles = [6, 22, 23, 24] #parents of taus considered (top, gamma, Z, W^+-)
        for index in range(ngens):
            if abs(gens[index].pdgId) == self.lep_id : #lepton
                if gens[index].genPartIdxMother > 0:
                    mother_id = abs(gens[gens[index].genPartIdxMother].pdgId)
                    if mother_id == self.lep_id: #lep -> lep + gamma protection
                        continue
                    if mother_id in motherParticles:
                        nGenLep = nGenLep + 1
                if gens[index].genPartIdxMother == 0 : #primary taus
                    nGenLep = nGenLep + 1

        self.out.fillBranch("nGen%s" % (self.Lepton), nGenLep)
        return True
