from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import os
import numpy as np
import itertools
from PhysicsTools.HeppyCore.utils.deltar import deltaR

ROOT.PyConfig.IgnoreCommandLineOptions = True

_rootLeafType2rootBranchType = {
    'UChar_t': 'b',
    'Char_t': 'B',
    'UInt_t': 'i',
    'Int_t': 'I',
    'Float_t': 'F',
    'Double_t': 'D',
    'ULong64_t': 'l',
    'Long64_t': 'L',
    'Bool_t': 'O'
}


class JetLepCleaner(Module):
    def __init__(self, Lepton, Jet, BJet, dRBJet, dRJet, RemoveFailingObjects):
        self.Lepton=Lepton,
        self.Jet=Jet,
        self.BJet=BJet,
        self.dRBJet=dRBJet,
        self.dRJet=dRJet,
        self.RemoveFailingObjects=RemoveFailingObjects,
        self.branchType = {}
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        _brlist_out = wrappedOutputTree._tree.GetListOfBranches()
        branches_out_lep = set(
            [_brlist_out.At(i) for i in range(_brlist_out.GetEntries())])
        branches_out_lep = [
            x for x in branches_out_lep
            if wrappedOutputTree._tree.GetBranchStatus(x.GetName())
        ]
        # Only keep branches with right collection name
        if self.RemoveFailingObjects[0]:
          self.brlist_sep_lep = [
              self.filterBranchNames(branches_out_lep,self.Lepton[0])
          ]
          self.brlist_all_lep = set(itertools.chain(*(self.brlist_sep_lep)))
        else:
          self.brlist_sep_lep = [ ]
      
        branches_out_jet = set(
            [_brlist_out.At(i) for i in range(_brlist_out.GetEntries())])
        branches_out_jet = [
            x for x in branches_out_jet
            if wrappedOutputTree._tree.GetBranchStatus(x.GetName())
        ]
        if self.RemoveFailingObjects[0]:
           # Only keep branches with right collection name
           self.brlist_sep_jet = [
              self.filterBranchNames(branches_out_jet,self.Jet[0])
           ]
           self.brlist_all_jet = set(itertools.chain(*(self.brlist_sep_jet)))

        else:
          self.brlist_sep_jet = [ ]
        

        self.out = wrappedOutputTree
        if self.RemoveFailingObjects[0]:
           for br in self.brlist_all_jet:
              self.out.branch("%s_%s" % (self.Jet[0], br),
                              _rootLeafType2rootBranchType[self.branchType[br]],
                              lenVar="n"+self.Jet[0])
           for br in self.brlist_all_jet:
              self.out.branch("%s_%s" % (self.Lepton[0], br),
                              _rootLeafType2rootBranchType[self.branchType[br]],
                              lenVar="n"+self.Lepton[0])        

        self.out.branch("%s_TaggedRemoved" % (self.Lepton[0]),_rootLeafType2rootBranchType['Bool_t'], lenVar="n"+self.Lepton[0])
        self.out.branch("%s_TaggedRemoved" % (self.Jet[0]),_rootLeafType2rootBranchType['Bool_t'], lenVar="n"+self.Jet[0])


        pass
 

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def filterBranchNames(self, branches, collection):
        out = []
        for br in branches:
            name = br.GetName()
            if not name.startswith(collection + '_'):
                continue
            out.append(name.replace(collection + '_', ''))
            self.branchType[out[-1]] = br.FindLeaf(br.GetName()).GetTypeName()
        return out


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = Collection(event, self.Jet[0])
        bjets = Collection(event, self.BJet[0])
        leptons = Collection(event, self.Lepton[0])

        clean_jets=[]
        clean_leptons=[]
        tagged_leptons=[]
        tagged_jets=[]        

        for lepton in leptons:
          b_overlap=False
          for bjet in bjets:
            if deltaR(lepton.eta, lepton.phi, bjet.eta, bjet.phi)<self.dRBJet:
               b_overlap=True
        
          if self.RemoveFailingObjects[0]:
            if not b_overlap:
               clean_leptons.append(lepton)
               tagged_leptons.append(False)
          else:
            clean_leptons.append(lepton)
            if not b_overlap:
               tagged_leptons.append(True)
            else:
               tagged_leptons.append(False)
        #if len(clean_leptons)==0: 
        #  return False

        for jet in jets:
          overlap=False
          for lepton in clean_leptons: 
            if deltaR(lepton.eta, lepton.phi, jet.eta, jet.phi)<self.dRJet:
               ovelap=True
          if self.RemoveFailingObjects[0]:
            if not overlap:
              clean_jets.append(jet)
              tagged_jets.append(False)
          else:
            clean_jets.append(jet)
            if not overlap:
               tagged_jets.append(True)
            else:
               tagged_jets.append(False)

#        if len(clean_jets)==0:
#          return False            
        if self.RemoveFailingObjects[0]:
          for brlist,clean_objs,col in zip([self.brlist_all_lep,self.brlist_all_jet],[clean_leptons,clean_jets],[self.Lepton[0],self.Jet[0]]):
#          print brlist,clean_objs,col
            for bridx, br in enumerate(brlist):
               out = []
               for obj in clean_objs:
                   out.append(getattr(obj, br))
               self.out.fillBranch("%s_%s" % (col, br), out) 

        self.out.fillBranch("%s_TaggedRemoved" % (self.Lepton[0]), tagged_leptons)
        self.out.fillBranch("%s_TaggedRemoved" % (self.Jet[0]), tagged_jets)


        return True


