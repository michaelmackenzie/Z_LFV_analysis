from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import os, math
import numpy as np
import itertools

ROOT.PyConfig.IgnoreCommandLineOptions = True

_rootLeafType2rootBranchType = {'UChar_t': 'b', 'Char_t': 'B', 'UInt_t': 'i','Int_t': 'I','Float_t': 'F', 'Double_t': 'D', 'ULong64_t': 'l', 'Long64_t': 'L', 'Bool_t': 'O'}


class JetPUIDWeight(Module):
    def __init__(self, year, jet_pu_id = 6, pt_min = 20., pt_max = 50.):
        self.year = year
        self.jet_pu_id = jet_pu_id
        self.pt_min = pt_min
        self.pt_max = pt_max

        data_file = os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/jme/scalefactorsPUID_81Xtraining.root"
        mc_file   = os.environ['CMSSW_BASE'] + "/src/CLFVAnalysis/scale_factors/jet_puid_mumu_" + year + ".root"

        self.data_file = ROOT.TFile(data_file, "READ")
        self.mc_file   = ROOT.TFile(mc_file  , "READ")
        if self.data_file.IsZombie():
            raise Exception("Jet PU ID Data file not found!")
        if self.mc_file.IsZombie():
            raise Exception("Jet PU ID MC file not found!")
        data_name = 'h2_eff_sf%s_M' % (year)
        if not self.data_file.GetListOfKeys().Contains(data_name):
            raise Exception("Jet PU ID Data histogram not found!")
        if not self.mc_file.GetListOfKeys().Contains('hRatio'):
            raise Exception("Jet PU ID MC histogram not found!")
        self.data_hist = self.data_file.Get(data_name)
        self.mc_hist   = self.mc_file.Get('hRatio')

        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):        
        self.out = wrappedOutputTree
        self.out.branch("JetPUIDWeight",'F')

        pass
 

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def mc_prob(self, jet):
        h = self.mc_hist
        bin_x = h.GetXaxis().FindBin(jet.pt)
        bin_y = h.GetYaxis().FindBin(jet.eta)
        p = h.GetBinContent(bin_x, bin_y)
        return p

    def data_scale(self, jet):
        h = self.data_hist
        bin_x = h.GetXaxis().FindBin(jet.pt)
        bin_y = h.GetYaxis().FindBin(jet.eta)
        sf = h.GetBinContent(bin_x, bin_y)
        return sf

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = Collection(event, "Jet")
        p_mc = 1.
        p_data = 1.
        min_p = 1.e-6
        max_p = 1 - min_p
        for jet in jets:
            if jet.pt <= self.pt_min or jet.pt >= self.pt_max: continue
            if math.fabs(jet.eta) >= 5.: continue
            p_mc_i = min(max_p, max(min_p, self.mc_prob(jet)))
            p_data_i = min(max_p, max(min_p, self.data_scale(jet)*p_mc_i))
            if jet.puId < self.jet_pu_id: #fails
                p_mc = p_mc*(1. - p_mc_i)
                p_data = p_data*(1. - p_data_i)
            else:
                p_mc = p_mc*(p_mc_i)
                p_data = p_data*(p_data_i)
                
        weight = p_data / p_mc
        self.out.fillBranch("JetPUIDWeight",weight)



        return True


