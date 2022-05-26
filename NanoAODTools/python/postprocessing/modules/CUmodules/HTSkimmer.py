from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import os
import numpy as np
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


class HTSkimmer(Module):
    def __init__(self, minJetPt, minJetEta, minJetPUid, minHT, collection ,HTname):
        self.minJetPt=minJetPt,
        self.minHT=minHT,
        self.minJetEta=minJetEta,
        self.minJetPUid=minJetPUid,
        self.collection=collection,
        self.HTname=HTname,
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch(self.HTname[0],'F')
        pass
 

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        Jets = Collection(event, self.collection[0])
        HT=0
        for jet in Jets:
          if getattr( jet,"pt" )>self.minJetPt[0] and abs(getattr( jet,"eta" ))<self.minJetEta[0] and getattr( jet,"puId" )>self.minJetPUid[0]:
             HT+=getattr( jet,"pt" )
        if HT< self.minHT[0]:
           print "HTSkimmer: HT lower than threshold; HT=",HT,"thresh.=",self.minHT[0],"skip"
           return False
        else:
           self.out.fillBranch(self.HTname[0],HT)

        return True


