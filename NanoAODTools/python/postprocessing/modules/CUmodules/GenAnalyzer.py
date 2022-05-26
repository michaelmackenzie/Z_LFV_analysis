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


class GenAnalyzer(Module):
    def __init__(self, decay, motherName, daughterNames, variables, conjugate, mother_has_antipart, daughter_has_antipart,grandmother=None,skip=False):
        self.decay=decay
        self.motherName = motherName
        self.daughterNames=daughterNames
        self.variables=variables
        self.conjugate = conjugate
        self.mother_antipart=mother_has_antipart
        self.daughter_antipart=daughter_has_antipart
        self.grandmother=grandmother
        self.skip=skip
        pass

    def beginJob(self):
        pdgs= self.decay.split("->")
        self.mom_pdg = float(pdgs[0])
        self.daughters_pdg_name = { name:float(pdg) for name,pdg in zip(self.daughterNames,pdgs[1].split(","))}
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

    def fillWithDefaults(self):
        if self.grandmother==None:
          self.out.fillBranch("%s_Idx" % (self.motherName), -99)

          for vr in self.variables:
            self.out.fillBranch("%s_%s" % (self.motherName, vr), -99)
          self.out.fillBranch("%s_Idx" % (self.motherName), -99)

        for daugther in self.daughterNames:
          self.out.fillBranch("%s_Idx" % (daugther), -99)
          for vr in self.variables:
            self.out.fillBranch("%s_%s" % (daugther, vr), -99)



    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        gens = Collection(event, "GenPart")      
        mom_cands=[]
        if self.grandmother!=None:
           mom_idx=getattr(event,self.grandmother)
           given_mom=gens[mom_idx]
           mom_cands.append((mom_idx,given_mom))
           if mom_idx<0:
              if self.skip:
                print "GenAnalyzer: grandmother Idx=-99; Skip evt"
                return False
              else:
                print "GenAnalyzer: grandmother Idx=-99"
                self.fillWithDefaults()
                return True

        else:        
          for igen,gen in enumerate(gens):
             if (getattr(gen,"pdgId")== self.mom_pdg or ( getattr(gen,"pdgId")== -1*self.mom_pdg and self.conjugate)) and (getattr(gen,"status")==62):
                mom_cands.append((igen,gen))
                

        if len(mom_cands)>1:
           print "GenAnalyzer: more mothers than 1"
           if self.skip:
              print "GenAnalyzer: skipping evt"
              return False
           else:
             self.fillWithDefaults()
             return True
        elif len(mom_cands)==0:
           print "GenAnalyzer: no mothers"
           if self.skip:
              return False
           else:
             print "GenAnalyzer: skipping evt"
             self.fillWithDefaults()
             return True

        
        
        mom_cand=mom_cands[0]
        
        daughter_part={}
        daughter_idx={}
        correct_decay={self.daughters_pdg_name[key]:False for key in self.daughters_pdg_name.keys() }
        daughter_label={ikey:[key,self.daughters_pdg_name[key],False] for ikey,key in enumerate(self.daughters_pdg_name.keys())}
        conjugate_decay={self.daughters_pdg_name[key]:False for key in self.daughters_pdg_name.keys()}
        is_conjugate=False
        if (getattr(mom_cand[1],"pdgId")==-1*self.mom_pdg and self.conjugate) or(getattr(mom_cand[1],"pdgId")==self.mom_pdg and self.conjugate and not self.mother_antipart):
           is_conjugate=True
        if self.conjugate:
           for pdg in self.cdaughters_pdg:
             conjugate_decay[pdg]=False
              
        not_expected_part=False
        nfound_daughters=0

        for igen,gen in enumerate(gens): 
          if mom_cand[0] != getattr(gen,"genPartIdxMother"):
             continue
          #guard againt part -> part +gamma (photos)
          if getattr(gen,"pdgId")==22: continue
           
          if getattr(gen,"pdgId")==getattr(mom_cand[1],"pdgId"):
             mom_cand=(igen,gen)
             continue;
          # end guard

          if (getattr(gen,"pdgId") in correct_decay.keys()) and getattr(mom_cand[1],"pdgId")==self.mom_pdg:
             daughter_name="skata"
             for label_key in daughter_label.keys():
                if daughter_label[label_key][1] != getattr(gen,"pdgId"):
                   continue
                if daughter_label[label_key][2]:
                   continue
                daughter_name=daughter_label[label_key][0]
                daughter_label[label_key][2]=True
                break
             #print "daughter name",daughter_name
             daughter_part[daughter_name]=gen
             correct_decay[daughter_name]=True
             daughter_idx[daughter_name]=igen
             nfound_daughters+=1
            
          elif (getattr(gen,"pdgId") in conjugate_decay.keys()) and is_conjugate:
             sgn=-1
             if getattr(gen,"pdgId") in correct_decay.keys(): sgn=1
             daughter_name="skata"
             for label_key in daughter_label.keys():
                if daughter_label[label_key][1] != -1*getattr(gen,"pdgId"):
                   continue
                if daughter_label[label_key][2]:
                   continue
                daughter_name=daughter_label[label_key][0]
                daughter_label[label_key][2]=True
                break
             daughter_part[daughter_name]=gen
             conjugate_decay[daughter_name]=True
             daughter_idx[daughter_name]=igen
             nfound_daughters+=1           
          else:
             not_expected_part=True
             print "GenAnalyzer: not expected particle",getattr(gen,"pdgId")
             print "expected",correct_decay

        if not_expected_part:  
           print "GenAnalyzer: not expected part"
           if self.skip:
             print "GenAnalyzer: skipping evt"
             return False
           else:
             self.fillWithDefaults()
             return True
        if not all(correct_decay) and not is_conjugate: 
           print "GenAnalyzer: decay not found"       
           if self.skip:
              print "GenAnalyzer: skipping evt"
              return False
           else:
              self.fillWithDefaults()
              return True
        if not all(conjugate_decay) and is_conjugate: 
           print "GenAnalyzer: conjugate decay not found"
           if self.skip:
              print "GenAnalyzer: skipping evt"
              return False
           else:
              fillWithDefaults()
              return True
             
        mother_daughter_cands={"mom":mom_cand[1],"daughter":daughter_part}
        mother_daughter_idxs={"mom":mom_cand[0],"daughter":daughter_idx}       
       
        
        if self.grandmother==None:
          self.out.fillBranch("%s_Idx" % (self.motherName), mother_daughter_idxs['mom'])
          for vr in self.variables:
            out=getattr(mother_daughter_cands['mom'],vr)
            self.out.fillBranch("%s_%s" % (self.motherName, vr), out)
          self.out.fillBranch("%s_Idx" % (self.motherName), mother_daughter_idxs['mom']) 

        for daugther_key in mother_daughter_cands['daughter'].keys():
          self.out.fillBranch("%s_Idx" % (daugther_key), mother_daughter_idxs['daughter'][daugther_key])
          for vr in self.variables:
            out = getattr(mother_daughter_cands['daughter'][daugther_key],vr)
            self.out.fillBranch("%s_%s" % (daugther_key, vr), out)
          
        return True
