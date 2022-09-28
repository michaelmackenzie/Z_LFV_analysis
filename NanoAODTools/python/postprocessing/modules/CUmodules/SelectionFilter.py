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
    def __init__(self, year, min_mass=50, max_mass=-1, min_dr=0.3, verbose=0):
        self.year = year
        self.min_mass = min_mass
        self.max_mass = max_mass
        self.min_dr = min_dr
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
        self.out.branch("SelectionFilter_MuTau", 'O')
        self.out.branch("SelectionFilter_ETau" , 'O')
        self.out.branch("SelectionFilter_EMu"  , 'O')
        self.out.branch("SelectionFilter_MuMu" , 'O')
        self.out.branch("SelectionFilter_EE"   , 'O')
        pass
 

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        print "SelectionFilter: Saw %10i events: N(mutau) = %i; N(etau) = %i; N(emu) = %i; N(mumu) = %i; N(ee) = %i" % (self.seen, self.mutau[0],
                                                                                                                      self.etau[0], self.emu[0],
                                                                                                                      self.mumu[0], self.ee[0])
        print "SelectionFilter: Passing tight IDs    : N(mutau) = %i; N(etau) = %i; N(emu) = %i; N(mumu) = %i; N(ee) = %i" % (self.mutau[1],
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
        mutau = nElectrons == 0 and nMuons     == 1 and nTaus  == 1
        etau  = nElectrons == 1 and nMuons     == 0 and nTaus  == 1
        emu   = nElectrons == 1 and nMuons     == 1
        mumu  = nElectrons <  2 and nMuons     == 2
        ee    = nElectrons == 2 and nMuons      < 2

        if (mutau + etau + emu + mumu + ee) > 1:
            print "SelectionFilter:: Event %8i: Error! More than one selection passed: N(e) = %i; N(mu) = %i; N(tau) = %i" % (self.seen, nElectrons, nMuons, nTaus)
            #Enforcing exclusive categories
            if (mutau and etau) or emu:
                mutau = False
                etau  = False
            if (mumu and ee) or mutau or etau or emu:
                mumu  = False
                ee    = False

        if self.verbose > 1:
            print " Event survived trigger check"
            print " Base     selection: mutau = %i; etau = %i; emu = %i; mumu = %i; ee = %i" % (mutau, etau, emu, mumu, ee)

        if not (mutau or etau or emu or mumu or ee):
            return False

        #Check triggers
        electronTriggered = False
        muonTriggered     = False
        elec_trig_pt      = 33.
        muon_trig_pt      = 25.

        #FIXME: Should we consider the Mu50 trigger?
        muonHighTriggered = False #HLT.Mu50
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

        #Apply some tighter selection IDs on the final leptons
        min_mass      = self.min_mass
        max_mass      = self.max_mass
        min_delta_r   = self.min_dr

        #Mass filter
        lepm = (lep1.p4() + lep2.p4()).M()
        if lepm < min_mass or (max_mass > min_mass and lepm > max_mass):
            return False

        #Delta R filter
        if math.fabs(lep1.p4().DeltaR(lep2.p4())) < min_delta_r:
            return False

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


        #Accept event

        self.out.fillBranch("SelectionFilter_MuTau", mutau)
        self.out.fillBranch("SelectionFilter_ETau" , etau)
        self.out.fillBranch("SelectionFilter_EMu"  , emu)
        self.out.fillBranch("SelectionFilter_MuMu" , mumu)
        self.out.fillBranch("SelectionFilter_EE"   , ee)

        if self.verbose:
            print "SelectionFilter: Event %8i: mutau = %i; etau = %i; emu = %i; mumu = %i; ee = %i" % (self.seen, mutau, etau, emu, mumu, ee)

        #Count the number of accepted events by category
        self.mutau[0] = self.mutau[0] + mutau
        self.etau[0]  = self.etau[0]  + etau
        self.emu[0]   = self.emu[0]   + emu
        self.mumu[0]  = self.mumu[0]  + mumu
        self.ee[0]    = self.ee[0]    + ee

        #Count the number of tight ID events for debugging/reference
        self.mutau[1] = self.mutau[1] + (mutau and lep1.pfRelIso04_all < 0.15 and lep2.idDeepTau2017v2p1VSjet > 50)
        self.mumu[1]  = self.mumu[1]  + (mumu  and lep1.pfRelIso04_all < 0.15 and lep2.pfRelIso04_all < 0.15)
        self.etau[1]  = self.etau[1]  + (etau  and lep1.pfRelIso03_all < 0.15 and lep2.idDeepTau2017v2p1VSjet > 50)
        self.emu[1]   = self.emu[1]   + (emu   and lep1.pfRelIso03_all < 0.15 and lep2.pfRelIso04_all < 0.15)
        self.ee[1]    = self.ee[1]    + (ee    and lep1.pfRelIso03_all < 0.15 and lep2.pfRelIso03_all < 0.15)

        return (mutau or etau or emu or mumu or ee)
