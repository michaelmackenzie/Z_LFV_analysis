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


class EGammaTnPFilter(Module):
    def __init__(self, year, verbose=0):
        self.year = year
        self.verbose = verbose
        self.seen = 0
        self.passed = 0
        pass

    def beginJob(self):
        pass

    def endJob(self):
        print "EGammaTnPFilter: Saw %i events, accepted %i events" % (self.seen, self.passed)
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("pair_mass"           , "F");
        self.out.branch("pair_pt"             , "F");
        self.out.branch("pair_eta"            , "F");
        self.out.branch("nElectrons"          , "I"); # number of accepted electrons
        self.out.branch("event_met_pfmet"     , "F");
        self.out.branch("one_pt"              , "F");
        self.out.branch("one_eta"             , "F");
        self.out.branch("one_sc_eta"          , "F");
        self.out.branch("one_phi"             , "F");
        self.out.branch("one_q"               , "F");
        self.out.branch("one_triggered"       , "O");
        self.out.branch("one_id1"             , "I");
        self.out.branch("one_id2"             , "I");
        self.out.branch("two_pt"              , "F");
        self.out.branch("two_eta"             , "F");
        self.out.branch("two_sc_eta"          , "F");
        self.out.branch("two_phi"             , "F");
        self.out.branch("two_q"               , "F");
        self.out.branch("two_triggered"       , "O");
        self.out.branch("two_id1"             , "I");
        self.out.branch("two_id2"             , "I");
        pass
 

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def check_trig(self, trigObjs, lepton, isMuon):
        if self.year == 2017:
            bit_1 = 10 # 32_L1DoubleEG_AND_L1SingleEGOr
            bit_2 = bit_1 # no second trigger
        else :
            bit_1 = 1 # WPTight 1 ele
            bit_2 = bit_1 # no second trigger
        deltaR_match = 0.2
        deltaPt_match = 10 #fractional match, > ~5 --> no pT matching
        result = 0
        passedBit1 = False
        passedBit2 = False
        pdg = 11
        name = "an Electron"
        if self.verbose > 9:
            print " Event", self.seen, ": Printing trigger object info for matching to a lepton with bits", (1<<bit_1), "and", (1<<bit_2)
            print " lepton pt, eta, phi =", lepton.pt, lepton.eta, lepton.phi
        for i_trig in range(len(trigObjs)):
            trigObj = trigObjs[i_trig]
            if abs(trigObj.id) != pdg:
                continue
            passBit1 = trigObj.filterBits & (1<<bit_1) != 0
            passBit2 = trigObj.filterBits & (1<<bit_2) != 0
            if self.verbose > 9:
                print "  Trigger object", i_trig, "for",name,"has filterBits", trigObj.filterBits, "pt, eta, phi =", trigObj.pt, trigObj.eta, trigObj.phi
            if passBit1 or passBit2:
                if self.verbose > 9:
                    print "   Trigger object", i_trig,"passed bit check, trig pt =", trigObj.pt, "lepton pt =", lepton.pt
                if math.fabs(lepton.pt - trigObj.pt) < deltaPt_match*lepton.pt:
                    deltaEta = math.fabs(lepton.eta - trigObj.eta)
                    deltaPhi = math.fabs(lepton.phi - trigObj.phi)
                    if deltaPhi > math.pi:
                        deltaPhi = math.fabs(2*math.pi - deltaPhi)
                    if self.verbose > 9:
                        print "    Trigger object passed pt check, trig eta, phi =", trigObj.eta, "," , trigObj.phi,\
                            "lepton eta, phi =", lepton.eta, ",", lepton.phi
                    deltaR = math.sqrt(deltaEta*deltaEta + deltaPhi*deltaPhi)
                    if deltaR < deltaR_match:
                        if self.verbose > 2:
                            print " Event",self.seen, "Trigger object",i_trig,"passed matching, pass bit1 =", passBit1, "pass bit2 =", passBit2
                        result = 1
                        return result
        return 0

    def fill_branches(self, one, two):
        self.out.fillBranch("pair_mass"      , (one.p4() + two.p4()).M())
        self.out.fillBranch("pair_pt"        , (one.p4() + two.p4()).Pt())
        self.out.fillBranch("pair_eta"       , (one.p4() + two.p4()).Eta())
        self.out.fillBranch("one_pt"         , one.pt)
        self.out.fillBranch("one_eta"        , one.eta)
        self.out.fillBranch("one_sc_eta"     , one.eta + one.deltaEtaSC)
        self.out.fillBranch("one_phi"        , one.phi)
        self.out.fillBranch("one_q"          , one.charge)
        self.out.fillBranch("one_id1"        , one.mvaFall17V2noIso_WPL + one.mvaFall17V2noIso_WP90 + one.mvaFall17V2noIso_WP80)
        self.out.fillBranch("one_id2"        , one.pfRelIso03_all < 0.5 + one.pfRelIso03_all < 0.15)
        self.out.fillBranch("two_pt"         , two.pt)
        self.out.fillBranch("two_eta"        , two.eta)
        self.out.fillBranch("two_sc_eta"     , two.eta + two.deltaEtaSC)
        self.out.fillBranch("two_phi"        , two.phi)
        self.out.fillBranch("two_q"          , two.charge)
        self.out.fillBranch("two_id1"        , two.mvaFall17V2noIso_WPL + two.mvaFall17V2noIso_WP90 + two.mvaFall17V2noIso_WP80)
        self.out.fillBranch("two_id2"        , two.pfRelIso03_all < 0.5 + two.pfRelIso03_all < 0.15)

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        self.seen = self.seen + 1
        if self.verbose > 9:
            print "***Processing event", self.seen

        electrons  = Collection(event, "Electron")
        HLT        = Object    (event, "HLT"     )
        PuppiMET   = Object    (event, "PuppiMET")
        trigObjs   = Collection(event, "TrigObj" )

        nElectrons = len(electrons)

        # require exactly two electrons
        if not nElectrons == 2:
            return False


        #Check triggers
        electronTriggered = False
        elec_trig_pt      = 33.
        if self.year == "2016":
            electronTriggered = HLT.Ele27_WPTight_Gsf
            elec_trig_pt = 28.
        elif self.year == "2017":
            electronTriggered = HLT.Ele32_WPTight_Gsf_L1DoubleEG
        elif self.year == "2018":
            electronTriggered = HLT.Ele32_WPTight_Gsf

        # if the correct trigger didn't fire, reject the event
        if not electronTriggered:
            return False

        ####################################
        #  Check leptons against triggers  #
        ####################################

        leptonOneTriggered = False
        leptonTwoTriggered = False
        #check if a selected electron matches with the electron triggers of interest
        if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
            print "Event", self.seen, ": printing electron trigger info..."
        leptonOneTriggered = self.check_trig(trigObjs, electrons[0], False)
        leptonTwoTriggered = self.check_trig(trigObjs, electrons[1], False)
        if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
            print " Electron 1 has trigger status =", leptonOneTriggered
            print " Electron 2 has trigger status =", leptonTwoTriggered

        if self.verbose > 0 and not leptonOneTriggered and not leptonTwoTriggered:
            print "Event", self.seen, "has triggered value changed after mapping! There are", nElectrons, "electrons and ", nMuons, " muons"

        # Reject the event if neither lepton is matched to a trigger
        if not leptonOneTriggered and not leptonTwoTriggered:
            return False


        ############################
        #  Additional filtering    #
        ############################

        lep1 = electrons[0]
        lep2 = electrons[1]

        #check for opposite-signed
        if lep1.charge*lep2.charge > 0:
            return False
            
        ## Filter by mass range ##
        lep_mass = (lep1.p4() + lep2.p4()).M()
        if lep_mass < 60. or lep_mass > 130.:
            return False
        delta_r = lep1.p4().DeltaR(lep2.p4())
        if delta_r < 0.3:
            return False

        ############################
        #      Accept event        #
        ############################

        if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
            print "passing event", self.seen


        self.out.fillBranch("nElectrons", nElectrons)
        self.out.fillBranch("event_met_pfmet", PuppiMET.pt)
        self.fill_branches(lep1, lep2)
        self.out.fillBranch("one_triggered", leptonOneTriggered)
        self.out.fillBranch("two_triggered", leptonTwoTriggered)

        # increment selection counts
        self.passed = self.passed + 1

        #Accept the event
        return True
