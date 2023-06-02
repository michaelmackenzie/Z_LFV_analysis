from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import os, math
import numpy as np
import itertools

ROOT.PyConfig.IgnoreCommandLineOptions = True

_rootLeafType2rootBranchType = {
    'UChar_t': 'b', 'Char_t': 'B', 'UInt_t': 'i', 'Int_t': 'I', 'Float_t': 'F',
    'Double_t': 'D', 'ULong64_t': 'l', 'Long64_t': 'L', 'Bool_t': 'O'}


class TriggerEff(Module):
    def __init__(self, year, Lepton, Embed = False, verbose=0):
        self.year = int(year)
        self.Lepton = Lepton
        self.Embed = Embed
        self.verbose = verbose
        known_leptons = ['Muon', 'Electron']
        if Lepton not in known_leptons:
            raise Exception("Unknown lepton %s for lepton corrections" % (Lepton))
        self.files = []
        self.data_hists = []
        self.mc_hists = []
        pass

    def beginJob(self):
        if self.Embed or self.Lepton == "Electron":
            self.init_embed()
        else:
            self.init_muon()

        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        # Create output branches
        self.out = wrappedOutputTree
        self.out.branch("%s_trigger_eff_data"      % (self.Lepton), 'F', lenVar = 'n%s' % (self.Lepton))
        self.out.branch("%s_trigger_eff_data_up"   % (self.Lepton), 'F', lenVar = 'n%s' % (self.Lepton))
        self.out.branch("%s_trigger_eff_data_down" % (self.Lepton), 'F', lenVar = 'n%s' % (self.Lepton))
        self.out.branch("%s_trigger_eff_mc"        % (self.Lepton), 'F', lenVar = 'n%s' % (self.Lepton))
        self.out.branch("%s_trigger_eff_mc_up"     % (self.Lepton), 'F', lenVar = 'n%s' % (self.Lepton))
        self.out.branch("%s_trigger_eff_mc_down"   % (self.Lepton), 'F', lenVar = 'n%s' % (self.Lepton))

        pass
 

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    #--------------------------------------------------------------------------------------------------------
    def init_embed(self):
        path = os.environ['CMSSW_BASE'] + '/src/PhysicsTools/NanoAODTools/data/embed/'
        path += 'embedding_eff_'
        path += 'mumu' if self.Lepton == 'Muon' else 'ee'
        path += '_mode-0_%i' % (self.year)
        periods = [0,1] if self.year == 2016 else [0]

        for period in periods:
            fname = path
            if self.year == 2016: fname += '_period_%i' % (period)
            fname += '.root'

            if self.verbose > 0:
                print "Opening correction file %s" % (fname)
            self.files.append(ROOT.TFile.Open(fname, 'READ'))
            if not self.files[-1] or self.files[-1].IsZombie():
                raise Exception("Failed to open %s trigger efficiency file" % (self.Lepton))
            data_name = 'PtVsEtaData'
            mc_name   = 'PtVsEtaMC' if self.Embed else 'PtVsEtaDYMC'
            if not self.files[-1].GetListOfKeys().Contains(data_name):
                raise Exception("Failed to retrieve %s trigger efficiency histogram: %s" % (self.Lepton, data_name))
            if not self.files[-1].GetListOfKeys().Contains(mc_name):
                raise Exception("Failed to retrieve %s trigger efficiency histogram: %s" % (self.Lepton, mc_name))

            self.data_hists.append(self.files[-1].Get(data_name))
            self.mc_hists.append(self.files[-1].Get(mc_name))
        pass

    #--------------------------------------------------------------------------------------------------------
    def init_muon(self):
        path = os.environ['CMSSW_BASE'] + '/src/PhysicsTools/NanoAODTools/data/muon/'
        periods = [0,1] if self.year == 2016 else [0]
        for period in periods:
            if self.year == 2016:
                if period == 0:
                    self.files.append(ROOT.TFile.Open(path + 'EfficienciesAndSF_RunBtoF_muon_2016.root', 'READ'))
                else:
                    self.files.append(ROOT.TFile.Open(path + 'EfficienciesAndSF_Period4_muonTrigger_2016.root', 'READ'))
                folder_name = 'IsoMu24_OR_IsoTkMu24_PtEtaBins'
            elif self.year == 2017:
                self.files.append(ROOT.TFile.Open(path + 'EfficienciesAndSF_2017_RunBtoF_Nov17Nov2017.root', 'READ'))
                folder_name = 'IsoMu27_PtEtaBins'
            elif self.year == 2018:
                self.files.append(ROOT.TFile.Open(path + 'EfficienciesAndSF_2018Data_BeforeMuonHLTUpdate.root', 'READ'))
                folder_name = 'IsoMu24_PtEtaBins'

            data_name = folder_name + '/efficienciesDATA/abseta_pt_DATA'
            mc_name   = folder_name + '/efficienciesMC/abseta_pt_MC'
            if not self.files[-1] or self.files[-1].IsZombie():
                raise Exception("Failed to open %s trigger efficiency file" % (self.Lepton))

            self.data_hists.append(self.files[-1].Get(data_name))
            self.mc_hists.append(self.files[-1].Get(mc_name))
            if not self.data_hists[-1] or self.data_hists[-1].IsZombie():
                raise Exception("Failed to retrieve %s trigger efficiency histogram: %s" % (self.Lepton, data_name))
            if not self.mc_hists[-1] or self.mc_hists[-1].IsZombie():
                raise Exception("Failed to retrieve %s trigger efficiency histogram: %s" % (self.Lepton, mc_name))
        pass

    def init_electron(self):
        path = os.environ['CMSSW_BASE'] + '/src/PhysicsTools/NanoAODTools/data/electron/'
        hist_name = 'EGamma_SF2D'
        periods = [0,1] if self.year == 2016 else [0]
        for period in periods:
            if self.Correction == 'ID':
                known_wp = ['Medium']
                if self.working_point not in known_wp:
                    raise Exception("Unknown %s %s correction working point %s" % (self.Lepton, self.Correction, self.working_point))
                if   self.year == 2016: self.files.append(ROOT.TFile.Open(path + '2016LegacyReReco_ElectronMVA90noiso_Fall17V2.root', 'READ'))
                elif self.year == 2017: self.files.append(ROOT.TFile.Open(path + '2017_ElectronMVA90noiso.root', 'READ'))
                elif self.year == 2018: self.files.append(ROOT.TFile.Open(path + '2018_ElectronMVA90noiso.root', 'READ'))
            elif self.Correction == 'IsoID':
                self.init_embed(useMC = True)
                return
            elif self.Correction == 'RecoID':
                if   self.year == 2016: self.files.append(ROOT.TFile.Open(path + 'EGM2D_BtoH_GT20GeV_RecoSF_Legacy2016.root', 'READ'))
                elif self.year == 2017: self.files.append(ROOT.TFile.Open(path + 'egammaEffi.txt_EGM2D_runBCDEF_passingRECO_2017.root', 'READ'))
                elif self.year == 2018: self.files.append(ROOT.TFile.Open(path + 'egammaEffi.txt_EGM2D_updatedAll_2018.root', 'READ'))

            if not self.files[-1] or self.files[-1].IsZombie():
                raise Exception("Failed to open %s %s correction file" % (self.Lepton, self.Correction))
            if not self.files[-1].GetListOfKeys().Contains(hist_name):
                raise Exception("Failed to retrieve %s %s %s correction histogram: %s" % (self.Lepton, self.working_point, self.Correction, hist_name))

            self.hists.append(self.files[-1].Get(hist_name))
        pass

    def get_effs(self, period, lepton, hists):
        #All corrections are 2D functions of eta (|eta|) and pT
        eta = lepton.eta
        pt  = lepton.pt
        hist = hists[period]

        #determine which axis is which by checking which range is consistent with eta/pT
        eta_x = hist.GetXaxis().GetBinLowEdge(hist.GetNbinsX()) < 10.
        eta_axis = hist.GetXaxis() if eta_x else hist.GetYaxis()
        #determine if it uses |eta| or eta by the axis eta range
        eta = eta if eta_axis.GetBinLowEdge(1) < -1. else math.fabs(eta)

        x_var = eta if eta_x else pt
        y_var = eta if eta_x else pt

        x_bin = max(1, min(hist.GetNbinsX(), hist.GetXaxis().FindBin(x_var)))
        y_bin = max(1, min(hist.GetNbinsY(), hist.GetYaxis().FindBin(y_var)))

        eff   = hist.GetBinContent(x_bin, y_bin)
        error = hist.GetBinError  (x_bin, y_bin)
        #Add an additional uncertainty on our measured TnP efficiencies
        if self.Embed or self.Lepton == 'Electron':
            error = math.sqrt(error*error + 0.005*0.005)
        up = eff + error
        down = max(1.e-6, eff - error)

        return eff, up, down

        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        if not hasattr(event, "%s_pt" % (self.Lepton)):
            raise Exception("Lepton branch %s not defined!" % (self.Lepton))
        if len(self.data_hists) == 0 or len(self.mc_hists) == 0:
            raise Exception("Histograms are not loaded!")

        leptons = Collection(event, self.Lepton)

        data_effs  = []
        data_ups   = []
        data_downs = []
        mc_effs    = []
        mc_ups     = []
        mc_downs   = []
        period = event.MCEra if hasattr(event, "MCEra") else 0
        period = min(period, len(self.data_hists) - 1)
        for lepton in leptons:
            eff, up, down = self.get_effs(period, lepton, self.data_hists)
            data_effs.append(eff)
            data_ups.append(up)
            data_downs.append(down)
            eff, up, down = self.get_effs(period, lepton, self.mc_hists)
            mc_effs.append(eff)
            mc_ups.append(up)
            mc_downs.append(down)
        self.out.fillBranch("%s_trigger_eff_data"      % (self.Lepton), data_effs )
        self.out.fillBranch("%s_trigger_eff_data_up"   % (self.Lepton), data_ups  )
        self.out.fillBranch("%s_trigger_eff_data_down" % (self.Lepton), data_downs)
        self.out.fillBranch("%s_trigger_eff_mc"        % (self.Lepton), mc_effs   )
        self.out.fillBranch("%s_trigger_eff_mc_up"     % (self.Lepton), mc_ups    )
        self.out.fillBranch("%s_trigger_eff_mc_down"   % (self.Lepton), mc_downs  )
            
        return True


