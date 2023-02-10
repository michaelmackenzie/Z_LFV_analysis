from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import os, math
import numpy as np
import itertools

ROOT.PyConfig.IgnoreCommandLineOptions = True

_rootLeafType2rootBranchType = {'UChar_t': 'b', 'Char_t': 'B', 'UInt_t': 'i','Int_t': 'I','Float_t': 'F', 'Double_t': 'D', 'ULong64_t': 'l', 'Long64_t': 'L', 'Bool_t': 'O'}


class ZpTWeight(Module):
    def __init__(self, year, branch = "GenZll"):
        self.year = year
        self.branch = branch

        mc_file   = os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/zpt/z_pt_vs_m_scales_mumu_" + year + ".root"
        sys_file  = os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/zpt/z_pt_vs_m_scales_ee_" + year + ".root"

        self.mc_file  = ROOT.TFile(mc_file , "READ")
        self.sys_file = ROOT.TFile(sys_file, "READ")
        if self.mc_file.IsZombie():
            raise Exception("Z pT correction file not found!")
        if self.sys_file.IsZombie():
            raise Exception("Z pT correction uncertainty file not found!")
        name = 'hGenRatio'
        if not self.mc_file.GetListOfKeys().Contains(name):
            raise Exception("Z pT correction histogram not found!")
        if not self.sys_file.GetListOfKeys().Contains(name):
            raise Exception("Z pT correction uncertainty histogram not found!")
        self.hist = self.mc_file.Get(name)
        self.sys_hist = self.sys_file.Get(name)

        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):        
        self.out = wrappedOutputTree
        self.out.branch("ZpTWeight",'F')
        self.out.branch("ZpTWeight_sys",'F')

        pass
 

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def get_weight(self, hist, pt, mass):
        bin_x = max(1, min(hist.GetNbinsX(), hist.GetXaxis().FindBin(mass)))
        bin_y = max(1, min(hist.GetNbinsY(), hist.GetYaxis().FindBin(pt  )))
        weight = hist.GetBinContent(bin_x, bin_y)
        weight = min(10., max(1.e-6, weight))
        return weight

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if not hasattr(event, "GenJet_pt"): #Data/Embedding
            self.out.fillBranch("ZpTWeight", 1.)
            self.out.fillBranch("ZpTWeight_sys", 1.)
            return True
        if not hasattr(event, "%s_pt" % (self.branch)) or not hasattr(event, "%s_mass" % (self.branch)):
            raise Exception("Z pT correction is missing Z pT/mass from branch %s" % (self.branch))

        genpart = Collection(event, "GenPart")
        z_mass = getattr(event, "%s_mass" % (self.branch))
        z_pt   = getattr(event, "%s_pt"   % (self.branch))
        # check if Z info is found
        if z_mass < 0. or z_pt < 0.:
            #if not found, try replacing with Z->ll di-lepton info
            idx_1 = getattr(event, "%s_LepOne_Idx" % (self.branch))
            idx_2 = getattr(event, "%s_LepTwo_Idx" % (self.branch))
            # if not found, fill with defaults (likely not a Drell-Yan event)
            if idx_1 < 0 or idx_2 < 0:
                self.out.fillBranch("ZpTWeight", 1.)
                self.out.fillBranch("ZpTWeight_sys", 1.)
                return True
            lep_1 = genpart[idx_1]
            lep_2 = genpart[idx_2]
            z_pt   = (lep_1.p4() + lep_2.p4()).Pt()
            z_mass = (lep_1.p4() + lep_2.p4()).M()

        # get the weight for the mass/pT value
        weight     = self.get_weight(self.hist    , z_pt, z_mass)
        weight_sys = self.get_weight(self.sys_hist, z_pt, z_mass)
        self.out.fillBranch("ZpTWeight"    , weight)
        self.out.fillBranch("ZpTWeight_sys", weight_sys)
        return True


