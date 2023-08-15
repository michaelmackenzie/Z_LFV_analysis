from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import os, math
import numpy as np
import itertools

ROOT.PyConfig.IgnoreCommandLineOptions = True

_rootLeafType2rootBranchType = {'UChar_t': 'b', 'Char_t': 'B', 'UInt_t': 'i','Int_t': 'I','Float_t': 'F', 'Double_t': 'D', 'ULong64_t': 'l', 'Long64_t': 'L', 'Bool_t': 'O'}


class BJetIDWeight(Module):
    def __init__(self, year, algo = 'deepcsv', WPs = ['L', 'T'], eta_max = 2.4):
        self.year = year
        self.algo = algo.lower()
        self.WPs = WPs
        self.eta_max = eta_max

        mc_files = []
        mc_files.append(os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/btagSF/btag_eff_wp_0_mumu_" + year + ".root")
        mc_files.append(os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/btagSF/btag_eff_wp_1_mumu_" + year + ".root")
        mc_files.append(os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/btagSF/btag_eff_wp_2_mumu_" + year + ".root")

        self.mc_files = []
        self.mc_hists = []
        for mc_file in mc_files:
            self.mc_files.append(ROOT.TFile(mc_file  , "READ"))
            if self.mc_files[-1].IsZombie():
                raise Exception("BTag ID MC efficiency file not found!")
            self.mc_hists.append({})
            self.mc_hists[-1]['L'] = self.mc_files[-1].Get('hLRatio') #Light quarks
            self.mc_hists[-1]['C'] = self.mc_files[-1].Get('hCRatio') #c quarks
            self.mc_hists[-1]['B'] = self.mc_files[-1].Get('hBRatio') #b quarks

        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):        
        self.out = wrappedOutputTree
        for WP in self.WPs:
            self.out.branch("Jet_btagSF_%s_%s_wt"      % (self.algo, WP), 'F', lenVar = 'nJet')
            self.out.branch("Jet_btagSF_%s_%s_wt_up"   % (self.algo, WP), 'F', lenVar = 'nJet')
            self.out.branch("Jet_btagSF_%s_%s_wt_down" % (self.algo, WP), 'F', lenVar = 'nJet')
        pass
 

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def mc_eff(self, jet, wp):
        #ensure it's a taggable jet
        if math.fabs(jet.eta) > self.eta_max: return 0.
        if jet.pt < 20.: return 0.
        #retrieve the relevant MC efficiency histogram
        hists = self.mc_hists[wp]
        if abs(jet.partonFlavour) == 4:
            hist = hists['C']
        elif abs(jet.partonFlavour) == 5:
            hist = hists['B']
        else:
            hist = hists['L']
        bin_x = hist.GetXaxis().FindBin(min(2.39, math.fabs(jet.eta)))
        bin_y = hist.GetYaxis().FindBin(min(999., jet.pt))
        eff = hist.GetBinContent(bin_x, bin_y)
        return eff

     #FIXME: The score and cut values should be a function of the algo selected
    def pass_wp(self, jet, wp):
        score = jet.btagDeepB
        val = 1. #default to failing
        if self.year == "2016":
            if   wp == 0: val = 0.2217;
            elif wp == 1: val = 0.6321;
            elif wp == 2: val = 0.8953;
        elif self.year == "2017":
            if   wp == 0: val = 0.1522;
            elif wp == 1: val = 0.4941;
            elif wp == 2: val = 0.8001;
        elif self.year == "2018":
            if   wp == 0: val = 0.1241;
            elif wp == 1: val = 0.4184;
            elif wp == 2: val = 0.7527;
        return score > val


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = Collection(event, "Jet")
        min_p = 1.e-6
        max_p = 1 - min_p
        weights = {}
        ups     = {}
        downs   = {}
        #list of weights for each WP + systematic variation
        for WP in self.WPs:
            weights[WP] = []
            ups    [WP] = []
            downs  [WP] = []
        for jet in jets:
            if jet.pt <= 20. or math.fabs(jet.eta) >= self.eta_max:
                for WP in self.WPs:
                    weights[WP].append(1.)
                    ups    [WP].append(1.)
                    downs  [WP].append(1.)
                continue
            for WP in self.WPs:
                wp = 0
                if   WP == 'M': wp = 1
                elif WP == 'T': wp = 2
                scale      = getattr(jet, 'btagSF_%s_%s'      % (self.algo, WP))
                scale_up   = getattr(jet, 'btagSF_%s_%s_up'   % (self.algo, WP))
                scale_down = getattr(jet, 'btagSF_%s_%s_down' % (self.algo, WP))
                p_mc   = min(max_p, max(min_p, self.mc_eff(jet, wp)))
                p_data = min(max_p, max(min_p, scale*p_mc))
                p_up   = min(max_p, max(min_p, scale_up*p_mc))
                p_down = min(max_p, max(min_p, scale_down*p_mc))
                passes = self.pass_wp(jet, wp)
                if not passes: #if fails, P(event) = 1 - P(pass)
                    p_mc   = 1. - p_mc
                    p_data = 1. - p_data
                    p_up   = 1. - p_up
                    p_down = 1. - p_down
                
                weight = p_data / p_mc
                up     = p_up   / p_mc
                down   = p_down / p_mc
                weights[WP].append(weight)
                ups    [WP].append(up)
                downs  [WP].append(down)

        #fill the results
        for WP in self.WPs:
            self.out.fillBranch("Jet_btagSF_%s_%s_wt"      % (self.algo, WP), weights[WP])
            self.out.fillBranch("Jet_btagSF_%s_%s_wt_up"   % (self.algo, WP), ups    [WP])
            self.out.fillBranch("Jet_btagSF_%s_%s_wt_down" % (self.algo, WP), downs  [WP])

        return True


