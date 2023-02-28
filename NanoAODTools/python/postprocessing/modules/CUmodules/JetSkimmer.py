from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import os
import numpy as np
import itertools

ROOT.PyConfig.IgnoreCommandLineOptions = True

_rootLeafType2rootBranchType = {'UChar_t': 'b', 'Char_t': 'B', 'UInt_t': 'i','Int_t': 'I','Float_t': 'F', 'Double_t': 'D', 'ULong64_t': 'l', 'Long64_t': 'L', 'Bool_t': 'O'}


class JetSkimmer(Module):
    def __init__(self, BtagWPs, nGoodJetMin, nBJetMax, BtagBranch = 'btagDeepB', Selection=None, Veto=None):
        self.BtagWPs=BtagWPs,
        self.nGoodJetMin=nGoodJetMin,
        self.nBJetMax=nBJetMax,
        self.BtagBranch = BtagBranch,
        self.Selection=Selection,
        self.Veto=Veto,
        self.branchType = {}

        self.doBJets = len(BtagWPs) > 0
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

        if self.doBJets:
            print "JetSkimmer: Initializing BJet branches"
            self.out.branch("nBJetMedium",'I')
            self.out.branch("nBJetTight",'I')
        
            for br in ["pt","eta", "phi", self.BtagBranch[0],"btagDeepC", "partonFlavour"]:
                if wrappedOutputTree._tree.GetBranchStatus('Jet_%s' % (br)):
                    leaf = wrappedOutputTree._tree.FindLeaf('Jet_%s' % (br))
                    self.out.branch("%s_%s" % ("BJet", br),
                                    _rootLeafType2rootBranchType[leaf.GetTypeName()], lenVar="nBJet")
                else: print "JetSkimmer: Jet collection is missing branch %s" % (br)
            self.out.branch("%s_idx"  % ("BJet"),_rootLeafType2rootBranchType['Int_t'], lenVar="nBJet")
            self.out.branch("%s_WPID" % ("BJet"),_rootLeafType2rootBranchType['Int_t'], lenVar="nBJet")

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
            jets = filter( self.Selection[0], jets)

        veto=[]
        if self.Veto[0]!=None:
            veto = filter( self.Veto[0], jets)
        if len(veto)>0:
            print "JetSkimmer: Veto on the number of jets"
            return False

        if len(jets)<self.nGoodJetMin[0]:
            print "JetSkimmer:",len(jets),"good jets found with lower limit",self.nGoodJetMin
            return False

        bjets={"pt":[],"eta":[],"phi":[],self.BtagBranch[0]:[],'partonFlavour':[],'idx':[],'WPID':[]}    
        if self.doBJets:
            #        nBJet=0; nCJet=0;
            nBJet = 0; nBJetMedium=0; nBJetTight=0;
            for idx,jet in enumerate(jets):
                if getattr(jet,self.BtagBranch[0])>float(self.BtagWPs[0][0]):
                    nBJet += 1
                    for key in bjets.keys():
                        if(hasattr(jet, key)): bjets[key].append(getattr(jet,key))
                        elif key == 'WPID': bjets[key].append(1)
                        elif key == 'idx': bjets[key].append(idx)
                        else: bjets[key].append(-999)
                    if getattr(jet,self.BtagBranch[0])>float(self.BtagWPs[0][1]):
                        bjets[key][-1] = 2
                        nBJetMedium+=1
                    if getattr(jet,self.BtagBranch[0])>float(self.BtagWPs[0][2]):
                        bjets[key][-1] = 3
                        nBJetTight+=1             

            if self.nBJetMax[0] > 0 and len(bjets)>self.nBJetMax[0]:
                print "JetSkimmer:",len(bjets),"good b-jets found with upper limit",self.nBJetMax, "skip"
                return False

        for bridx, br in enumerate(self.brlist_all):
            out = []
            for obj in jets:
                out.append(getattr(obj, br))
            self.out.fillBranch("%s_%s" % ("Jet", br), out)
        if self.doBJets:
            for key in bjets.keys():
                if self.out._tree.GetBranchStatus('BJet_%s' % (key)):
                    self.out.fillBranch("%s_%s" % ("BJet", key), bjets[key]) 

            self.out.fillBranch("nBJetMedium",nBJetMedium)
            self.out.fillBranch("nBJetTight",nBJetTight)

        return True


