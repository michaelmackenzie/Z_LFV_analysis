from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import os, math
import numpy as np
import itertools

ROOT.PyConfig.IgnoreCommandLineOptions = True

_rootLeafType2rootBranchType = {'UChar_t': 'b', 'Char_t': 'B', 'UInt_t': 'i','Int_t': 'I','Float_t': 'F', 'Double_t': 'D', 'ULong64_t': 'l', 'Long64_t': 'L', 'Bool_t': 'O'}


class EmbeddingUnfolding(Module):
    def __init__(self, year, branch = "GenZll", use_ic = True):
        self.year = year
        self.branch = branch
        self.use_ic = use_ic

        file = os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/embed/"
        if use_ic: file += "htt_ic_scalefactors_legacy_%s.root" % (year)
        else:      file += "htt_scalefactors_legacy_%s.root"    % (year)

        self.file = ROOT.TFile(file, "READ")
        if self.file.IsZombie(): raise Exception("Embedding unfolding file not found!")

        # Retrieve the RooWorkspace
        self.workspace = self.file.Get('w')

        # Retrieve the unfolding functions
        if use_ic:
            self.trigger = self.workspace.obj('m_sel_trg_ic_ratio')
            self.id      = self.workspace.obj('m_sel_id_ic_ratio')
        elif year == '2016':
            self.trigger = self.workspace.obj('m_sel_trg_kit_ratio')
            self.id      = self.workspace.obj('m_sel_idEmbratio')
        else:
            self.trigger = self.workspace.obj('m_sel_trg_ratio')
            self.id      = self.workspace.obj('m_sel_idEmbratio')

        # Retrieve the unfolding variables, the gen-level tau info
        self.gen_pt    = self.workspace.var(  'gt_pt')
        self.gen_pt_1  = self.workspace.var( 'gt1_pt')
        self.gen_pt_2  = self.workspace.var( 'gt2_pt')
        self.gen_eta   = self.workspace.var( 'gt_eta')
        self.gen_eta_1 = self.workspace.var('gt1_eta')
        self.gen_eta_2 = self.workspace.var('gt2_eta')

        if not self.trigger or not self.id:
            raise Exception('Embedding unfolding unable to find workspace functions')
        if not self.gen_pt or not self.gen_pt_1 or not self.gen_pt_2:
            raise Exception('Embedding unfolding unable to find workspace pt variables')
        if not self.gen_eta or not self.gen_eta_1 or not self.gen_eta_2:
            raise Exception('Embedding unfolding unable to find workspace eta variables')

        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):        
        self.out = wrappedOutputTree
        self.out.branch("EmbeddingUnfolding",'F')

        pass
 

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        weight = 1.

        # Retrieve the gen-tau info
        if not hasattr(event, '%s_LepOne_pt' % (self.branch)):
            self.out.fillBranch("EmbeddingUnfolding",1.)
            return True
        gen_one_pt  = getattr(event, '%s_LepOne_pt'  % (self.branch))
        gen_one_eta = getattr(event, '%s_LepOne_eta' % (self.branch))
        gen_two_pt  = getattr(event, '%s_LepTwo_pt'  % (self.branch))
        gen_two_eta = getattr(event, '%s_LepTwo_eta' % (self.branch))

        # Unfold the trigger
        self.gen_pt_1.setVal(gen_one_pt )
        self.gen_eta_1.setVal(gen_one_eta)
        self.gen_pt_2.setVal(gen_two_pt )
        self.gen_eta_2.setVal(gen_two_eta)
        trig_wt = self.trigger.evaluate()

        # Unfold the muon ID selection for each gen tau
        self.gen_pt.setVal(gen_one_pt )
        self.gen_pt.setVal(gen_one_eta)
        id_1 = self.id.evaluate()
        self.gen_pt.setVal(gen_two_pt )
        self.gen_pt.setVal(gen_two_eta)
        id_2 = self.id.evaluate()

        #unfolding efficiencies --> can't be smaller than 1
        weight = max(1., trig_wt) * max(1., id_1) * max(1., id_2)
        if weight > 5.:
            print "Large unfolding weight = %.2f: trig = %.2f, id(1) = %.2f, id(2) = %.2f" % (weight, trig_wt, id_1, id_2)
            print " Inputs: pt(1) = %.1f, eta(1) = %.2f, pt(2) = %.1f, eta(2) = %.2f" % (gen_one_pt, gen_one_eta, gen_two_pt, gen_two_eta)
            weight = 1.
        

        self.out.fillBranch("EmbeddingUnfolding",weight)
        return True


