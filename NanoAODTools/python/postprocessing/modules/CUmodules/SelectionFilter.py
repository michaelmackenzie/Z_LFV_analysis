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


class SelectionFilter(Module):
    def __init__(self, verbose=0):
        self.verbose = verbose
        self.seen = 0
        self.mutau = 0
        self.etau = 0
        self.emu = 0
        self.mumu = 0
        self.ee = 0
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("SelectionFilter_ID", 'I')
        pass
 

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        print "SelectionFilter: Saw %i events: N(mutau) = %i; N(etau) = %i; N(emu) = %i; N(mumu) = %i; N(ee) = %i" % (self.seen, self.mutau, self.etau, self.emu, self.mumu, self.ee)
        pass


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        self.seen = self.seen + 1

        electrons  = Collection(event, "Electron")
        muons      = Collection(event, "Muon"    )
        taus       = Collection(event, "Tau"     )
        nElectrons = len(electrons)
        nMuons     = len(muons    )
        nTaus      = len(taus     )

        if self.verbose > 1:
            print "SelectionFilter: N(e) = %i; N(mu) = %i; N(tau) = %i" % (nElectrons, nMuons, nTaus)

        #Count the selected leptons in the event to determine possible selections
        mutau = nMuons     == 1 and nTaus  == 1
        etau  = nElectrons == 1 and nTaus  == 1
        emu   = nElectrons == 1 and nMuons == 1
        mumu  = nMuons     == 2
        ee    = nElectrons == 2

        #Apply some tighter selection IDs on the final leptons
        if etau:
            etau = etau and taus[0].idDeepTau2017v2p1VSe > 50 #tighter anti-electron tau veto
            etau = etau and electrons[0].pt > 29. #minimum threshold for Run-II
        if mutau:
            mutau = mutau and muons[0].pt > 25. #minimum threshold for Run-II
        if emu:
            emu = emu and (electrons[0].pt > 29. or muons[0].pt > 25.) #minimum threshold for Run-II
        if mumu:
            mumu = mumu and (muons[0].pt > 25. or muons[1].pt > 25.) #minimum threshold for Run-II
        if ee:
            ee = ee and (electrons[0].pt > 29. or electrons[1].pt > 29.) #minimum threshold for Run-II

        #Next remove overlap between the data channels
        if (mutau and etau) or emu:
            mutau = False
            etau  = False
        if (mumu and ee) or (mutau or etau or emu):
            mumu  = False
            ee    = False

        #Finally apply some additional event filtering
        if mutau:
            lep1 = muons[0]
            lep2 = taus[0]
        elif etau:
            lep1 = electrons[0]
            lep2 = taus[0]
        elif emu:
            lep1 = electrons[0]
            lep2 = muons[0]
        elif mumu:
            lep1 = muons[0]
            lep2 = muons[1]
        elif ee:
            lep1 = electrons[0]
            lep2 = electrons[1]
        else:
            return False

        dilep = lep1.p4() + lep2.p4()
        #Mass filter
        if dilep.M() < 50.:
            return False
        #Overlap filter
        if lep1.p4().DeltaR(lep2.p4()) < 0.3:
            return False
        
        ID = 1*mutau + 2*etau + 3*emu + 4*mumu + 5*ee
        self.out.fillBranch("SelectionFilter_ID", ID)

        if self.verbose:
            print "SelectionFilter: mutau = %i; etau = %i; emu = %i; mumu = %i; ee = %i" % (mutau, etau, emu, mumu, ee)

        self.mutau = self.mutau + mutau
        self.etau  = self.etau  + etau
        self.emu   = self.emu   + emu
        self.mumu  = self.mumu  + mumu
        self.ee    = self.ee    + ee

        return (ID != 0)
