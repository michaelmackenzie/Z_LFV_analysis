from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import os
import numpy as np
import itertools
import math

ROOT.PyConfig.IgnoreCommandLineOptions = True

_rootLeafType2rootBranchType = {
    'UChar_t': 'b', 'Char_t': 'B', 'UInt_t': 'i', 'Int_t': 'I', 'Float_t': 'F',
    'Double_t': 'D', 'ULong64_t': 'l', 'Long64_t': 'L', 'Bool_t': 'O'}


class SelectionFilter(Module):
    def __init__(self, year, verbose=0):
        self.year = year
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
        HLT        = Object    (event, "HLT"     )

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

        #Check triggers
        electronTriggered = False
        muonTriggered     = False
        elec_trig_pt      = 33.
        muon_trig_pt      = 25.
        if self.year == "2016":
            electronTriggered = HLT.Ele27_WPTight_Gsf
            muonTriggered     = HLT.IsoMu24
            elec_trig_pt = 28.
        elif self.year == "2017":
            electronTriggered = HLT.Ele32_WPTight_Gsf_L1DoubleEG
            muonTriggered     = HLT.IsoMu27
            muon_trig_pt = 28.
        elif self.year == "2018":
            electronTriggered = HLT.Ele32_WPTight_Gsf
            muonTriggered     = HLT.IsoMu24
        
        #Apply some tighter selection IDs on the final leptons
        elec_gap_low  = 1.4442
        elec_gap_high = 1.556
        if etau:
            etau = etau and electronTriggered
            etau = etau and electrons[0].pt > elec_trig_pt
            etau = etau and taus[0].idDeepTau2017v2p1VSe > 50 #tighter anti-electron tau veto
            eta_sc = math.fabs(electrons[0].eta + electrons[0].deltaEtaSC)
            etau = etau and (eta_sc < elec_gap_low or eta_sc > elec_gap_high)
        if mutau:
            mutau = mutau and muonTriggered
            mutau = mutau and muons[0].pt > muon_trig_pt
        if emu:
            emu = emu and ((muonTriggered and muons[0].pt > muon_trig_pt) or (electronTriggered and electrons[0].pt > elec_trig_pt))
            eta_sc = math.fabs(electrons[0].eta + electrons[0].deltaEtaSC)
            emu = emu and (eta_sc < elec_gap_low or eta_sc > elec_gap_high)
        if mumu:
            mumu = mumu and muonTriggered
            mumu = mumu and (muons[0].pt > muon_trig_pt or muons[1].pt > muon_trig_pt)
        if ee:
            ee = ee and electronTriggered
            ee = ee and (electrons[0].pt > elec_trig_pt or electrons[1].pt > elec_trig_pt)
            eta_sc_1 = math.fabs(electrons[0].eta + electrons[0].deltaEtaSC)
            eta_sc_2 = math.fabs(electrons[1].eta + electrons[1].deltaEtaSC)
            ee = ee and (eta_sc_1 < elec_gap_low or eta_sc_1 > elec_gap_high)
            ee = ee and (eta_sc_2 < elec_gap_low or eta_sc_2 > elec_gap_high)

        #Next remove overlap between the data channels
        #FIXME: Should allow etau_h and mutau_h events, separate searches
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

        #FIXME: should use bits, e.g. ID = 1*mutau + (1<<1)*etau + (1<<2)*emu + (1<<3)*mumu + (1<<4)*ee, to use events in multiple selections
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
