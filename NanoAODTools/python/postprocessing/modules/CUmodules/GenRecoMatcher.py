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


class GenRecoMatcher(Module):
    def __init__(self, genParticles, recoCollections, maxDR):
        self.genParticleNames = genParticles
        self.recoCollectionNames = recoCollections
        self.maxDR=maxDR
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for name in self.genParticleNames:
          self.out.branch("%s_recoIdx"%(name),'F')
          self.out.branch("%s_recoDR"%(name),'F')

        for name in self.recoCollectionNames:
          self.out.branch("%s_genDR" % (name),
                            _rootLeafType2rootBranchType['Float_t'],
                            lenVar="n%s" % name)
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
        for gen_name,reco_name in zip(self.genParticleNames,self.recoCollectionNames):
          reco = Collection(event, reco_name)
          gen_eta = getattr(event, gen_name+"_eta")
          gen_phi = getattr(event, gen_name+"_phi")
          DRs = [99. for i in range(len(reco))]
          minDR=99.
          minIdx=-1.
          for irc,rc in enumerate(reco):
            dr=deltaR(gen_eta,gen_phi,getattr(rc,'eta'),getattr(rc,'phi'))
            if dr<self.maxDR and dr<minDR:
               minDR=dr
               minIdx=irc
                 
          if minIdx>-1:  DRs[minIdx]=minDR

          self.out.fillBranch("%s_recoDR" % (gen_name), minDR)
          self.out.fillBranch("%s_recoIdx" % (gen_name), minIdx)
          self.out.fillBranch("%s_genDR" % (reco_name), DRs) 

        return True
