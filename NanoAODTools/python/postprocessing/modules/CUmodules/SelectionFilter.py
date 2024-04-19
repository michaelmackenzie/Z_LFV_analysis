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
    def __init__(self, year, min_mass=50, max_mass=-1, min_dr=0.3, use_emu_trig=False, apply_trigger=True, data_region=None, dataset=None, verbose=0,
                 kill_channels = []):
        self.year = year
        self.min_mass = min_mass
        self.max_mass = max_mass
        self.min_dr = min_dr
        self.use_emu_trig = use_emu_trig
        self.apply_trigger = apply_trigger
        self.data_region = data_region
        self.dataset = dataset
        self.verbose = verbose
        self.kill_channels = kill_channels
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
        self.out.branch("SelectionFilter_LepM" , 'F') #For filtering mass regions downstream
        pass
 

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        print "SelectionFilter: Saw %10i events: N(mutau) = %i; N(etau) = %i; N(emu) = %i; N(mumu) = %i; N(ee) = %i" % (self.seen, self.mutau[0],
                                                                                                                      self.etau[0], self.emu[0],
                                                                                                                      self.mumu[0], self.ee[0])
        print "SelectionFilter: Passing tight IDs    : N(mutau) = %i; N(etau) = %i; N(emu) = %i; N(mumu) = %i; N(ee) = %i" % (self.mutau[1],
                                                                                                                              self.etau[1], self.emu[1],
                                                                                                                              self.mumu[1], self.ee[1])
        #Add a histogram with selection count information
        h = ROOT.TH1D("events_selection", "events_selection", 10, 0, 10)
        h.Fill(0.5, self.seen    )
        h.Fill(1.5, self.emu[0]  )
        h.Fill(2.5, self.etau[0] )
        h.Fill(3.5, self.mutau[0])
        h.Fill(4.5, self.ee[0]   )
        h.Fill(5.5, self.mumu[0] )
        h.Write()
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
        emuTriggered      = False
        mueTriggered      = False
        elec_trig_pt      = 33.
        muon_trig_pt      = 25.
        emu_trig_e_pt     = 23.
        mue_trig_e_pt     = 12.
        emu_trig_mu_pt    =  8.
        mue_trig_mu_pt    = 23.

        #FIXME: Should we consider the Mu50 trigger?
        muonHighTriggered = False #HLT.Mu50
        if self.year == "2016":
            electronTriggered = HLT.Ele27_WPTight_Gsf
            muonTriggered     = HLT.IsoMu24
            if self.data_region is None or self.data_region not in ['G', 'H']:
                emuTriggered      = HLT.Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL
                mueTriggered      = HLT.Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL
            else:
                emuTriggered      = HLT.Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ
                mueTriggered      = HLT.Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ
            elec_trig_pt = 28.
        elif self.year == "2017":
            electronTriggered = HLT.Ele32_WPTight_Gsf_L1DoubleEG
            muonTriggered     = HLT.IsoMu27
            emuTriggered      = HLT.Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ
            mueTriggered      = HLT.Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ
            muon_trig_pt = 28.
        elif self.year == "2018":
            electronTriggered = HLT.Ele32_WPTight_Gsf
            muonTriggered     = HLT.IsoMu24
            emuTriggered      = HLT.Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL
            mueTriggered      = HLT.Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL

        # #Default the e-mu trigger to _DZ when available, as no _DZ becomes pre-scaled during 2016
        # #for MC, continue to use the no _DZ version in 2016, as the H->ll' analysis did
        # is_MC = hasattr(event, "nGenJet") #neither data nor Embedded samples
        # if hasattr(HLT, "Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL"):
        #     emuTriggered = HLT.Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL
        # if hasattr(HLT, "Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ") and (not is_MC or self.year != "2016"):
        #     emuTriggered = HLT.Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ
        # if hasattr(HLT, "Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL"):
        #     mueTriggered = HLT.Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL
        # if hasattr(HLT, "Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ") and (not is_MC or self.year != "2016"):
        #     mueTriggered = HLT.Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ

        if self.verbose > 1:
            print " Muon triggered =", muonTriggered, "(low) and", muonHighTriggered, "(high); Electron triggered =", electronTriggered,\
                "; emu triggered =", emuTriggered, "; mue triggered =", mueTriggered

        #initial trigger filter
        isTriggered = not self.apply_trigger or electronTriggered or muonTriggered
        if self.use_emu_trig and emu: #only relevant for e-mu data
            isTriggered = isTriggered or emuTriggered or mueTriggered
        if not isTriggered:
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

        #Next check the triggers given the selection being used and the trigger thresholds
        isTriggered = not self.apply_trigger

        #check electron triggers
        pass_ele_trig = False
        pass_ele_trig = pass_ele_trig or (abs(lep1_fl) == 11 and lep1.pt > elec_trig_pt and electronTriggered)
        pass_ele_trig = pass_ele_trig or (abs(lep2_fl) == 11 and lep2.pt > elec_trig_pt and electronTriggered)
        #check muon triggers
        pass_muon_trig = False
        pass_muon_trig = pass_muon_trig or (abs(lep1_fl) == 13 and lep1.pt > muon_trig_pt and muonTriggered)
        pass_muon_trig = pass_muon_trig or (abs(lep2_fl) == 13 and lep2.pt > muon_trig_pt and muonTriggered)
        pass_muon_trig = pass_muon_trig or (abs(lep1_fl) == 13 and lep1.pt > 50 and muonHighTriggered)
        pass_muon_trig = pass_muon_trig or (abs(lep2_fl) == 13 and lep2.pt > 50 and muonHighTriggered)
        #check emu triggers
        pass_emu_trig = False
        if self.use_emu_trig and emu:
            electron = lep1 if abs(lep1_fl) == 11 else lep2
            muon     = lep2 if abs(lep1_fl) == 11 else lep1
            pass_emu_trig = pass_emu_trig or (emuTriggered and muon.pt > emu_trig_mu_pt and electron.pt > emu_trig_e_pt)
            pass_emu_trig = pass_emu_trig or (mueTriggered and muon.pt > mue_trig_mu_pt and electron.pt > mue_trig_e_pt)

        #take an OR of all triggers
        isTriggered = pass_ele_trig or pass_muon_trig or pass_emu_trig
        if not isTriggered:
            return False

        #if using the MuonEG dataset, only pass the event if it's e-mu triggered and e-mu data
        if self.dataset is not None and 'MuonEGRun' in self.dataset:
            if not emu:
                return False
            if self.apply_trigger and not pass_emu_trig:
                return False
            #These events will come from the other datasets, where we can select them with e-mu trigger if needed there
            if self.apply_trigger and (pass_muon_trig or pass_ele_trig):
                return False

        if self.verbose > 1:
            print " Event survived trigger threshold filtering"

        # Check if this channel is being filtered out in this ntupling

        for channel in self.kill_channels:
            if channel == "mumu"  and mumu : return False
            if channel == "ee"    and ee   : return False
            if channel == "emu"   and emu  : return False
            if channel == "etau"  and etau : return False
            if channel == "mutau" and mutau: return False

        if self.verbose > 1:
            print " Event survived channel filtering"

        #Accept event

        self.out.fillBranch("SelectionFilter_MuTau", mutau)
        self.out.fillBranch("SelectionFilter_ETau" , etau)
        self.out.fillBranch("SelectionFilter_EMu"  , emu)
        self.out.fillBranch("SelectionFilter_MuMu" , mumu)
        self.out.fillBranch("SelectionFilter_EE"   , ee)
        self.out.fillBranch("SelectionFilter_LepM" , lepm)

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
