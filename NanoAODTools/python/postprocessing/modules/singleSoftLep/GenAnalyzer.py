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


class GenAnalyzer(Module):
    def __init__(self, decay, motherName, daughterNames, variables, conjugate, daughter_antipart,grandmother=None):
        self.decay=decay
        self.motherName = motherName
        self.daughterNames=daughterNames
        self.variables=variables
        self.conjugate = conjugate
        self.daughter_antipart=daughter_antipart
        self.grandmother=grandmother
        pass

    def beginJob(self):
        pdgs= self.decay.split("->")
        self.mom_pdg = float(pdgs[0])
        self.daughters_pdg_name = { float(pdg):name for name,pdg in zip(self.daughterNames,pdgs[1].split(","))}
        self.cdaughters_pdg=[]
        if self.conjugate:
          for antipart,pdg in zip(self.daughter_antipart,pdgs[1].split(",")):
             if antipart: self.cdaughters_pdg.append(-1*float(pdg))
             else: self.cdaughters_pdg.append(float(pdg))
#        for name,pdg in zip(self.daughterNames,pdgs[1].split(",")):
#          self.daughters_pdg_name[float(pdg)] = name
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for var in self.variables:
          if self.grandmother==None:
            self.out.branch("%s_%s"%(self.motherName,var),'F')
          for name in self.daughterNames:
            self.out.branch("%s_%s"%(name,var),'F') 
        if self.grandmother==None:
           self.out.branch("%s_Idx"%(self.motherName),'F')
        for name in self.daughterNames:
          self.out.branch("%s_Idx"%(name),'F')
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

        gens = Collection(event, "GenPart")      
        mom_cands=[]

        if self.grandmother!=None:
           mom_idx=getattr(event,self.grandmother)
           given_mom=gens[mom_idx]
           mom_cands.append((mom_idx,given_mom))
        else:        
          for igen,gen in enumerate(gens):
             if (getattr(gen,"pdgId")== self.mom_pdg or ( getattr(gen,"pdgId")== -1*self.mom_pdg and self.conjugate)) and (getattr(gen,"status")==62):
                mom_cands.append((igen,gen))

        if len(mom_cands)>1:
           print "more mothers than 1 -skipping"
           return False
        elif len(mom_cands)==0:
           print "no mothers -skipping"
           return False

        
        
        mom_cand=mom_cands[0]
        
        daughter_part={}
        daughter_idx={}
        correct_decay={key:False for key in self.daughters_pdg_name.keys() }
        conjugate_decay={}
        is_conjugate=False
        if getattr(mom_cand[1],"pdgId")==-1*self.mom_pdg and self.conjugate:
           is_conjugate=True
        if self.conjugate:
           for pdg in self.cdaughters_pdg:
             conjugate_decay[pdg]=False
              
        not_expected_part=False
        for igen,gen in enumerate(gens): 
          if mom_cand[0] != getattr(gen,"genPartIdxMother"):
             continue
          if getattr(gen,"pdgId")==22: continue
          if getattr(gen,"pdgId")==getattr(mom_cand[1],"pdgId"):
             mom_cand=(igen,gen)
             continue;
          if (getattr(gen,"pdgId") in correct_decay.keys()) and getattr(mom_cand[1],"pdgId")==self.mom_pdg:
             daughter_part[getattr(gen,"pdgId")]=gen
             correct_decay[getattr(gen,"pdgId")]=True
             daughter_idx[getattr(gen,"pdgId")]=igen
          elif (getattr(gen,"pdgId") in conjugate_decay.keys()) and is_conjugate:
             sgn=-1
             if getattr(gen,"pdgId") in correct_decay.keys(): sgn=1
             daughter_part[sgn*getattr(gen,"pdgId")]=gen
             conjugate_decay[sgn*getattr(gen,"pdgId")]=True
             daughter_idx[sgn*getattr(gen,"pdgId")]=igen
          else:
             not_expected_part=True
#              break;           
        if not_expected_part:  
             print "not expected part -skip"
             return False
        if not all(correct_decay) and not is_conjugate: 
             print "decay not found - skip"       
             return False
        if not all(conjugate_decay) and is_conjugate: 
             print "conjugate decay not found - skip"
             return False

        mother_daughter_cands={"mom":mom_cand[1],"daughter":daughter_part}
        mother_daughter_idxs={"mom":mom_cand[0],"daughter":daughter_idx}       

        if self.grandmother==None:
          for vr in self.variables:
            out=getattr(mother_daughter_cands['mom'],vr)
          self.out.fillBranch("%s_%s" % (self.motherName, vr), out)
          self.out.fillBranch("%s_Idx" % (self.motherName), mother_daughter_idxs['mom']) 

        for key in mother_daughter_cands['daughter'].keys():
          self.out.fillBranch("%s_Idx" % (self.daughters_pdg_name[key]), mother_daughter_idxs['daughter'][key])
          for vr in self.variables:
            out = getattr(mother_daughter_cands['daughter'][key],vr)
            self.out.fillBranch("%s_%s" % (self.daughters_pdg_name[key], vr), out) 


        return True
