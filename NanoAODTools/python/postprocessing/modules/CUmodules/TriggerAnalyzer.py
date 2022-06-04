from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Object
import ROOT
import os
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


class TriggerAnalyzer(Module):
    def __init__(self, particlePdgId, triggerBits, branchNames, recoCollection, maxDR, maxRelDpt):
        self.particlePdgId = particlePdgId
        self.triggerBits = triggerBits
        self.recoCollectionName = recoCollection
        self.maxDR=maxDR
        self.branchNames=branchNames
        self.maxRelDpt=maxRelDpt
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

        self.out.branch("%s_trgDR"%(self.recoCollectionName),
                            _rootLeafType2rootBranchType['Float_t'],
                            lenVar="n%s"%(self.recoCollectionName))

        self.out.branch("%s_trgRelDpt"%(self.recoCollectionName),
                            _rootLeafType2rootBranchType['Float_t'],
                            lenVar="n%s"%(self.recoCollectionName))

        for name in self.branchNames:
          self.out.branch("%s_%s"%(self.recoCollectionName,name),
                          _rootLeafType2rootBranchType['Bool_t'],
                          lenVar="n%s"%(self.recoCollectionName))
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
#        print self.recoCollectionName
        reco_objs = Collection(event, self.recoCollectionName)
        trg_objs = Collection(event, "TrigObj")
        
        fired_trg_objs=[]
        fired_bits=[]
        for trg in trg_objs:
          if abs(trg.id) != self.particlePdgId:
             continue;
          bits=[ False for i in range(len(self.triggerBits)) ]
          for ibit,bit in enumerate(self.triggerBits):
            if trg.filterBits & (1<<bit) != 0:
               bits[ibit] = True
          if any(bits):
             fired_trg_objs.append(trg)
             fired_bits.append(bits)


        paths_per_obj=[];   dr_per_obj=[];   dpt_per_obj=[]
        for ireco in range(len(reco_objs)):
          paths=[]
          for path in range(len(self.branchNames)):
             paths.append(False)
          paths_per_obj.append(paths)  
          dr_per_obj.append(100)
          dpt_per_obj.append(-1)
        
        for itrg,trg in enumerate(fired_trg_objs):
          minDR=1000
          temp_idx=-1
          for ireco,reco in enumerate(reco_objs):
             dr=deltaR(getattr(trg,'eta'),getattr(trg,'phi'),getattr(reco,'eta'),getattr(reco,'phi'))  
             if dr<minDR:
                minDR=dr
                temp_idx=ireco  
          if minDR<self.maxDR and abs(getattr(trg,'pt')-getattr(reco,'pt'))*1./getattr(reco,'pt')<self.maxRelDpt:
             dr_per_obj[ireco]=minDR
             dpt_per_obj[ireco]=abs(getattr(trg,'pt')-getattr(reco,'pt'))*1./getattr(reco,'pt')
             for ibit,bit in enumerate(fired_bits[itrg]):
               paths_per_obj[ireco][ibit]=fired_bits[itrg][ibit]
        
        obj_per_paths= []
        for itrg in range(len(paths_per_obj[0])):
          objs_result=[]
          for ipth in  range(len(paths_per_obj)):
             objs_result.append(paths_per_obj[ipth][itrg])
          obj_per_paths.append(objs_result)
        
        self.out.fillBranch("%s_trgDR"%(self.recoCollectionName), dr_per_obj)
        self.out.fillBranch("%s_trgRelDpt"%(self.recoCollectionName), dpt_per_obj)
        for iname in range(len(self.branchNames)):
          self.out.fillBranch("%s_%s"%(self.recoCollectionName,self.branchNames[iname]), obj_per_paths[iname])
        return True
