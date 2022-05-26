from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import os
import numpy as np
import itertools

ROOT.PyConfig.IgnoreCommandLineOptions = True

_rootLeafType2rootBranchType = {'UChar_t': 'b', 'Char_t': 'B', 'UInt_t': 'i','Int_t': 'I','Float_t': 'F', 'Double_t': 'D', 'ULong64_t': 'l', 'Long64_t': 'L', 'Bool_t': 'O'}


class JetSkimmer(Module):
    def __init__(self, BtagWPs, nGoodJetMin, nBJetMax, Selection=None, Veto=None):
        self.BtagWPs=BtagWPs,
        self.nGoodJetMin=nGoodJetMin,
        self.nBJetMax=nBJetMax,
        self.Selection=Selection,
        self.Veto=Veto,
        self.branchType = {}
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        _brlist_out = wrappedOutputTree._tree.GetListOfBranches()
        branches_out = set(
            [_brlist_out.At(i) for i in range(_brlist_out.GetEntries())])
        branches_out = [
            x for x in branches_out
            if wrappedOutputTree._tree.GetBranchStatus(x.GetName())
        ]
        # Only keep branches with right collection name
        self.brlist_sep = [
            self.filterBranchNames(branches_out,"Jet")
        ]
        self.brlist_all = set(itertools.chain(*(self.brlist_sep)))

        # Create output branches
        self.out = wrappedOutputTree
        for br in self.brlist_all:
            self.out.branch("%s_%s" % ("Jet", br),
                            _rootLeafType2rootBranchType[self.branchType[br]],
                            lenVar="nJet")

 #       self.out.branch("nBJet",'F')
#        self.out.branch("nBJet",'F')        
        
        self.out.branch("nBJetMedium",'F')
        self.out.branch("nBJetTight",'F')
        
        for br in ["pt","eta", "phi", "btagDeepB","btagDeepC"]:
            self.out.branch("%s_%s" % ("BJet", br),_rootLeafType2rootBranchType['Float_t'], lenVar="nBJet")            

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
        jets = Collection(event, "Jet")
        if self.Selection[0]!=None:
 #         print self.Selection[0]
          jets = filter( self.Selection[0], jets)

        veto=[]
        if self.Veto[0]!=None:
          veto = filter( self.Veto[0], jets)
        if len(veto)>0:
           print "veto from jets"
           return False

      
        bjets={"pt":[],"eta":[],"phi":[],"btagDeepB":[]}
    
#        nBJet=0; nCJet=0;
        nBJetMedium=0; nBJetTight=0;
        for jet in jets:
          if getattr(jet,"btagDeepB")>float(self.BtagWPs[0][0]):
             for key in bjets.keys():
               bjets[key].append(getattr(jet,key))
             if getattr(jet,"btagDeepB")>float(self.BtagWPs[0][1]):
                nBJetMedium+=1
             if getattr(jet,"btagDeepB")>float(self.BtagWPs[0][2]):
                nBJetTight+=1             
             
        if len(jets)<self.nGoodJetMin[0]:
           print "JetSkimmer:",len(jets),"good jets found with lower limit",self.nGoodJetMin
           return False
           

        if len(bjets)>self.nBJetMax[0]:
            print "JetSkimmer:",len(bjets),"good b-jets found with upper limit",self.nBJetMax, "skip"
            return False

        for bridx, br in enumerate(self.brlist_all):
            out = []
            for obj in jets:
                out.append(getattr(obj, br))
            self.out.fillBranch("%s_%s" % ("Jet", br), out) 
        for key in bjets.keys():
            self.out.fillBranch("%s_%s" % ("BJet", key), bjets[key]) 

        self.out.fillBranch("nBJetMedium",nBJetMedium)
        self.out.fillBranch("nBJetTight",nBJetTight)



        return True


