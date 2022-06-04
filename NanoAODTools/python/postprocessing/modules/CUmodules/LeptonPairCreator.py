from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import os
import numpy as np
import itertools

ROOT.PyConfig.IgnoreCommandLineOptions = True

_rootLeafType2rootBranchType = {
    'UChar_t': 'b', 'Char_t': 'B', 'UInt_t': 'i', 'Int_t': 'I', 'Float_t': 'F',
    'Double_t': 'D', 'ULong64_t': 'l', 'Long64_t': 'L', 'Bool_t': 'O'}


class LeptonPairCreator(Module):
    def __init__(self, LepCollectionA, LepCollectionB=None, LepAmass=0.105,LepBmass=0.000511, pairName="DiLep", minLep1Pt=0, minLep2Pt=0, minPairPt=0, minPairMass=0, maxPairMass=None, OppCharge=False, SameCharge=False, minN=-1):
        self.LepCollectionA=LepCollectionA,
        self.LepCollectionB=LepCollectionB,
        self.LepAmass=LepAmass,
        self.LepBmass = LepBmass,
        self.pairName = pairName,
        self.minLep1Pt=minLep1Pt,
        self.minLep2Pt = minLep2Pt,
        self.minPairPt = minPairPt,
        self.minPairMass = minPairMass,
        self.maxPairMass = maxPairMass,
        self.OppCharge = OppCharge,
        self.SameCharge = SameCharge,
        self.minN = minN,
        self.branchType = {}
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):

        # Create output branches
        self.out = wrappedOutputTree
  #      self.out.branch("n%s" % self.pairName[0],'I')
        for br in ["pt","eta","phi","mass","charge","idxA","idxB"]:
            self.out.branch("%s_%s" % (self.pairName[0], br),
                            _rootLeafType2rootBranchType["Float_t"],
                            lenVar="n%s" % self.pairName[0])

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
        leptonsA = Collection(event, self.LepCollectionA[0])     
        output_collection={"pt":[],"eta":[],"phi":[],"mass":[],"charge":[],"idxA":[],"idxB":[]}
        nOut=0

        if self.LepCollectionB[0]==None:
           for ilep in range(len(leptonsA)):
             lepA=leptonsA[ilep]
             if getattr(lepA,"pt")< self.minLep2Pt:
                continue
             vecA = ROOT.TLorentzVector()
             vecA.SetPtEtaPhiM( getattr(lepA,"pt"), getattr(lepA,"eta"), getattr(lepA,"phi"), self.LepAmass[0] )
             vecB = ROOT.TLorentzVector()
             for ilepB in range(ilep+1, len(leptonsA)): 
               lepB=leptonsA[ilepB]
               if getattr(lepB,"pt")< self.minLep2Pt:
                  continue
               if self.OppCharge[0] and getattr(lepA,"charge")==getattr(lepB,"charge"):
                  continue
               if self.SameCharge[0] and getattr(lepA,"charge")!=getattr(lepB,"charge"):
                  continue
               if self.minLep1Pt[0]!=None and getattr(lepA,"pt")<self.minLep1Pt[0] and getattr(lepB,"pt")<self.minLep1Pt[0]:
                  continue;
               vecB.SetPtEtaPhiM( getattr(lepB,"pt"), getattr(lepB,"eta"), getattr(lepB,"phi"), self.LepBmass[0] )

               if (vecA+vecB).Pt()<self.minPairPt[0]:
                  continue
               if (vecA+vecB).M()<self.minPairMass[0]:
                  continue
               if self.minLep1Pt[0]!=None and getattr(lepA,"pt")<self.minLep1Pt[0] and getattr(lepB,"pt")<self.minLep1Pt[0]:
                  continue;
               nOut+=1
               output_collection["pt"].append( (vecA+vecB).Pt() )
               output_collection["eta"].append( (vecA+vecB).Eta() )
               output_collection["phi"].append( (vecA+vecB).Phi() )
               output_collection["mass"].append( (vecA+vecB).M() )
               output_collection["charge"].append( getattr(lepA,"charge") + getattr(lepB,"charge") )
               output_collection["idxA"].append( ilep )
               output_collection["idxB"].append( ilepB )
                      
        else:
           leptonsB = Collection(event, self.LepCollectionB[0])
           for iA,lepA in enumerate(leptonsA):
             if getattr(lepA,"pt")< self.minLep2Pt[0]:
                continue
             vecA = ROOT.TLorentzVector()
             vecA.SetPtEtaPhiM( getattr(lepA,"pt"), getattr(lepA,"eta"), getattr(lepA,"phi"), self.LepAmass[0] )
             vecB = ROOT.TLorentzVector()
             for iB,lepB in enumerate(leptonsB):
                if getattr(lepB,"pt")< self.minLep2Pt[0]:
                   continue
                if self.OppCharge[0] and getattr(lepA,"charge")==getattr(lepB,"charge"):
                   continue
                if self.SameCharge[0] and getattr(lepA,"charge")!=getattr(lepB,"charge"):
                   continue
                if self.minLep1Pt[0]!=None and getattr(lepA,"pt")<self.minLep1Pt[0] and getattr(lepB,"pt")<self.minLep1Pt[0]:
                  continue;
                vecB.SetPtEtaPhiM( getattr(lepB,"pt"), getattr(lepB,"eta"), getattr(lepB,"phi"), self.LepBmass[0] )
                
                if (vecA+vecB).Pt()<self.minPairPt[0]:
                   continue
                if (vecA+vecB).M()<self.minPairMass[0]:
                   continue
                if self.maxPairMass[0]!=None and (vecA+vecB).M()>self.maxPairMass[0]:
                   continue
                nOut+=1
                output_collection["pt"].append( (vecA+vecB).Pt() )
                output_collection["eta"].append( (vecA+vecB).Eta() )
                output_collection["phi"].append( (vecA+vecB).Phi() )
                output_collection["mass"].append( (vecA+vecB).M() )
                output_collection["charge"].append( getattr(lepA,"charge") + getattr(lepB,"charge") )
                output_collection["idxA"].append( iA )
                output_collection["idxB"].append( iB )

        if nOut<self.minN[0]:
           return False
        self.out.fillBranch("n%s" % self.pairName[0],nOut)
        for br in output_collection.keys():
            self.out.fillBranch("%s_%s" % (self.pairName[0], br), output_collection[br])

        return True


