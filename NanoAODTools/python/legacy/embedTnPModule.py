import ROOT
import math
import time

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class exampleProducer(Module):
    def __init__(self,runningEra, maxEvents, startEvent, isData):
        self.runningEra = runningEra
        self.maxEvents = maxEvents #for quick local testing
        self.startEvent = startEvent
        self.isData = isData
        self.seen = 0
        self.passed = 0
        self.muonPassed = 0
        self.elecPassed = 0
        self.probe_passed = 0
        self.probe_failed = 0
        self.failTrigMap = 0
        self.negativeEvents = 0
        if self.maxEvents == 1:
            self.verbose = 20
        elif self.maxEvents > 0 and self.maxEvents < 20:
            self.verbose = 10
        elif self.maxEvents > 0 and self.maxEvents < 100:
            self.verbose = 5
        elif self.maxEvents > 0 and self.maxEvents < 1000:
            self.verbose = 2
        else:
            self.verbose = 1
        # self.tnpTree = ROOT.TTree("fitter_tree", "TnP Tree")
        pass
    def beginJob(self):
        self.beginTime = time.clock()
        pass
    def endJob(self):
        print "Passed", self.passed, "from", (self.seen-self.startEvent+1), "events processed", self.muonPassed, "muon events and", self.elecPassed, "electron events"
        print "Found", self.failTrigMap, "events that failed trigger matching requirements"
        # if self.probe_passed > 0 or self.probe_failed > 0:
        #     print "Probes passed", self.probe_passed, "probes failed", self.probe_failed, "efficiency", (self.probe_passed) * 1. / (self.probe_failed + self.probe_passed)
        # else :
        #     print "No events to probe, so no efficiency estimate!"
        print "Processing took", time.clock()-self.beginTime, "seconds"
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        # outputFile.SetCompressionLevel(0) #don't compress to speed up processing and reduce memory (?)
        self.out = wrappedOutputTree
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

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        outputFile.cd()
        h = ROOT.TH1D("events", "events", 10, 1, 11)
        h.Fill(1.5 , self.seen)
        h.Fill(2.5 , self.passed)
        h.Fill(10.5, self.negativeEvents)
        h.Write()
        pass

    def check_trig(self, trigObjs, lepton, isMuon):
        if isMuon :
            bit_1 = 1#3 #2 #Iso 1 muon
            bit_2 = 10 # bit_1 # 1024 #Mu50
        else :
            if self.runningEra == 1:
                bit_1 = 10 #1024 #32_L1DoubleEG_AND_L1SingleEGOr
                bit_2 = bit_1 #no second trigger
            else :
                bit_1 = 1 #2 # WPTight 1 ele
                bit_2 = bit_1 # no second trigger
        deltaR_match = 0.2
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
            passBit1 = trigObj.filterBits & (1<<bit_1) != 0
            passBit2 = trigObj.filterBits & (1<<bit_2) != 0
            if self.verbose > 9:
                print "  Trigger object", i_trig, "for",name,"has filterBits", trigObj.filterBits, "pt, eta, phi =", trigObj.pt, trigObj.eta, trigObj.phi
            if passBit1 or passBit2:
                if self.verbose > 9:
                    print "   Trigger object", i_trig,"passed bit check, trig pt =", trigObj.pt, "lepton pt =", lepton.pt
                if abs(lepton.pt - trigObj.pt) < deltaPt_match*lepton.pt:
                    deltaEta = abs(lepton.eta - trigObj.eta)
                    deltaPhi = abs(lepton.phi - trigObj.phi)
                    if deltaPhi > math.pi:
                        deltaPhi = abs(2*math.pi - deltaPhi)
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

    # electron ID check
    def elec_id(self, electron, WP):
        if WP == 0: 
            return True
        elif WP == 1:
            return electron.mvaFall17V2Iso_WPL
        elif WP == 2:
            return electron.mvaFall17V2Iso_WP80
        elif WP == 3:
            return electron.mvaFall17V2Iso_WP90
        return False

    # muon ID check
    def muon_id(self, muon, ID, IsoID):
        passed = (ID == 0 or
                  (ID == 1 and muon.looseId) or
                  (ID == 2 and muon.mediumId) or
                  (ID == 3 and muon.tightId))
        passed = passed and muon.pfRelIso04_all < IsoID
        return passed

    # ee/mumu selection check
    def sameflavor_check(self, indices, leptons, is_mumu, min_mass_cut, max_mass_cut, trig_pt, id_id, iso_id):
        nLep = len(indices)
        for i in range(nLep):
            for j in range(i+1, nLep):
                lep_1 = leptons[indices[i]]
                lep_2 = leptons[indices[j]]
                if lep_1.pt < trig_pt and lep_2.pt < trig_pt:
                    continue
                lep_mass = (lep_1.p4() + lep_2.p4()).M()
                if lep_mass < min_mass_cut or lep_mass > max_mass_cut:
                    continue
                if is_mumu:
                    if not self.muon_id(lep_1, id_id, iso_id) or not self.muon_id(lep_1, id_id, iso_id):
                        continue
                else :
                    if not self.elec_id(lep_1, id_id) or not self.elec_id(lep_2, id_id):
                        continue
                #Accept the event
                return True, indices[i], indices[j]

        return False, -1, -1

    def fill_branches(self, one, two, isMuons):
        self.out.fillBranch("pair_mass"      , (one.p4() + two.p4()).M())
        self.out.fillBranch("pair_pt"        , (one.p4() + two.p4()).Pt())
        self.out.fillBranch("pair_eta"       , (one.p4() + two.p4()).Eta())
        self.out.fillBranch("one_pt"         , one.pt)
        self.out.fillBranch("one_eta"        , one.eta)
        if not isMuons:
            self.out.fillBranch("one_sc_eta"     , one.eta + one.deltaEtaSC)
        else :
            self.out.fillBranch("one_sc_eta"     , one.eta)
        self.out.fillBranch("one_phi"        , one.phi)
        self.out.fillBranch("one_q"          , one.charge)
        self.out.fillBranch("two_pt"         , two.pt)
        self.out.fillBranch("two_eta"        , two.eta)
        if not isMuons:
            self.out.fillBranch("two_sc_eta"     , two.eta + two.deltaEtaSC)
        else :
            self.out.fillBranch("two_sc_eta"     , two.eta)
        self.out.fillBranch("two_phi"        , two.phi)
        self.out.fillBranch("two_q"          , two.charge)

    # Main processing loop
    def analyze(self, event):
        ############################
        #     Begin event loop     #
        ############################
        #increment event count
        self.seen = self.seen + 1
        #record negative events for proper normalization
        if self.isData == 0 and event.genWeight < 0.:
            self.negativeEvents = self.negativeEvents + 1
        if(self.startEvent > self.seen): #continue until reach desired starting point
            return False
        if(self.startEvent > 1 and self.startEvent == self.seen):
            print "***Found starting event", self.startEvent
        if(self.maxEvents > 0 and self.seen-self.startEvent >= self.maxEvents) : #exit if processed maximum events
            print "Processed the maximum number of events,", self.maxEvents
            self.endJob()
            exit()        
        if self.verbose > 9:
            print "***Processing event", self.seen
            
        """process event, return True (go to next module) or False (fail, go to next event)"""
        HLT       = Object    (event, "HLT")
        electrons = Collection(event, "Electron")
        muons     = Collection(event, "Muon")
        PuppiMET  = Object    (event, "PuppiMET")
        trigObjs  = Collection(event, "TrigObj")

        # Need at least 2 electrons or 2 electrons for tag and probe
        if(len(electrons) < 2 and len(muons) < 2):
            return False

        ############################
        #    Trigger parameters    #
        ############################
        doTriggerMatching = True #whether or not to require the matched trigger
        
        minmupt     = 25. # muon trigger
        minelept    = 33. # electron trigger
        if self.runningEra == 0 :
            minelept = 28. #lower pT electron trigger in 2016
        elif self.runningEra == 1 :
            minmupt = 28. #higher pT muon trigger in 2017

        ## Non-trigger lepton parameters ##
        minmuptlow  = 10.
        mineleptlow = 10.

        
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

        ## selection parameters ##
        maxMET      = -1. # < 0 to apply no cut
        minLepM     = 60. # generator only went down to 50 GeV/c^2
        maxLepM     = 130.        
        eleId       = 2 #0 = none 1 = WPL, 2 = WP80, 3 = WP90
        muonId      = 3 # 0 = no cut 1 = loose, 2 = medium, 3 = tight
        muonIso     = muonIsoTight

        ############################
        #     Veto object IDs      #
        ############################

        # muons
        minmupt_count = 10. # 3 GeV/c threshold in nanoAOD
        muonIso_count = 100. #no cut
        muonId_count = 0 # 0 = no cut 1 = loose, 2 = medium, 3 = tight
        max_muon_eta = 2.4
        # electrons
        minelept_count = mineleptlow # 5 GeV/c threshold in nanoAOD, but set it to be the trigger threshold used in the analysis
        eleId_count = 0 #0 = none 1 = WPL, 2 = WP80, 3 = WP90        
        max_ele_eta = 2.5

        ############################
        #     Begin selections     #
        ############################
        
        ### initial filtering ###
        if maxMET > 0 and PuppiMET.pt > maxMET : #cut high MET events
            return False

        ############################
        #    Trigger selection     #
        ############################
        ### check which triggers are fired ###
        muonTriggered = False
        muonLowTriggered = False
        muonHighTriggered = False
        electronTriggered = False        
        if self.runningEra == 0 :
            muonLowTriggered = HLT.IsoMu24
            muonHighTriggered = HLT.Mu50
            electronTriggered = HLT.Ele27_WPTight_Gsf
        elif self.runningEra == 1 :
            muonLowTriggered = HLT.IsoMu27
            muonHighTriggered = HLT.Mu50
            electronTriggered = HLT.Ele32_WPTight_Gsf_L1DoubleEG
        elif self.runningEra == 2 :
            muonLowTriggered = HLT.IsoMu24
            muonHighTriggered = HLT.Mu50
            electronTriggered = HLT.Ele32_WPTight_Gsf
        muonTriggered = muonLowTriggered or muonHighTriggered
        if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
            print "Event", self.seen, "muonTriggered =",muonTriggered,"electronTriggered =",electronTriggered
        #require a trigger
        if not muonTriggered and not electronTriggered :
            return False
        
        ############################
        #     Count electrons      #
        ############################

        nElectrons = 0
        nMuons = 0
        elec_dict = dict() # save a dictionary to find the objects again
        muon_dict = dict()

        if (self.verbose > 9 and self.seen % 10 == 0) or self.verbose > 10:
            print "Event", self.seen, ": printing electron info..."
        for index in range(len(electrons)) :
            ele_sc_eta = math.fabs(electrons[index].eta + electrons[index].deltaEtaSC)
            if(self.verbose > 9 and self.seen % 10 == 0) or self.verbose > 10:
                print " Electron", index, "pt =", electrons[index].pt, "SC eta =", ele_sc_eta, \
                    "WPL =", electrons[index].mvaFall17V2Iso_WPL, \
                    "WP80 =", electrons[index].mvaFall17V2Iso_WP80, \
                    "WP90 =", electrons[index].mvaFall17V2Iso_WP90 
            if (electrons[index].pt > minelept_count and  ele_sc_eta < max_ele_eta
                and (ele_sc_eta < 1.442 or ele_sc_eta > 1.566)
                and self.elec_id(electrons[index], eleId_count)) :
                elec_dict[nElectrons] = index
                nElectrons = nElectrons + 1

        ############################
        #       Count muons        #
        ############################
        if(self.verbose > 9 and self.seen % 10 == 0) or self.verbose > 10:
            print "Event", self.seen, ": printing muon info..."
        for index in range(len(muons)) :
            if(self.verbose > 9 and self.seen % 10 == 0) or self.verbose > 10:
                print " Muon", index, "pt =", muons[index].pt, "IDL =", muons[index].looseId, "IDM =", muons[index].tightId, \
                    "IDT =", muons[index].tightId, "iso = ", muons[index].pfRelIso04_all 
            if (muons[index].pt > minmupt_count and
                abs(muons[index].eta) < max_muon_eta and
                self.muon_id(muons[index], muonId_count, muonIso_count)) :
                #FIXME: Add dxy, dz cuts
                muon_dict[nMuons] = index
                nMuons = nMuons + 1

        if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
            print "Event",self.seen,"nelectron (N before IDs) =",nElectrons,"(", len(electrons),") nmuon (N before IDs) =",nMuons,"(", len(muons),") "
            
        if not ((nElectrons == 2 and nMuons == 0) or (nMuons == 2 and nElectrons == 0)): #exactly two electrons or muons, no extras
            return False

        doMuons = (nMuons == 2)
        
        ####################################
        #  Check leptons against triggers  #
        ####################################

        leptonOneTriggered = False
        leptonTwoTriggered = False
        if doTriggerMatching:
            if doMuons :
                muonTrig = False
                #check if a selected muon matches with the muon triggers of interest
                if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
                    print "Event", self.seen, ": printing muon trigger info..."
                for i_muon in range(nMuons):
                    hasFired = self.check_trig(trigObjs, muons[muon_dict[i_muon]], True)
                    if hasFired > 0:
                        muonTrig  = True
                        if i_muon == 0 :
                            leptonOneTriggered = True
                        else :
                            leptonTwoTriggered = True
                    if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
                        print " Muon",i_muon,"has hasFired =",hasFired
            else :
                electronTriggered = False
                if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
                    print "Event", self.seen, ": printing electron trigger info..."
                for i_elec in range(nElectrons):
                    hasFired = self.check_trig(trigObjs, electrons[elec_dict[i_elec]], False)
                    if hasFired > 0:
                        electronTriggered = True
                        if i_elec == 0 :
                            leptonOneTriggered = True
                        else :
                            leptonTwoTriggered = True
                    if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
                        print " Electron", i_elec, "has hasFired =", hasFired

        if self.verbose > 0 and not leptonOneTriggered and not leptonTwoTriggered:
            print "Event", self.seen, "has triggered value changed after mapping! There are", nElectrons, "electrons and ", nMuons, " muons"
        
        if not leptonOneTriggered and not leptonTwoTriggered:
            self.failTrigMap = self.failTrigMap + 1
            return False

        if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
            print " Event", self.seen, "passed trigger matching"

        ############################
        #   Check each selection   #
        ############################

        ## check if the event passes each selection ##
        ee    = not doMuons
        mumu  = doMuons

        ## store selected lepton info ##
        leptonOneIndex  = -1
        leptonOneFlavor = 0
        leptonTwoIndex  = -1
        leptonTwoFlavor = 0
        
        ############################
        #         Mu+Mu            #
        ############################

        if doMuons :
            # mumu, leptonOneIndex, leptonTwoIndex = self.sameflavor_check(muon_dict, muons, True, minLepM, maxLepM, minmupt, muonId_count, muonIso_count)
            # if mumu: #accepted
            leptonOneIndex = muon_dict[0]
            leptonTwoIndex = muon_dict[1]
            if leptonOneIndex == leptonTwoIndex:
                print "!!! Warning!",self.seen, "returned the same index values for the EE selection!"
            lep1 = muons[leptonOneIndex]
            lep2 = muons[leptonTwoIndex]
            leptonOneFlavor = lep1.charge*-13
            leptonTwoFlavor = lep2.charge*-13
            mumu = mumu and lep1.pt > minmuptlow and lep2.pt > minmuptlow
            mumu = mumu and (self.muon_id(lep1, muonId, muonIso) or self.muon_id(lep2, muonId, muonIso)) #at least one must pass tight ID
            # mumu = mumu and (self.muon_id(lep1, muonId, muonIso_count) or self.muon_id(lep1, muonId_count, muonIso)) #can't fail both tight IDs
            # mumu = mumu and (self.muon_id(lep2, muonId, muonIso_count) or self.muon_id(lep2, muonId_count, muonIso)) #can't fail both tight IDs

        ############################
        #           E+E            #
        ############################

        if not doMuons :
            # ee, leptonOneIndex, leptonTwoIndex = self.sameflavor_check(elec_dict, electrons, False, minLepM, maxLepM, minelept, eleId_count, 0)
            # if ee: #accepted
            leptonOneIndex = elec_dict[0]
            leptonTwoIndex = elec_dict[1]
            if leptonOneIndex == leptonTwoIndex:
                print "!!! Warning!",self.seen, "returned the same index values for the EE selection!"
            lep1 = electrons[leptonOneIndex]
            lep2 = electrons[leptonTwoIndex]
            leptonOneFlavor = lep1.charge*-11
            leptonTwoFlavor = lep2.charge*-11
            ee = ee and lep1.pt > mineleptlow and lep2.pt > mineleptlow
            ee = ee and (self.elec_id(lep1, eleId) or self.elec_id(lep2, eleId)) #at least one must pass the tight ID

        # must pass a selection
        if not ee and not mumu:
            if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
                print " Event", self.seen, "failed selection requirements"
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

        ## Filter by charge ##
        if leptonOneFlavor*leptonTwoFlavor > 0:
            return False

        if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
            print "passing event", self.seen

        ############################
        #      Accept event        #
        ############################

        self.out.fillBranch("nElectrons", nElectrons)
        self.out.fillBranch("nMuons", nMuons)
        self.out.fillBranch("event_met_pfmet", PuppiMET.pt)
        self.fill_branches(lep1, lep2, doMuons)
        self.out.fillBranch("one_triggered", leptonOneTriggered)
        self.out.fillBranch("two_triggered", leptonTwoTriggered)

        if doMuons :
            self.out.fillBranch("one_id1", lep1.looseId + lep1.mediumId + lep1.tightId)
            self.out.fillBranch("one_id2", ((lep1.pfRelIso04_all < muonIsoVVLoose) + (lep1.pfRelIso04_all < muonIsoVLoose) +
                                            (lep1.pfRelIso04_all < muonIsoLoose )  +
                                            (lep1.pfRelIso04_all < muonIsoMedium)  + (lep1.pfRelIso04_all < muonIsoTight) +
                                            (lep1.pfRelIso04_all < muonIsoVTight)  + (lep1.pfRelIso04_all < muonIsoVVTight)))
            self.out.fillBranch("two_id1", lep2.looseId + lep2.mediumId + lep2.tightId)
            self.out.fillBranch("two_id2", ((lep2.pfRelIso04_all < muonIsoVVLoose) + (lep2.pfRelIso04_all < muonIsoVLoose) +
                                            (lep2.pfRelIso04_all < muonIsoLoose )  +
                                            (lep2.pfRelIso04_all < muonIsoMedium)  + (lep2.pfRelIso04_all < muonIsoTight) +
                                            (lep2.pfRelIso04_all < muonIsoVTight)  + (lep2.pfRelIso04_all < muonIsoVVTight)))
        else :
            self.out.fillBranch("one_id1", lep1.mvaFall17V2Iso_WPL + lep1.mvaFall17V2Iso_WP90 + lep1.mvaFall17V2Iso_WP80)
            self.out.fillBranch("one_id2", 0)
            self.out.fillBranch("two_id1", lep2.mvaFall17V2Iso_WPL + lep2.mvaFall17V2Iso_WP90 + lep2.mvaFall17V2Iso_WP80)
            self.out.fillBranch("two_id2", 0)
            if ((lep1.mvaFall17V2Iso_WP80 and (not lep1.mvaFall17V2Iso_WPL or not lep1.mvaFall17V2Iso_WP90))
                or (lep1.mvaFall17V2Iso_WP90 and not lep1.mvaFall17V2Iso_WPL)):
                print "Event", seen, "electron 1 IDs not sensible! WPL =", lep1.mvaFall17V2Iso_WPL, "WP90 =", lep1.mvaFall17V2Iso_WP90, "WP80 =", lep1.mvaFall17V2Iso_WP80
            if ((lep2.mvaFall17V2Iso_WP80 and (not lep2.mvaFall17V2Iso_WPL or not lep2.mvaFall17V2Iso_WP90))
                or (lep2.mvaFall17V2Iso_WP90 and not lep2.mvaFall17V2Iso_WPL)):
                print "Event", seen, "electron 2 IDs not sensible! WPL =", lep2.mvaFall17V2Iso_WPL, "WP90 =", lep2.mvaFall17V2Iso_WP90, "WP80 =", lep2.mvaFall17V2Iso_WP80

        # increment selection counts
        self.passed = self.passed + 1
        if doMuons :
            self.muonPassed = self.muonPassed + 1
        else :
            self.elecPassed = self.elecPassed + 1
        # if leptonOneTriggered and leptonTwoTriggered :
        #     self.probe_passed = self.probe_passed + 2 #each passes the others probe check
        # else :
        #     self.probe_failed = self.probe_failed + 1 #only 1 tag, so 1 probe failure

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
leptonConstr = lambda runningEra, maxEvents, startEvent, isData : exampleProducer(runningEra, maxEvents, startEvent, isData)
