from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import os
import numpy as np
import itertools

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


class GenIdenticalMothersDiscriminator(Module):
    def __init__(self,originalMotherNames, selNameMother, daughtersPDG, skipIfNotFound=False,AlternativeDaugthers=None, verbosity=1):
        self.originalMotherNames=originalMotherNames
        self.selNameMother=selNameMother
        self.daughtersPDG=daughtersPDG
        self.skipIfNotFound=skipIfNotFound
        self.AlternativeDaugthers = AlternativeDaugthers
        self.verbosity = verbosity
#        self.newNameMotherB=newNameMotherB
 #       self.daughtersPDGMotherB = daughtersPDGMotherB
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        _brlist_out = wrappedOutputTree._tree.GetListOfBranches()
        self.out = wrappedOutputTree
        branches_out = set(
            [_brlist_out.At(i) for i in range(_brlist_out.GetEntries())])
        branches_out = [
            x for x in branches_out
            if wrappedOutputTree._tree.GetBranchStatus(x.GetName())
        ]
        # Only keep branches with right collection name
        #print branches_out
        self.brlist_sel = [
            branch.GetName().split("_")[1] for branch in branches_out  if (self.originalMotherNames[0] in branch.GetName()) and ("Idx" not in branch.GetName())
        ]
        #self.brlist_mother = set(itertools.chain(*(self.brlist_sel)))
        ''' self.brlist_sel2 = [
            self.filterBranchNames(branches_out,self.originalMotherName2)
        ]
        self.brlist_mother2 = set(itertools.chain(*(self.brlist_sel2)))'''
        self.out = wrappedOutputTree
        for br in self.brlist_sel:
            self.out.branch("%s_%s" % (self.selNameMother, br),'F')
        self.out.branch("%s_%s" % (self.selNameMother, "Idx"),'F')
#        for br in self.brlist_mother2:
#            self.out.branch("%s_%s" % (self.newNameMotherB, br),'F')

        pass
 

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    '''def filterBranchNames(self, branches, collection):
        out = []
        for br in branches:
            name = br.GetName()
            if not name.startswith(collection + '_'):
                continue
            out.append(name.replace(collection + '_', ''))
            self.branchType[out[-1]] = br.FindLeaf(br.GetName()).GetTypeName()
        return out'''


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        gens = Collection(event, "GenPart")    

        self.daughtersPDG= map(float,self.daughtersPDG)

#        self.daughtersPDGMotherB= map(float,self.daughtersPDGMotherB)        

        mothers_idx=[]
        for originalMotherName in self.originalMotherNames:
          mothers_idx.append(getattr(event,originalMotherName+"_Idx"))
        
        
        mothers_obj=[]
        for idx in mothers_idx:
          mothers_obj.append(gens[idx])       

        daughtersPDG_per_mom=[]
        for mom_idx in mothers_idx:       
          daughters_1mom=[]
          for gen in gens:
            if mom_idx != getattr(gen,"genPartIdxMother"):
               continue
            if getattr(gen,"pdgId")==22:
               continue
            daughters_1mom.append(float(getattr(gen,"pdgId")))
          daughtersPDG_per_mom.append(daughters_1mom)
        
        correctMomOrderObj=None
        correctMomOrderIdx=-1
        
        for iMomX,found_daughtersMomX in enumerate(daughtersPDG_per_mom):
          if set(self.daughtersPDG) == set (found_daughtersMomX):
             correctMomOrderObj=mothers_obj[iMomX]
             correctMomOrderIdx=mothers_idx[iMomX]
        
        if correctMomOrderObj==None and self.AlternativeDaugthers!=None:
           for AlternativeDaugther in self.AlternativeDaugthers:    
             AlternativeDaugther=map(float,AlternativeDaugther)
             for iMomX,found_daughtersMomX in enumerate(daughtersPDG_per_mom):
               if set(AlternativeDaugther) == set (found_daughtersMomX):
                  correctMomOrderObj=mothers_obj[iMomX]
                  correctMomOrderIdx=mothers_idx[iMomX]
             if correctMomOrderObj!=None:
                break;

        if correctMomOrderObj==None:
           for iMomX,found_daughtersMomX in enumerate(daughtersPDG_per_mom):
              if self.verbosity>0:
                 print "given",set(self.daughtersPDG),"found",set (found_daughtersMomX)
                 if set(self.daughtersPDG) == set (found_daughtersMomX):
                    print "ok"
              correctMomOrderObj=mothers_obj[iMomX]
              correctMomOrderIdx=mothers_idx[iMomX]
           if self.verbosity>0:
              print "GenIdenticalMothersDiscriminator: decays to discriminate not found"
           if self.skipIfNotFound:
              if self.verbosity>0:
                 print "GenIdenticalMothersDiscriminator: skip event!!! To keep evt: put flag to false"
              return False
           self.out.fillBranch("%s_Idx" % (self.selNameMother), -99)
           for vr in self.brlist_sel:
             self.out.fillBranch("%s_%s" % (self.selNameMother, vr), -99)
           return True
           
           
        self.out.fillBranch("%s_Idx" % (self.selNameMother), correctMomOrderIdx)
        for vr in self.brlist_sel:
          out=getattr(correctMomOrderObj,vr)
          self.out.fillBranch("%s_%s" % (self.selNameMother, vr), out)
        return True
