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
        print "Passed", self.passed, "from", (self.seen-self.startEvent+1), "events processed"
        print "Found", self.failTrigMap, "events that failed trigger matching requirements"
        if self.probe_passed > 0 or self.probe_failed > 0:
            print "Probes passed", self.probe_passed, "probes failed", self.probe_failed, "efficiency", (self.probe_passed) * 1. / (self.probe_failed + self.probe_passed)
        else :
            print "No events to probe, so no efficiency estimate!"
        print "Processing took", time.clock()-self.beginTime, "seconds"
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        # outputFile.SetCompressionLevel(0) #don't compress to speed up processing and reduce memory (?)
        self.out = wrappedOutputTree
        self.out.branch("pair_mass"           , "F");
        self.out.branch("pair_pt"             , "F");
        self.out.branch("pair_eta"            , "F");
        self.out.branch("nElectrons"          ,  "I"); # number of accepted electrons
        self.out.branch("event_met_pfmet"     , "F");
        self.out.branch("tag_Ele_pt"          , "F");
        self.out.branch("tag_Ele_eta"         , "F");
        self.out.branch("tag_sc_eta"          , "F");
        self.out.branch("tag_Ele_phi"         , "F");
        self.out.branch("tag_Ele_q"           , "F");
        self.out.branch("tag_Ele_ID"          , "I");
        # self.out.branch("tag_Ele_trigMVA"     , "F");
        # self.out.branch("tag_Ele_nonTrigMVA"  , "F");
        self.out.branch("probe_Ele_pt"        , "F");
        self.out.branch("probe_Ele_eta"       , "F");
        self.out.branch("probe_sc_eta"        , "F");
        self.out.branch("probe_Ele_phi"       , "F");
        self.out.branch("probe_Ele_q"         , "F");
        self.out.branch("probe_triggered"     , "O");
        self.out.branch("probe_Ele_ID"        , "I");
        # self.out.branch("probe_Ele_trigMVA"   , "F");
        # self.out.branch("probe_Ele_nonTrigMVA", "F");
        # print "Input tree:", inputTree, "Output tree:", wrappedOutputTree

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        outputFile.cd()
        h = ROOT.TH1D("events", "events", 10, 1, 11)
        h.Fill(1.5 , self.seen)
        h.Fill(2.5 , self.passed)
        h.Fill(10.5, self.negativeEvents)
        h.Write()
        pass

    def check_trig(self, trigObjs, lepton):
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
                        # passedBit1 = passedBit1 or passBit1
                        # passedBit2 = passedBit2 or passBit2
        return 0 #passedBit1 + 2*passedBit2

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

    def fill_branches(self, tag, probe, passed):
        self.out.fillBranch("pair_mass"      , (tag.p4() + probe.p4()).M())
        self.out.fillBranch("pair_pt"        , (tag.p4() + probe.p4()).Pt())
        self.out.fillBranch("pair_eta"       , (tag.p4() + probe.p4()).Eta())
        self.out.fillBranch("tag_Ele_pt"     , tag.pt)
        self.out.fillBranch("tag_Ele_eta"    , tag.eta)
        self.out.fillBranch("tag_sc_eta"     , tag.eta + tag.deltaEtaSC)
        self.out.fillBranch("tag_Ele_phi"    , tag.phi)
        self.out.fillBranch("tag_Ele_q"      , tag.charge)
        self.out.fillBranch("tag_Ele_ID"     , tag.mvaFall17V2Iso_WPL + tag.mvaFall17V2Iso_WP90 + tag.mvaFall17V2Iso_WP80)
        self.out.fillBranch("probe_Ele_pt"   , probe.pt)
        self.out.fillBranch("probe_Ele_eta"  , probe.eta)
        self.out.fillBranch("probe_sc_eta"   , probe.eta + probe.deltaEtaSC)
        self.out.fillBranch("probe_Ele_phi"  , probe.phi)
        self.out.fillBranch("probe_Ele_q"    , probe.charge)
        self.out.fillBranch("probe_triggered", passed)
        self.out.fillBranch("probe_Ele_ID"   , probe.mvaFall17V2Iso_WPL + probe.mvaFall17V2Iso_WP90 + probe.mvaFall17V2Iso_WP80)

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
        HLT       = Object(event, "HLT")
        electrons = Collection(event, "Electron")
        PuppiMET  = Object(event, "PuppiMET")
        trigObjs  = Collection(event, "TrigObj")

        # Need at least 2 electrons for tag and probe
        if(len(electrons) < 2):
            return False

        ############################
        #    Trigger parameters    #
        ############################
        doTriggerMatching = True #whether or not to require the matched trigger
        
        minelept    = 33. # electron trigger
        if self.runningEra == 0 :
            minelept = 28. #lower pT electron trigger in 2016

        ## Non-trigger lepton parameters ##
        mineleptlow = 25 #set so both leptons can pass the trigger requirement

        
        ############################
        #       Object IDs         #
        ############################
        

        ## selection parameters ##
        maxMET      = -1. # < 0 to apply no cut
        minLepM     = 60. # generator only went down to 50 GeV/c^2
        maxLepM     = 130.        

        ############################
        #     Veto object IDs      #
        ############################
        
        minelept_count = mineleptlow # 5 GeV/c threshold in nanoAOD, but set it to be the trigger threshold used in the analysis
        eleId_count = 1 #0 = none 1 = WPL, 2 = WP80, 3 = WP90        
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
        electronTriggered = False        
        if self.runningEra == 0 :
            electronTriggered = HLT.Ele27_WPTight_Gsf
        elif self.runningEra == 1 :
            electronTriggered = HLT.Ele32_WPTight_Gsf_L1DoubleEG
        elif self.runningEra == 2 :
            electronTriggered = HLT.Ele32_WPTight_Gsf
        if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
            print "Event", self.seen, ": electronTriggered =",electronTriggered
        #require a trigger
        if not electronTriggered :
            return False

        
        ############################
        #     Count electrons      #
        ############################

        nElectrons = 0
        elec_dict = dict() # save a dictionary to find the objects again
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
                and (ele_sc_eta < 1.4442 or ele_sc_eta > 1.566)
                and self.elec_id(electrons[index], eleId_count)) :
                elec_dict[nElectrons] = index
                nElectrons = nElectrons + 1

        if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
            print "Event",self.seen,"nelectron (N before IDs) =",nElectrons,"(", len(electrons),")  met =",PuppiMET.pt

        if nElectrons != 2: #Require dielectron events only
            return False

        
        ####################################
        #  Check leptons against triggers  #
        ####################################

        leptonOneTriggered = False
        leptonTwoTriggered = False
        if doTriggerMatching:
            electronTriggered = False
            if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
                print "Event", self.seen, ": printing electron trigger info..."
            for i_elec in range(nElectrons):
                hasFired = self.check_trig(trigObjs, electrons[elec_dict[i_elec]])
                if hasFired > 0:
                    electronTriggered = True
                    if i_elec == 0 :
                        leptonOneTriggered = True
                    else :
                        leptonTwoTriggered = True
                if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
                    print " Electron", i_elec, "has hasFired =", hasFired

        if self.verbose > 0 and not electronTriggered:
            print "Event", self.seen, "has electron triggered value changed after mapping! There are", nElectrons, "electrons..."
        
        if not electronTriggered :
            self.failTrigMap = self.failTrigMap + 1
            return False

        ############################
        #   Check each selection   #
        ############################


        ## store selected lepton info ##
        leptonOneIndex  = -1
        leptonOneFlavor = 0
        leptonTwoIndex  = -1
        leptonTwoFlavor = 0
        
        ############################
        #           E+E            #
        ############################

        ee    = True
        leptonOneIndex = elec_dict[0]
        leptonTwoIndex = elec_dict[1]
        if leptonOneIndex == leptonTwoIndex:
            print "!!! Warning!",self.seen, "returned the same index values for the EE selection!"
            return False
        lep1 = electrons[leptonOneIndex]
        lep2 = electrons[leptonTwoIndex]
        leptonOneFlavor = lep1.charge*-11
        leptonTwoFlavor = lep2.charge*-11
        ee = ee and lep1.pt > mineleptlow and lep2.pt > mineleptlow
        ee = ee and (lep1.pt > minelept or lep2.pt > minelept)
        #at least one must pass the WP80 ID and fire the trigger (tag requirement)
        ee = ee and ((self.elec_id(lep1, 2) and leptonOneTriggered) or (self.elec_id(lep2, 2) and leptonTwoTriggered))

        # must pass a selection
        if not ee:
            return False

        ############################
        #  Additional filtering    #
        ############################

        ## Filter by mass range ##
        lep_mass = (lep1.p4() + lep2.p4()).M()
        if lep_mass < minLepM or lep_mass > maxLepM:
            return False

        ## Filter by charge ##
        if leptonOneFlavor*leptonTwoFlavor > 0:
            return False

        if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
            print "passing event", self.seen

        ############################
        #      Accept event        #
        ############################
        #18530 with extra fill call, matching printed expectation, without
        if leptonOneTriggered :
            self.out.fillBranch("nElectrons", nElectrons)
            self.out.fillBranch("event_met_pfmet", PuppiMET.pt)
            self.fill_branches(lep1, lep2, leptonTwoTriggered)
        if leptonTwoTriggered :
            # If both triggered, need to fill the tree before filling the info for the other configuration
            if leptonOneTriggered :
                self.out.fill()
            self.out.fillBranch("nElectrons", nElectrons)
            self.out.fillBranch("event_met_pfmet", PuppiMET.pt)
            self.fill_branches(lep2, lep1, leptonOneTriggered)


        # increment selection counts
        self.passed = self.passed + 1
        if leptonOneTriggered and leptonTwoTriggered :
            self.probe_passed = self.probe_passed + 2 #each passes the others probe check
        else :
            self.probe_failed = self.probe_failed + 1 #only 1 tag, so 1 probe failure

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
leptonConstr = lambda runningEra, maxEvents, startEvent, isData : exampleProducer(runningEra, maxEvents, startEvent, isData)
