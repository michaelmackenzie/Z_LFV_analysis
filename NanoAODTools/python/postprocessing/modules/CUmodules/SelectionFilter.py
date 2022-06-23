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
    def __init__(self, year, prev_ids=0, verbose=0):
        self.year = year
        self.prev_ids = prev_ids
        self.verbose = verbose
        self.seen = 0
        self.mutau = [0,0]
        self.etau = [0,0]
        self.emu = [0,0]
        self.mumu = [0,0]
        self.ee = [0,0]
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
        print "SelectionFilter: Saw %i events: N(mutau) = %i; N(etau) = %i; N(emu) = %i; N(mumu) = %i; N(ee) = %i" % (self.seen, self.mutau[0],
                                                                                                                      self.etau[0], self.emu[0],
                                                                                                                      self.mumu[0], self.ee[0])
        print "SelectionFilter: Passing tight IDs: N(mutau) = %i; N(etau) = %i; N(emu) = %i; N(mumu) = %i; N(ee) = %i" % (self.mutau[1],
                                                                                                                          self.etau[1], self.emu[1],
                                                                                                                          self.mumu[1], self.ee[1])
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
            print "SelectionFilter Event %8i:\n N(e) = %i; N(mu) = %i; N(tau) = %i" % (self.seen, nElectrons, nMuons, nTaus)

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

        #FIXME: Should we consider the Mu50 trigger?
        muonHighTriggered = HLT.Mu50 and self.prev_ids
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

        if self.verbose > 1:
            print " Muon triggered =", muonTriggered, "(low) and", muonHighTriggered, "(high); Electron triggered =", electronTriggered

        #initial trigger filter
        if not (electronTriggered or muonTriggered or muonHighTriggered):
            return False

        if self.verbose > 1:
            print " Event survived trigger check"
            print " Base     selection: mutau = %i; etau = %i; emu = %i; mumu = %i; ee = %i" % (mutau, etau, emu, mumu, ee)


        #Apply some tighter selection IDs on the final leptons
        elec_gap_low  = 1.4442
        elec_gap_high = 1.556
        if etau:
            # etau = etau and electronTriggered
            etau = etau and electrons[0].pt > elec_trig_pt
            etau = etau and taus[0].idDeepTau2017v2p1VSe > 50 #tighter anti-electron tau veto
            eta_sc = math.fabs(electrons[0].eta + electrons[0].deltaEtaSC)
            etau = etau and (eta_sc < elec_gap_low or eta_sc > elec_gap_high)
        if mutau:
            # mutau = mutau and (muonTriggered or (muonHighTriggered and muons[0].pt > 50.))
            mutau = mutau and muons[0].pt > muon_trig_pt
            if self.prev_ids:
                mutau = mutau and muons[0].tightId
        if emu:
            # emu = emu and ((muonTriggered and muons[0].pt > muon_trig_pt) or (muonHighTriggered and muons[0].pt > 50.) or (electronTriggered and electrons[0].pt > elec_trig_pt))
            eta_sc = math.fabs(electrons[0].eta + electrons[0].deltaEtaSC)
            emu = emu and (eta_sc < elec_gap_low or eta_sc > elec_gap_high)
            if self.prev_ids:
                emu = emu and muons[0].tightId
        if mumu:
            # mumu = mumu and ((muonTriggered and (muons[0].pt > muon_trig_pt or muons[1].pt > muon_trig_pt))
            #                  or muonHighTriggered and (muons[0].pt > 50. or muons[1].pt > 50.))
            if self.prev_ids:
                mumu = mumu and muons[0].tightId and muons[1].tightId
                mumu = mumu and (muons[0].pfRelIso04_all < 0.15) and (muons[1].pfRelIso04_all < 0.15)
                mumu = mumu and nElectrons == 0
        if ee:
            # ee = ee and electronTriggered
            # ee = ee and (electrons[0].pt > elec_trig_pt or electrons[1].pt > elec_trig_pt)
            eta_sc_1 = math.fabs(electrons[0].eta + electrons[0].deltaEtaSC)
            eta_sc_2 = math.fabs(electrons[1].eta + electrons[1].deltaEtaSC)
            ee = ee and (eta_sc_1 < elec_gap_low or eta_sc_1 > elec_gap_high)
            ee = ee and (eta_sc_2 < elec_gap_low or eta_sc_2 > elec_gap_high)
            if self.prev_ids:
                ee = ee and electrons[0].mvaFall17V2Iso_WP80 and electrons[1].mvaFall17V2Iso_WP80
                ee = ee and nMuons == 0


        if self.verbose > 1:
            print " Filtered selection: mutau = %i; etau = %i; emu = %i; mumu = %i; ee = %i" % (mutau, etau, emu, mumu, ee)

        #Next remove overlap between the data channels
        #FIXME: Should allow etau_h and mutau_h events, separate searches
        if (mutau and etau) or emu:
            mutau = False
            etau  = False
        if (mumu and ee) or (mutau or etau or emu):
            mumu  = False
            ee    = False

        if self.verbose > 1:
            print " Pruned   selection: mutau = %i; etau = %i; emu = %i; mumu = %i; ee = %i" % (mutau, etau, emu, mumu, ee)

        #Finally apply some additional event filtering
        if mutau:
            lep1 = muons[0]
            lep2 = taus[0]
            lep1_fl = 13
            lep2_fl = 15
        elif etau:
            lep1 = electrons[0]
            lep2 = taus[0]
            lep1_fl = 11
            lep2_fl = 15
        elif emu:
            lep1 = electrons[0]
            lep2 = muons[0]
            lep1_fl = 11
            lep2_fl = 13
        elif mumu:
            lep1 = muons[0]
            lep2 = muons[1]
            lep1_fl = 13
            lep2_fl = 13
        elif ee:
            lep1 = electrons[0]
            lep2 = electrons[1]
            lep1_fl = 11
            lep2_fl = 11
        else:
            return False

        if self.verbose > 1:
            print " Event survived selection specific filtering"

        #Next check the triggers
        isTriggered = False
        #check electron triggers
        isTriggered = isTriggered or (abs(lep1_fl) == 11 and lep1.pt > elec_trig_pt and electronTriggered)
        isTriggered = isTriggered or (abs(lep2_fl) == 11 and lep2.pt > elec_trig_pt and electronTriggered)
        #check muon triggers
        isTriggered = isTriggered or (abs(lep1_fl) == 13 and lep1.pt > muon_trig_pt and muonTriggered)
        isTriggered = isTriggered or (abs(lep2_fl) == 13 and lep2.pt > muon_trig_pt and muonTriggered)
        isTriggered = isTriggered or (abs(lep1_fl) == 13 and lep1.pt > 50 and muonHighTriggered)
        isTriggered = isTriggered or (abs(lep2_fl) == 13 and lep2.pt > 50 and muonHighTriggered)

        if not isTriggered:
            return False

        if self.verbose > 1:
            print " Event survived trigger threshold filtering"

        dilep = lep1.p4() + lep2.p4()
        #Mass filter
        if dilep.M() < 50.:
            return False
        if self.prev_ids and dilep.M() > 170.:
            return False
        if self.verbose > 1:
            print " Event survived di-lepton mass filtering"

        #Overlap filter
        if not self.prev_ids:
            if lep1.p4().DeltaR(lep2.p4()) < 0.3:
                return False
        if self.verbose > 1:
            print " Event survived overlap filtering"

        #FIXME: should use bits, e.g. ID = 1*mutau + (1<<1)*etau + (1<<2)*emu + (1<<3)*mumu + (1<<4)*ee, to use events in multiple selections
        ID = 1*mutau + 2*etau + 3*emu + 4*mumu + 5*ee
        self.out.fillBranch("SelectionFilter_ID", ID)

        if self.verbose:
            print "SelectionFilter: Event %8i: mutau = %i; etau = %i; emu = %i; mumu = %i; ee = %i" % (self.seen, mutau, etau, emu, mumu, ee)

        self.mutau[0] = self.mutau[0] + mutau
        self.etau[0]  = self.etau[0]  + etau
        self.emu[0]   = self.emu[0]   + emu
        self.mumu[0]  = self.mumu[0]  + mumu
        self.ee[0]    = self.ee[0]    + ee

        #removing loose ID region events
        self.mutau[1] = self.mutau[1] + (mutau and lep1.pfRelIso04_all < 0.15 and lep2.idDeepTau2017v2p1VSjet > 50)
        self.mumu[1]  = self.mumu[1]  + (mumu  and lep1.pfRelIso04_all < 0.15 and lep2.pfRelIso04_all < 0.15)
        if self.prev_ids:
            self.etau[1]  = self.etau[1]  + (etau  and lep1.mvaFall17V2Iso_WP80 and lep2.idDeepTau2017v2p1VSjet > 50)
            self.emu[1]   = self.emu[1]   + (emu   and lep1.mvaFall17V2Iso_WP80 and lep2.pfRelIso04_all < 0.15)
            self.ee[1]    = self.ee[1]    + (ee    and lep1.mvaFall17V2Iso_WP80 and lep2.mvaFall17V2Iso_WP80)
        else:
            self.etau[1]  = self.etau[1]  + (etau  and lep1.pfRelIso03_all < 0.15 and lep2.idDeepTau2017v2p1VSjet > 50)
            self.emu[1]   = self.emu[1]   + (emu   and lep1.pfRelIso03_all < 0.15 and lep2.pfRelIso04_all < 0.15)
            self.ee[1]    = self.ee[1]    + (ee    and lep1.pfRelIso03_all < 0.15 and lep2.pfRelIso03_all < 0.15)

        return (ID != 0)
