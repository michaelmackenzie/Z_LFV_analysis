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


class LeptonSF(Module):
    def __init__(self, year, Lepton, Correction, working_point = 'Medium', Embed = False, verbose=0):
        self.year = int(year)
        self.Lepton = Lepton
        self.Correction = Correction
        self.working_point = working_point
        self.Embed = Embed
        self.verbose = verbose
        known_leptons = ['Muon', 'Electron']
        if Lepton not in known_leptons:
            raise Exception("Unknown lepton %s for lepton corrections" % (Lepton))
        self.files = []
        self.hists = []
        pass

    def beginJob(self):
        if self.Embed:
            self.init_embed()
        elif self.Lepton == 'Muon':
            self.init_muon()
        elif self.Lepton == 'Electron':
            self.init_electron()

        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        # Create output branches
        self.out = wrappedOutputTree
        self.out.branch("%s_%s_wt"   % (self.Lepton, self.Correction), 'F', lenVar = 'n%s' % (self.Lepton))
        self.out.branch("%s_%s_up"   % (self.Lepton, self.Correction), 'F', lenVar = 'n%s' % (self.Lepton))
        self.out.branch("%s_%s_down" % (self.Lepton, self.Correction), 'F', lenVar = 'n%s' % (self.Lepton))

        pass
 

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    #--------------------------------------------------------------------------------------------------------
    def init_embed(self, useMC = False):
        known_corr = ['ID', 'IsoID', 'RecoID']
        if self.Correction not in known_corr:
            raise Exception("Unknown %s correction %s" % (self.Lepton, self.Correction))
        if self.Correction == 'RecoID':
            if self.Lepton == 'Muon':
                raise Exception("Reco ID not defined for muons")
            else: # use MC electron reco ID corrections
                self.init_electron()
                return
        path = os.environ['CMSSW_BASE'] + '/src/PhysicsTools/NanoAODTools/data/embed/'
        path += 'embedding_eff_'
        path += 'mumu' if self.Lepton == 'Muon' else 'ee'
        if self.Correction == 'ID': mode = 1
        elif self.Correction == 'IsoID': mode = 2
        path += '_mode-%i_%i' % (mode, self.year)
        periods = [0,1] if self.year == 2016 else [0]

        for period in periods:
            fname = path
            if self.year == 2016: fname += '_period_%i' % (period)
            fname += '.root'

            if self.verbose > 0:
                print "Opening correction file %s" % (fname)
            self.files.append(ROOT.TFile.Open(fname, 'READ'))
            hist_name = 'PtVsEtaSF' if not useMC else 'PtVsEtaDYMC'
            if not self.files[-1] or self.files[-1].IsZombie():
                raise Exception("Failed to open %s %s correction file" % (self.Lepton, self.Correction))
            if not self.files[-1].GetListOfKeys().Contains(hist_name):
                raise Exception("Failed to retrieve %s %s correction histogram: %s" % (self.Lepton, self.Correction, hist_name))
            if useMC and not self.files[-1].GetListOfKeys().Contains('PtVsEtaData'):
                raise Exception("Failed to retrieve %s %s Data correction histogram: %s" % (self.Lepton, self.Correction, hist_name))

            if useMC:
                self.hists.append(self.files[-1].Get('PtVsEtaData'))
                self.hists[-1].Divide(self.files[-1].Get('PtVsEtaDYMC'))
            else:
                self.hists.append(self.files[-1].Get(hist_name))
        pass

    #--------------------------------------------------------------------------------------------------------
    def init_muon(self):
        known_corr = ['ID', 'IsoID']
        if self.Correction not in known_corr:
            raise Exception("Unknown %s correction %s" % (self.Lepton, self.Correction))
        path = os.environ['CMSSW_BASE'] + '/src/PhysicsTools/NanoAODTools/data/muon/'
        periods = [0,1] if self.year == 2016 else [0]
        for period in periods:
            if self.Correction == 'ID':
                known_wp = ['Medium', 'Tight']
                if self.working_point not in known_wp:
                    raise Exception("Unknown %s %s correction working point %s" % (self.Lepton, self.Correction, self.working_point))
                if self.year == 2016:
                    if period == 0:
                        self.files.append(ROOT.TFile.Open(path + 'RunBCDEF_SF_ID_muon_2016.root', 'READ'))
                    else:
                        self.files.append(ROOT.TFile.Open(path + 'RunGH_SF_ID_muon_2016.root', 'READ'))
                    hist_name = 'NUM_%sID_DEN_genTracks_eta_pt' % (self.working_point)
                elif self.year == 2017:
                    self.files.append(ROOT.TFile.Open(path + '2017_Mu_RunBCDEF_SF_ID.root', 'READ'))
                    hist_name = 'NUM_%sID_DEN_genTracks_pt_abseta' % (self.working_point)
                elif self.year == 2018:
                    self.files.append(ROOT.TFile.Open(path + 'RunABCD_SF_ID_muon_2018.root', 'READ'))
                    hist_name = 'NUM_%sID_DEN_TrackerMuons_pt_abseta' % (self.working_point)
            elif self.Correction == 'IsoID':
                known_wp = ['Tight', 'TightIDandIPCut', 'Medium', 'MediumID']
                if self.working_point not in known_wp:
                    raise Exception("Unknown %s %s correction working point %s" % (self.Lepton, self.Correction, self.working_point))
                if self.working_point == 'Tight': self.working_point = 'TightIDandIPCut'
                if self.working_point == 'Medium': self.working_point = 'MediumID'
                if self.year == 2016:
                    if period == 0:
                        self.files.append(ROOT.TFile.Open(path + 'RunBCDEF_SF_ISO_muon_2016.root', 'READ'))
                    else:
                        self.files.append(ROOT.TFile.Open(path + 'RunGH_SF_ISO_muon_2016.root', 'READ'))
                    hist_name = 'NUM_TightRelIso_DEN_%s_eta_pt' % (self.working_point)
                elif self.year == 2017:
                    self.files.append(ROOT.TFile.Open(path + '2017_Mu_RunBCDEF_SF_ISO.root', 'READ'))
                    hist_name = 'NUM_TightRelIso_DEN_%s_pt_abseta' % (self.working_point)
                elif self.year == 2018:
                    self.files.append(ROOT.TFile.Open(path + 'RunABCD_SF_ISO_muon_2018.root', 'READ'))
                    hist_name = 'NUM_TightRelIso_DEN_%s_pt_abseta' % (self.working_point)

            if not self.files[-1] or self.files[-1].IsZombie():
                raise Exception("Failed to open %s %s correction file" % (self.Lepton, self.Correction))
            if not self.files[-1].GetListOfKeys().Contains(hist_name):
                raise Exception("Failed to retrieve %s %s %s correction histogram: %s" % (self.Lepton, self.working_point, self.Correction, hist_name))

            self.hists.append(self.files[-1].Get(hist_name))
        pass

    def init_electron(self):
        known_corr = ['ID', 'IsoID', 'RecoID']
        if self.Correction not in known_corr:
            raise Exception("Unknown %s correction %s" % (self.Lepton, self.Correction))
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

    def get_weight(self, period, lepton):
        #All corrections are 2D functions of eta (|eta|) and pT
        eta = lepton.eta
        pt  = lepton.pt
        hist = self.hists[period]

        #determine which axis is which by checking which range is consistent with eta/pT
        eta_x = hist.GetXaxis().GetBinLowEdge(hist.GetNbinsX()) < 10.
        eta_axis = hist.GetXaxis() if eta_x else hist.GetYaxis()
        #determine if it uses |eta| or eta by the axis eta range
        eta = eta if eta_axis.GetBinLowEdge(1) < -1. else math.fabs(eta)

        x_var = eta if eta_x else pt
        y_var = eta if eta_x else pt

        x_bin = max(1, min(hist.GetNbinsX(), hist.GetXaxis().FindBin(x_var)))
        y_bin = max(1, min(hist.GetNbinsY(), hist.GetYaxis().FindBin(y_var)))

        weight = hist.GetBinContent(x_bin, y_bin)
        error = hist.GetBinError(x_bin, y_bin)
        #Add an additional uncertainty on Embedded lepton scales
        if self.Embed or (self.Lepton == 'Electron' and self.Correction == 'IsoID'):
            if self.Lepton == 'Muon':
                error = math.sqrt(error*error + 0.01*0.01)
            elif self.Lepton == 'Electron':
                error = math.sqrt(error*error + 0.02*0.02)
        up = weight + error
        down = max(1.e-6, weight - error)

        return weight, up, down

        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        if not hasattr(event, "%s_pt" % (self.Lepton)):
            raise Exception("Lepton branch %s not defined!" % (self.Lepton))
        if len(self.hists) == 0:
            raise Exception("No correction histograms are loaded!")

        leptons = Collection(event, self.Lepton)

        weights = []
        ups = []
        downs = []
        period = event.MCEra if hasattr(event, "MCEra") else 0
        period = min(period, len(self.hists) - 1)
        for lepton in leptons:
            weight, up, down = self.get_weight(period, lepton)
            weights.append(weight)
            ups.append(up)
            downs.append(down)
        self.out.fillBranch("%s_%s_wt"   % (self.Lepton, self.Correction), weights)
        self.out.fillBranch("%s_%s_up"   % (self.Lepton, self.Correction), ups    )
        self.out.fillBranch("%s_%s_down" % (self.Lepton, self.Correction), downs  )
            
        return True


