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


class EmbeddingEMuStudy(Module):
    def __init__(self, year, final_state = "emu", verbose=0):
        self.year = year
        self.final_state = final_state
        self.cut_flow = ROOT.TH1D("hcutflow", "Cut-flow", 100, 0, 100)
        self.ids = []
        if "e" in final_state:
            self.ids.append(11)
        if "mu" in final_state:
            self.ids.append(13)
        if "tau" in final_state:
            self.ids.append(15)
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        pass
 

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.cut_flow.Write()
        nevents = self.cut_flow.GetBinContent(1)
        prev_val = nevents
        print "EmbeddingEMuStudy: Saw %i events, printing efficiencies:" % (nevents)
        for bin in range(1,self.cut_flow.GetNbinsX()+1):
            bin_val = self.cut_flow.GetBinContent(bin)
            if bin_val > 0.:
                print " Step %20s: %8i events, %.3f step, %.3f overall" % (self.cut_flow.GetXaxis().GetBinLabel(bin), bin_val, bin_val/prev_val, bin_val/nevents)
                prev_val = bin_val
        pass

    def get_decay_list(self, idx, gens):
        daughters = []
        for igen,gen in enumerate(gens):
            if gen.genPartIdxMother == idx:
                daughters.append(igen)
        return daughters

    def get_hadronic_lv(self, idx, gens):
        self_decay = True
        pdgId = gens[idx].pdgId
        while self_decay:
            self_decay = False
            daughters = self.get_decay_list(idx, gens)
            #descend down the decay chain until no longer radiative decays, etc.
            for ipart in daughters:
                if gens[ipart].pdgId == pdgId:
                    self_decay = True
                    idx = ipart
        lv = ROOT.TLorentzVector()
        if len(daughters) == 0:
            return lv

        #get the visible decay product
        for ipart in daughters:
            pdgId = gens[ipart].pdgId
            if abs(pdgId) != 12 and abs(pdgId) != 14 and abs(pdgId) != 16: #non-neutrino
                lv = lv + gens[ipart].p4()
        return lv
    
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        self.cut_flow.Fill("Total",1)

        genparts   = Collection(event, "GenPart" )

        ############################################
        # Gen filtering
        ############################################

        lep_one_idx = event.GenZll_LepOne_DecayIdx
        lep_two_idx = event.GenZll_LepTwo_DecayIdx

        #non-tau Z->ll: -99, hadronic tau decay: -1
        if lep_one_idx < -1 or lep_two_idx < -1:
            return False

        lep_one_id = abs(genparts[lep_one_idx].pdgId) if lep_one_idx > -1 else 15
        lep_two_id = abs(genparts[lep_two_idx].pdgId) if lep_two_idx > -1 else 15

        #same-flavor channel
        if lep_one_id == lep_two_id:
            return False

        #ensure it is the right final state
        if not lep_one_id in self.ids or not lep_two_id in self.ids:
            return False
        self.cut_flow.Fill("DecaySelection",1)

        #get the gen tau particles
        tau_one_idx = event.GenZll_LepOne_Idx
        tau_two_idx = event.GenZll_LepTwo_Idx

        gen_tau_1 = genparts[tau_one_idx]
        gen_tau_2 = genparts[tau_two_idx]

        #gen particle vector, use sum of non-neutrinos for hadronic decays
        lv1       = genparts[lep_one_idx].p4() if lep_one_id != 15 else self.get_hadronic_lv(tau_one_idx, genparts)
        lv2       = genparts[lep_two_idx].p4() if lep_two_id != 15 else self.get_hadronic_lv(tau_two_idx, genparts)

        #tau cuts
        if lep_one_id == 15 or lep_two_id == 15:
            if lv1.Pt() < 18. or lv2.Pt() < 18.:
                return False
            self.cut_flow.Fill("PtCut",1)
            if math.fabs(lv1.Eta()) > 2.4 or math.fabs(lv2.Eta()) > 2.4:
                return False
            # if math.fabs(lv1.Eta()) > 2.2 and math.fabs(lv2.Eta()) > 2.2:
            #     return False
            self.cut_flow.Fill("EtaCut",1)
        #tau_e tau_mu cuts
        else:
            if lv1.Pt() < 9. or lv2.Pt() < 9.:
                return False
            self.cut_flow.Fill("TrailingPt",1)

            if lv1.Pt() < 19. and lv2.Pt() < 19.:
                return False
            self.cut_flow.Fill("LeadingPt",1)

        if math.fabs(gen_tau_1.eta) > 2.4 or math.fabs(gen_tau_2.eta) > 2.4:
            return False
        self.cut_flow.Fill("TauEta",1)

        z_mass = abs(event.GenZll_mass)
        if z_mass < 0.:
            z_mass = (gen_tau_1.p4() + gen_tau_2.p4()).M()
        if z_mass < 50.:
            return False
        self.cut_flow.Fill("Mass",1)

        return True
