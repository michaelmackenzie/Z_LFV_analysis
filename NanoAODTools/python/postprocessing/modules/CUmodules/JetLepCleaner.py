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
    def __init__(self, Lepton, Jet, dRJet, RemoveOverlappingJets, RemoveOverlappingLeptons):
        self.Lepton=Lepton,
        self.Jet=Jet,
        self.dRJet=dRJet,
        self.RemoveOverlappingJets=RemoveOverlappingJets,
        self.RemoveOverlappingLeptons=RemoveOverlappingLeptons,
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
        if self.RemoveOverlappingLeptons[0]:
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
        if self.RemoveOverlappingJets[0]:
           # Only keep branches with right collection name
           self.brlist_sep_jet = [
              self.filterBranchNames(branches_out_jet,self.Jet[0])
           ]
           self.brlist_all_jet = set(itertools.chain(*(self.brlist_sep_jet)))

        else:
          self.brlist_sep_jet = [ ]
        

        self.out = wrappedOutputTree
        if self.RemoveOverlappingJets[0]:
           for br in self.brlist_all_jet:
              self.out.branch("%s_%s" % (self.Jet[0], br),
                              _rootLeafType2rootBranchType[self.branchType[br]],
                              lenVar="n"+self.Jet[0])
        if self.RemoveOverlappingLeptons[0]:
           for br in self.brlist_all_jet:
              self.out.branch("%s_%s" % (self.Lepton[0], br),
                              _rootLeafType2rootBranchType[self.branchType[br]],
                              lenVar="n"+self.Lepton[0])        

        self.out.branch("%s_TaggedAsRemovedBy%s" % (self.Lepton[0],self.Jet[0]),_rootLeafType2rootBranchType['Bool_t'], lenVar="n"+self.Lepton[0])
        self.out.branch("%s_TaggedAsRemovedBy%s" % (self.Jet[0],self.Lepton[0]),_rootLeafType2rootBranchType['Bool_t'], lenVar="n"+self.Jet[0])
        self.out.branch("%s_%sOverlapIdx" % (self.Lepton[0],self.Jet[0]),_rootLeafType2rootBranchType['Int_t'], lenVar="n"+self.Lepton[0])
        self.out.branch("%s_%sOverlapIdx" % (self.Jet[0],self.Lepton[0]),_rootLeafType2rootBranchType['Int_t'], lenVar="n"+self.Jet[0])


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
        leptons = Collection(event, self.Lepton[0])
        if self.RemoveOverlappingLeptons[0] and self.RemoveOverlappingJets[0]:
           print "JetLepCleaner: Warning: removing BOTH jets and leptons when overlap might give wrong results"
        clean_jets=[]
        clean_leptons=[]
        tagged_leptons=[]
        tagged_jets=[]        
        lepton_overlap_jet_idx=[]
        jet_overlap_lepton_idx=[]

        
        for lepton in leptons:
          overlap=False
          overlap_idx=-1
          minDR=1000.
          itemp=-1
          for ijet,jet in enumerate(jets):
            if deltaR(lepton.eta, lepton.phi, jet.eta, jet.phi)<minDR:
               minDR=deltaR(lepton.eta, lepton.phi, jet.eta, jet.phi)
               itemp=ijet
          if minDR<self.dRJet[0]:
               overlap=True
               overlap_idx=itemp 
          if self.RemoveOverlappingLeptons[0]:
            if not overlap:
              clean_leptons.append(lepton)
              tagged_leptons.append(overlap)
              lepton_overlap_jet_idx.append(overlap_idx)
            else:
              pass
          else:
            clean_leptons.append(lepton) 
            tagged_leptons.append(overlap)
            lepton_overlap_jet_idx.append(overlap_idx)
        

        for jet in jets:
          overlap=False
          overlap_idx=-1
          minDR=1000.
          itemp=-1
          for ilep,lepton in enumerate(leptons): 
            if deltaR(lepton.eta, lepton.phi, jet.eta, jet.phi)<minDR:
               minDR=deltaR(lepton.eta, lepton.phi, jet.eta, jet.phi)
               itemp=ilep

          if minDR<self.dRJet[0]:
               overlap=True
               overlap_idx=itemp
          if self.RemoveOverlappingJets[0]:
            if not overlap:
              clean_jets.append(jet)
              tagged_jets.append(overlap)
              jet_overlap_lepton_idx.append(overlap_idx)
            else:
              pass
          else:
            clean_jets.append(jet)
            tagged_jets.append(overlap)
            jet_overlap_lepton_idx.append(overlap_idx)
        

        if self.RemoveOverlappingJets[0]:
          for brlist,clean_objs,col in zip([self.brlist_all_jet],[clean_jets],[self.Jet[0]]):
            for bridx, br in enumerate(brlist):
               out = []
               for obj in clean_objs:
                   out.append(getattr(obj, br))
               self.out.fillBranch("%s_%s" % (col, br), out) 
        if self.RemoveOverlappingLeptons[0]:
          for brlist,clean_objs,col in zip([self.brlist_all_lep],[clean_leptons],[self.Lepton[0]]):
            for bridx, br in enumerate(brlist):
               out = []
               for obj in c_objs:
                   out.append(getattr(obj, br))
               self.out.fillBranch("%s_%s" % (col, br), out)

        self.out.fillBranch("%s_TaggedAsRemovedBy%s" % (self.Lepton[0],self.Jet[0]), tagged_leptons)
        self.out.fillBranch("%s_%sOverlapIdx" % (self.Lepton[0],self.Jet[0]), lepton_overlap_jet_idx)
        self.out.fillBranch("%s_TaggedAsRemovedBy%s" % (self.Jet[0],self.Lepton[0]), tagged_jets)
        self.out.fillBranch("%s_%sOverlapIdx" % (self.Jet[0],self.Lepton[0]), jet_overlap_lepton_idx)
        

        return True



