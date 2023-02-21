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


class EmbeddingTnPFilter(Module):
    def __init__(self, year, verbose=0):
        self.year = year
        self.verbose = verbose
        self.seen = 0
        self.passed = 0
        pass

    def beginJob(self):
        pass

    def endJob(self):
        print "EmbeddingTnPFilter: Saw %i events, accepted %i events" % (self.seen, self.passed)
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("pair_ismuon"         , "O");
        self.out.branch("pair_mass"           , "F");
        self.out.branch("pair_pt"             , "F");
        self.out.branch("pair_eta"            , "F");
        self.out.branch("nElectrons"          , "I"); # number of accepted electrons
        self.out.branch("nMuons"              , "I"); # number of accepted muons
        self.out.branch("event_met_pfmet"     , "F");
        self.out.branch("one_pt"              , "F");
        self.out.branch("one_eta"             , "F");
        self.out.branch("one_sc_eta"          , "F");
        self.out.branch("one_phi"             , "F");
        self.out.branch("one_q"               , "F");
        self.out.branch("one_ecorr"           , "F");
        self.out.branch("one_triggered"       , "O");
        self.out.branch("one_id1"             , "I");
        self.out.branch("one_id2"             , "I");
        self.out.branch("two_pt"              , "F");
        self.out.branch("two_eta"             , "F");
        self.out.branch("two_sc_eta"          , "F");
        self.out.branch("two_phi"             , "F");
        self.out.branch("two_q"               , "F");
        self.out.branch("two_ecorr"           , "F");
        self.out.branch("two_triggered"       , "O");
        self.out.branch("two_id1"             , "I");
        self.out.branch("two_id2"             , "I");
        pass
 

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def check_trig(self, trigObjs, lepton, isMuon):
        if isMuon :
            bit_1 = 1 #IsoMu
            bit_2 = bit_1 # no second trigger
            pt_min_1 = 27. if self.year == "2017" else 24.
            pt_min_2 = pt_min_1
        else :
            if self.year == "2017":
                bit_1 = 10 # 32_L1DoubleEG_AND_L1SingleEGOr
                bit_2 = bit_1 # no second trigger
            else :
                bit_1 = 1 # WPTight 1 ele
                bit_2 = bit_1 # no second trigger
            pt_min_1 = 27. if self.year == "2016" else 32.
            pt_min_2 = pt_min_1
        deltaR_match = 0.1
        deltaPt_match = 10 #fractional match, > ~5 --> no pT matching
        result = 0
        passedBit1 = False
        passedBit2 = False
        pdg = 13
        name = "a Muon"
        if not isMuon:
            pdg = 11
            name = "an Electron"
        if self.verbose > 9:
            print " Event", self.seen, ": Printing trigger object info for matching to a lepton with bits", (1<<bit_1), "and", (1<<bit_2)
            print " lepton pt, eta, phi =", lepton.pt, lepton.eta, lepton.phi
        for i_trig in range(len(trigObjs)):
            trigObj = trigObjs[i_trig]
            if abs(trigObj.id) != pdg:
                continue
            passBit1 = (trigObj.filterBits & (1<<bit_1) != 0) and trigObj.pt > pt_min_1
            passBit2 = (trigObj.filterBits & (1<<bit_2) != 0) and trigObj.pt > pt_min_2
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

    def fill_branches(self, one, two, isMuons):
        self.out.fillBranch("pair_ismuon"    , isMuons)
        self.out.fillBranch("pair_mass"      , (one.p4() + two.p4()).M())
        self.out.fillBranch("pair_pt"        , (one.p4() + two.p4()).Pt())
        self.out.fillBranch("pair_eta"       , (one.p4() + two.p4()).Eta())
        self.out.fillBranch("one_pt"         , one.pt)
        self.out.fillBranch("one_eta"        , one.eta)
        if not isMuons:
            self.out.fillBranch("one_sc_eta"     , one.eta + one.deltaEtaSC)
            self.out.fillBranch("one_ecorr"      , one.eCorr)
        else :
            self.out.fillBranch("one_sc_eta"     , one.eta)
            self.out.fillBranch("one_ecorr"      , 0.)
        self.out.fillBranch("one_phi"        , one.phi)
        self.out.fillBranch("one_q"          , one.charge)
        self.out.fillBranch("two_pt"         , two.pt)
        self.out.fillBranch("two_eta"        , two.eta)
        if not isMuons:
            self.out.fillBranch("two_sc_eta"     , two.eta + two.deltaEtaSC)
            self.out.fillBranch("two_ecorr"      , two.eCorr)
        else :
            self.out.fillBranch("two_sc_eta"     , two.eta)
            self.out.fillBranch("two_ecorr"      , 0.)
        self.out.fillBranch("two_phi"        , two.phi)
        self.out.fillBranch("two_q"          , two.charge)

    # electron ID check
    def elec_id(self, electron, WP):
        if WP == 0: 
            return True
        elif WP == 1:
            return electron.mvaFall17V2noIso_WPL
        elif WP == 2:
            return electron.mvaFall17V2noIso_WP90
        elif WP == 3:
            return electron.mvaFall17V2noIso_WP80
        return False

    # muon ID check
    def muon_id(self, muon, ID, IsoID):
        passed = (ID == 0 or
                  (ID == 1 and muon.looseId ) or
                  (ID == 2 and muon.mediumId) or
                  (ID == 3 and muon.tightId ))
        passed = passed and muon.pfRelIso04_all < IsoID
        return passed

    def form_pairs(self, leptons):
        pairs = []
        nlep = len(leptons)
        min_mass = 60.
        max_mass = 130.
        for i in range(nlep-1):
            for j in range(i+1, nlep):
                lep1 = leptons[i]
                lep2 = leptons[j]
                if lep1.charge*lep2.charge > 0:
                    continue
                mass = (lep1.p4() + lep2.p4()).M()
                if mass < min_mass or mass > max_mass:
                    continue
                if lep1.p4().DeltaR(lep2.p4()) < 0.3:
                    continue
                pairs.append([i,j])
        return pairs
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        self.seen = self.seen + 1
        if self.verbose > 9:
            print "***Processing event", self.seen

        electrons  = Collection(event, "Electron")
        muons      = Collection(event, "Muon"    )
        HLT        = Object    (event, "HLT"     )
        PuppiMET   = Object    (event, "PuppiMET")
        trigObjs   = Collection(event, "TrigObj" )

        #count Z-like pairs
        electron_pairs = self.form_pairs(electrons)
        muon_pairs     = self.form_pairs(muons    )

        nElectrons = len(electrons     )
        nMuons     = len(muons         )
        nElePairs  = len(electron_pairs)
        nMuPairs   = len(muon_pairs    )

        # require exactly one muon or one electron Z pair
        if not ((nElePairs == 1 and nMuPairs != 1) or (nElePairs != 1 and nMuPairs == 1)):
            return False


        # determine if this is a di-muon or di-electron event
        doMuons = nMuPairs == 1
        lep1_index = muon_pairs[0][0] if doMuons else electron_pairs[0][0]
        lep2_index = muon_pairs[0][1] if doMuons else electron_pairs[0][1]

        #Check triggers
        electronTriggered = False
        muonTriggered     = False
        elec_trig_pt      = 33.
        muon_trig_pt      = 25.
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

        # if the correct trigger didn't fire, reject the event
        if not ((not doMuons and electronTriggered) or (doMuons and muonTriggered)):
            return False

        ####################################
        #  Check leptons against triggers  #
        ####################################

        leptonOneTriggered = False
        leptonTwoTriggered = False
        if doMuons :
            #check if a selected muon matches with the muon triggers of interest
            if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
                print "Event", self.seen, ": printing muon trigger info..."
            leptonOneTriggered = self.check_trig(trigObjs, muons[lep1_index], True)
            leptonTwoTriggered = self.check_trig(trigObjs, muons[lep2_index], True)
            if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
                print " Muon 1 has trigger status =", leptonOneTriggered
                print " Muon 2 has trigger status =", leptonTwoTriggered
        else :
            #check if a selected muon matches with the muon triggers of interest
            if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
                print "Event", self.seen, ": printing electron trigger info..."
            leptonOneTriggered = self.check_trig(trigObjs, electrons[lep1_index], False)
            leptonTwoTriggered = self.check_trig(trigObjs, electrons[lep2_index], False)
            if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
                print " Electron 1 has trigger status =", leptonOneTriggered
                print " Electron 2 has trigger status =", leptonTwoTriggered

        if self.verbose > 0 and not leptonOneTriggered and not leptonTwoTriggered:
            print "Event", self.seen, "has triggered value changed after mapping! There are", nElectrons, "electrons and ", nMuons, " muons"

        # Reject the event if neither lepton is matched to a trigger
        if not leptonOneTriggered and not leptonTwoTriggered:
            return False


        ############################
        #       Object IDs         #
        ############################


        ## muon isolation cut levels ##
        muonIsoVVLoose = 0.5
        muonIsoVLoose  = 0.4
        muonIsoLoose   = 0.25 #eff ~ 0.98
        muonIsoMedium  = 0.20
        muonIsoTight   = 0.15 #eff ~ 0.95
        muonIsoVTight  = 0.10
        muonIsoVVTight = 0.05

        ## tight ID selection parameters ##
        minLepM     = 60. # generator only went down to 50 GeV/c^2
        maxLepM     = 130.        
        eleId       = 2 # 0 = none 1 = WPL, 2 = WP90, 3 = WP80
        muonId      = 2 # 0 = no cut 1 = loose, 2 = medium, 3 = tight
        muonIso     = muonIsoTight

        ############################
        #   Check each selection   #
        ############################

        passed = True

        if doMuons:
            lep1 = muons[lep1_index]
            lep2 = muons[lep2_index]
            passed = passed and (self.muon_id(lep1, muonId, muonIso) or self.muon_id(lep2, muonId, muonIso)) #at least one must pass the tight ID
        else:
            lep1 = electrons[lep1_index]
            lep2 = electrons[lep2_index]
            passed = passed and (self.elec_id(lep1, eleId) or self.elec_id(lep2, eleId)) #at least one must pass the tight ID

        if not passed:
            return False

        #check for opposite-signed
        if lep1.charge*lep2.charge > 0:
            return False
            
        ############################
        #  Additional filtering    #
        ############################

        ## Filter by mass range ##
        lep_mass = (lep1.p4() + lep2.p4()).M()
        if lep_mass < minLepM or lep_mass > maxLepM:
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
        self.out.fillBranch("nMuons", nMuons)
        self.out.fillBranch("event_met_pfmet", PuppiMET.pt)
        self.fill_branches(lep1, lep2, doMuons)
        self.out.fillBranch("one_triggered", leptonOneTriggered)
        self.out.fillBranch("two_triggered", leptonTwoTriggered)

        if doMuons :
            self.out.fillBranch("one_id1", lep1.mediumId and math.fabs(lep1.dz) < 0.2 and math.fabs(lep1.dxy) < 0.5)
            self.out.fillBranch("one_id2", ((lep1.pfRelIso04_all < muonIsoVVLoose) + (lep1.pfRelIso04_all < muonIsoVLoose) +
                                            (lep1.pfRelIso04_all < muonIsoLoose )  +
                                            (lep1.pfRelIso04_all < muonIsoMedium)  + (lep1.pfRelIso04_all < muonIsoTight) +
                                            (lep1.pfRelIso04_all < muonIsoVTight)  + (lep1.pfRelIso04_all < muonIsoVVTight)))
            self.out.fillBranch("two_id1", lep2.mediumId and math.fabs(lep2.dz) < 0.2 and math.fabs(lep2.dxy) < 0.5)
            self.out.fillBranch("two_id2", ((lep2.pfRelIso04_all < muonIsoVVLoose) + (lep2.pfRelIso04_all < muonIsoVLoose) +
                                            (lep2.pfRelIso04_all < muonIsoLoose )  +
                                            (lep2.pfRelIso04_all < muonIsoMedium)  + (lep2.pfRelIso04_all < muonIsoTight) +
                                            (lep2.pfRelIso04_all < muonIsoVTight)  + (lep2.pfRelIso04_all < muonIsoVVTight)))
        else :
            self.out.fillBranch("one_id1", lep1.mvaFall17V2noIso_WP90 and math.fabs(lep1.dz) < 0.2 and math.fabs(lep1.dxy) < 0.5)
            #use muon Iso ID flag definitions for electron iso ID
            self.out.fillBranch("one_id2", ((lep1.pfRelIso03_all < muonIsoVVLoose) + (lep1.pfRelIso03_all < muonIsoVLoose) +
                                            (lep1.pfRelIso03_all < muonIsoLoose )  +
                                            (lep1.pfRelIso03_all < muonIsoMedium)  + (lep1.pfRelIso03_all < muonIsoTight) +
                                            (lep1.pfRelIso03_all < muonIsoVTight)  + (lep1.pfRelIso03_all < muonIsoVVTight)))
            self.out.fillBranch("two_id1", lep2.mvaFall17V2noIso_WP90 and math.fabs(lep2.dz) < 0.2 and math.fabs(lep2.dxy) < 0.5)
            #use muon Iso ID flag definitions for electron iso ID
            self.out.fillBranch("two_id2", ((lep2.pfRelIso03_all < muonIsoVVLoose) + (lep2.pfRelIso03_all < muonIsoVLoose) +
                                            (lep2.pfRelIso03_all < muonIsoLoose )  +
                                            (lep2.pfRelIso03_all < muonIsoMedium)  + (lep2.pfRelIso03_all < muonIsoTight) +
                                            (lep2.pfRelIso03_all < muonIsoVTight)  + (lep2.pfRelIso03_all < muonIsoVVTight)))

        # increment selection counts
        self.passed = self.passed + 1

        #Accept the event
        return True
