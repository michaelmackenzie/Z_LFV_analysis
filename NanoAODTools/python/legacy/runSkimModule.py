import ROOT
import math
import time

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class exampleProducer(Module):
    def __init__(self,runningEra, maxEvents, startEvent, isData, saveZ):
        self.runningEra = runningEra
        self.maxEvents = maxEvents #for quick local testing
        self.startEvent = startEvent
        self.isData = isData
        self.isDY = saveZ
        self.seen = 0
        self.mutau = 0
        self.etau = 0
        self.emu = 0
        self.mumu = 0
        self.ee = 0
        self.failTrigMap = 0
        self.negativeEvents = 0
        self.nTauRejected = 0
        if self.maxEvents == 1:
            self.verbose = 20
        elif self.maxEvents > 0 and self.maxEvents < 10:
            self.verbose = 10
        elif self.maxEvents > 0 and self.maxEvents < 1000:
            self.verbose = 2
        else:
            self.verbose = 1
        self.cut_flow_tt = ROOT.TH1D("cut_flow_tt", "cut_flow_tt", 100, 0, 100)
        self.cut_flow_ll = ROOT.TH1D("cut_flow_ll", "cut_flow_ll", 100, 0, 100)
        self.cut_flow_embed = ROOT.TH1D("cut_flow_embed", "cut_flow_embed", 100, 0, 100)
        pass

    #--------------------------------------------------------------------------------------------------------------
    def beginJob(self):
        self.beginTime = time.clock()
        pass

    #--------------------------------------------------------------------------------------------------------------
    def endJob(self):
        print "Saw", self.emu, "e+mu,", self.etau,"e+tau,", self.mutau, "mu+tau,", self.mumu, "mu+mu, and", self.ee, "ee","from",(self.seen-self.startEvent+1),"events processed"
        print "Rejected", self.nTauRejected, "from etau/mutau due to overlap"
        print "Found", self.failTrigMap, "events that failed trigger matching requirements"
        print "Processing took", time.clock()-self.beginTime, "seconds"
        pass

    #--------------------------------------------------------------------------------------------------------------
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        # outputFile.SetCompressionLevel(0) #don't compress to speed up processing and reduce memory (?)
        self.out = wrappedOutputTree
        self.out.branch("M_ll" ,  "F"); # di-lepton mass
        self.out.branch("leptonOneFlavor",  "I"); # lepton one flavor
        self.out.branch("leptonOneIndex" ,  "I"); # lepton one index
        self.out.branch("leptonTwoFlavor",  "I"); # lepton two flavor
        self.out.branch("leptonTwoIndex" ,  "I"); # lepton two index
        self.out.branch("leptonOneGenPt" ,  "F"); # Gen-level matched particle pT
        self.out.branch("leptonTwoGenPt" ,  "F"); # Gen-level matched particle pT
        self.out.branch("zPt"            ,  "F"); # Gen-level Z pT
        self.out.branch("zMass"          ,  "F"); # Gen-level Z mass
        self.out.branch("zLepOne"        ,  "I"); # Gen-level Z lepton daughter 1
        self.out.branch("zLepTwo"        ,  "I"); # Gen-level Z lepton daughter 2
        self.out.branch("zLepOnePt"      ,  "F"); # Gen-level Z lepton daughter 1
        self.out.branch("zLepTwoPt"      ,  "F"); # Gen-level Z lepton daughter 2
        self.out.branch("zLepOneEta"     ,  "F"); # Gen-level Z lepton daughter 1
        self.out.branch("zLepTwoEta"     ,  "F"); # Gen-level Z lepton daughter 2
        self.out.branch("muonLowTrigger" ,  "O"); # fired muon low trigger
        self.out.branch("muonHighTrigger",  "O"); # fired muon high trigger
        self.out.branch("electronTrigger",  "O"); # fired electron trigger
        self.out.branch("nElectrons"     ,  "I"); # store lepton counts
        self.out.branch("nMuons"         ,  "I");
        self.out.branch("nTaus"          ,  "I");
        self.out.branch("nGenTaus"       ,  "I"); #number of generated taus from relevant particles
        # self.out.branch("dataPeriod"     ,  "I"); #store which run if in data
        # self.out.branch("mcEra"          ,  "I"); #store which period of data this is split into (e.g. 2016 B-F vs GH)
        self.name = inputFile.GetName()
        # data samples from Z to ll (include LFV just for Z info)
        # self.isDY = self.isDY or ("DYJetsToLL" in name) or ("ZMuTau" in name) or ("ZETau" in name) or ("ZEMu" in name)
        print "Using isDY =", self.isDY, "for file", self.name
        
    #--------------------------------------------------------------------------------------------------------------
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        outputFile.cd()
        h = ROOT.TH1D("events", "events", 10, 1, 11)
        h.Fill(1.5, self.seen)
        h.Fill(2.5, self.emu)
        h.Fill(3.5, self.etau)
        h.Fill(4.5, self.mutau)
        h.Fill(5.5, self.mumu)
        h.Fill(6.5, self.ee)
        h.Fill(10.5, self.negativeEvents)
        h.Write()
        self.cut_flow_tt.Write()
        self.cut_flow_ll.Write()
        self.cut_flow_embed.Write()
        pass

    #--------------------------------------------------------------------------------------------------------------
    # count the number of gen-level taus produced from Z, W, and tops
    def countGenTaus(self, genParts):
        ngenpart = len(genParts)
        nGenTaus = 0
        motherParticles = [6, 22, 23, 24] #parents of taus considered
        for index in range(ngenpart):
            if abs(genParts[index].pdgId) == 15 : #tau
                if genParts[index].genPartIdxMother >= 0 and abs(genParts[genParts[index].genPartIdxMother].pdgId) != 15 :
                    motherID = abs(genParts[genParts[index].genPartIdxMother].pdgId)
                    if motherID in motherParticles : #parent is a relevant particle
                        nGenTaus = nGenTaus + 1
                if genParts[index].genPartIdxMother < 0 : #no listed parent, include in the count for now
                    nGenTaus = nGenTaus + 1
        return nGenTaus
    
    #--------------------------------------------------------------------------------------------------------------
    # get generator info for Z boson
    def genZInfo(self, event):
        genParts = Collection(event, "GenPart")
        ngenpart = len(genParts)
        zpt = -1.
        zmass = -1.
        leponeid = 0
        leptwoid = 0
        leponept = 0
        leptwopt = 0
        leponeeta = 0
        leptwoeta = 0
        for index in range(ngenpart):
            if abs(genParts[index].pdgId) == 23 or abs(genParts[index].pdgId) == 25: #Z/H boson
                if (genParts[index].statusFlags & (1<<13)): #check if isLastCopy()
                    zpt = genParts[index].pt
                    zmass = genParts[index].mass
                else : #save values in case no Z/H passes the last copy check, if not filled already
                    if zpt < 0. :
                        zpt = genParts[index].pt
                    if zmass < 0. :
                        zmass = genParts[index].mass
            elif ((abs(genParts[index].pdgId) == 11 or abs(genParts[index].pdgId) == 13 or abs(genParts[index].pdgId) == 15) #charged lepton
                  and genParts[index].genPartIdxMother >= 0 and (genParts[genParts[index].genPartIdxMother].pdgId == 23 #parent is z-boson
                                                                 or genParts[genParts[index].genPartIdxMother].pdgId == 25)): #parent is h-boson
                if leponeid == 0:
                    leponeid  = genParts[index].pdgId
                    leponept  = genParts[index].pt
                    leponeeta = genParts[index].eta
                else:
                    leptwoid = genParts[index].pdgId
                    leptwopt  = genParts[index].pt
                    leptwoeta = genParts[index].eta
        if zpt < 0. or zmass < 0. or leponeid == 0 or leptwoid == 0:
            if self.verbose > 1 :
                print "Warning! Not all Z information was found in event", self.seen
                print "Found Z pT =", zpt, "and Mass =", zmass, ". Lep One Pdg ID =", leponeid, "and Lep Two Pdg ID =", leptwoid
                print "Attempting to replace the Z by looking for two leptons with parent = 0..."
                print "Printing the gen particle information:"
            leponeindex = -1
            leptwoindex = -1
            for index in range(ngenpart):
                if self.verbose > 9:
                    print "Index", index, ": Pdg =", genParts[index].pdgId, " parent =", genParts[index].genPartIdxMother, \
                        "mass =", genParts[index].mass, "pt =", genParts[index].pt
                if((abs(genParts[index].pdgId) == 11 or abs(genParts[index].pdgId) == 13 or abs(genParts[index].pdgId) == 15) #charged lepton
                   and genParts[index].genPartIdxMother == 0) : #Mother is original quark
                    if leponeindex < 0:
                        leponeindex = index
                    elif leptwoindex < 0:
                        leptwoindex = index
            if leponeindex < 0 or leptwoindex < 0:
                print "Failed to find leptons coming from particle 0!"
            else :
                if self.verbose > 1 :
                    print "Z info replacement was successful!"
                lv1 = ROOT.TLorentzVector()
                lv1.SetPtEtaPhiM(genParts[leponeindex].pt, genParts[leponeindex].eta, genParts[leponeindex].phi, genParts[leponeindex].mass)
                lv2 = ROOT.TLorentzVector()
                lv2.SetPtEtaPhiM(genParts[leptwoindex].pt, genParts[leptwoindex].eta, genParts[leptwoindex].phi, genParts[leptwoindex].mass)
                zpt = (lv1+lv2).Pt()
                zmass = (lv1+lv2).M()
                leponeid  = genParts[leponeindex].pdgId
                leptwoid  = genParts[leptwoindex].pdgId
                leponept  = genParts[leponeindex].pt
                leponeeta = genParts[leponeindex].eta
                leptwopt  = genParts[leptwoindex].pt
                leptwoeta = genParts[leptwoindex].eta
        self.out.fillBranch("zPt", zpt)
        self.out.fillBranch("zMass", zmass)
        self.out.fillBranch("zLepOne", leponeid)
        self.out.fillBranch("zLepTwo", leptwoid)
        self.out.fillBranch("zLepOnePt", leponept)
        self.out.fillBranch("zLepTwoPt", leptwopt)
        self.out.fillBranch("zLepOneEta", leponeeta)
        self.out.fillBranch("zLepTwoEta", leptwoeta)

    #--------------------------------------------------------------------------------------------------------------
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
                        # if not isMuon:
                        result = 1
                        return result
                        # passedBit1 = passedBit1 or passBit1
                        # passedBit2 = passedBit2 or passBit2
        return 0 #passedBit1 + 2*passedBit2

    #--------------------------------------------------------------------------------------------------------------
    # electron ID check
    def elec_id(self, electron, WP):
        if WP == 0: 
            return True
        elif WP == 1:
            return electron.mvaFall17V2Iso_WPL
        elif WP == 2:
            return electron.mvaFall17V2Iso_WP80
        elif WP == 3: # Historical reasons to be out of order, only WPL and WP80 originally considered
            return electron.mvaFall17V2Iso_WP90
        return False

    #--------------------------------------------------------------------------------------------------------------
    # muon ID check
    def muon_id(self, muon, ID, IsoID):
        passed = ((ID == 1 and muon.looseId) or
                  (ID == 2 and muon.mediumId) or
                  (ID == 3 and muon.tightId))
        passed = passed and muon.pfRelIso04_all < IsoID
        return passed
    
    #--------------------------------------------------------------------------------------------------------------
    # tau ID check
    def tau_id(self, tau, useDeep, antiEle, antiMu, antiJet) :
        passed = True
        if useDeep:
            passed = passed and tau.idDeepTau2017v2p1VSe >= antiEle
            passed = passed and tau.idDeepTau2017v2p1VSmu >= antiMu
            passed = passed and tau.idDeepTau2017v2p1VSjet >= antiJet
            passed = passed and tau.idDecayModeNewDMs
        else:
            passed = passed and tau.idAntiEle >= antiEle
            passed = passed and tau.idAntiMu >= antiMu
            passed = passed and tau.idMVAnewDM2017v2 >= antiJet
            passed = passed and tau.idDecayMode
        return passed

    #--------------------------------------------------------------------------------------------------------------
    # ee/mumu selection check, as more than two leptons may be identified for the flavor
    # returns the first pair that pass the trigger threshold, lepton IDs, and the mass window
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

    #--------------------------------------------------------------------------------------------------------------
    # Main processing loop
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

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

        ############################
        #  Get cut flow histogram  #
        ############################
        if self.isData :
            nGenTaus = 0
        else :
            nGenTaus = self.countGenTaus(Collection(event, "GenPart"))

        if self.isData or nGenTaus == 2:
            cut_flow = self.cut_flow_tt #tau-tau cut-flow
        else:
            cut_flow = self.cut_flow_ll #cut-flow for the rest

        cut_flow.Fill(0)

        if self.isData == 0:
            embedWeight = math.fabs(event.genWeight)
        else:
            embedWeight = 1.

        cut_flow_embed = self.cut_flow_embed
        cut_flow_embed.Fill(0,embedWeight)
        if nGenTaus == 2:
            cut_flow_embed.Fill(1, embedWeight)

        ############################
        #      Get input data      #
        ############################

        HLT       = Object(event, "HLT")
        electrons = Collection(event, "Electron")
        muons     = Collection(event, "Muon")
        taus      = Collection(event, "Tau")
        jets      = Collection(event, "Jet")
        PuppiMET  = Object(event, "PuppiMET")
        trigObjs  = Collection(event, "TrigObj")

        if(len(electrons) == 1 and len(muons) == 1):
            cut_flow_embed.Fill(2, embedWeight)

        ############################
        #    Trigger parameters    #
        ############################

        doTriggerMatching = False #whether or not to require a matched trigger object to the trigger lepton
        minmupt     = 25. # muon trigger
        minelept    = 33. # electron trigger
        if self.runningEra == 0 :
            minelept = 28. # lower pT electron trigger in 2016
        elif self.runningEra == 1 :
            minmupt = 28. # higher pT muon trigger in 2017

        ## Non-trigger lepton pt thresholds ##
        minmuptlow  = 10.
        mineleptlow = 10.
        mintaupt    = 20.

        
        ############################
        #       Object IDs         #
        ############################
        
        ## jet parameters ##
        jetIdflag   = 1
        jetPUIdflag = 4


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
        maxJetPt    = -1. # < 0 to apply no cut
        minLepM     = 50. # generator only went down to 50 GeV/c^2
        maxLepM     = 170.
        cutBJets    = False

        # switch between tau IDs (deep NN IDs or old MVA IDs)
        useDeepNNTauIDs = True
        
        muonIso_DF  = muonIsoTight
        eleId_DF    = 2
        muonIso_SF  = muonIso_DF #set separately in case of QCD scale, not done in Same Flavor
        eleId_SF    = eleId_DF #set separately in case of QCD scale, not done in Same Flavor        
        tauAntiEle = 1 # (bitmask) MVA: 8 = tight, 16 = very tight deepNN:  1 = VVVLoose 2 = VVLoose 4 = VLoose   8 = Loose
        #                                                                  16 = Medium  32 = Tight  64 = VTight 128 = VVTight
        tauAntiEle_etau = 50 #higher veto requirement for ee -> e fake tau
        tauAntiMu  = 10 # (bitmask) MVA: 1 = loose 2 = tight deepNN: 1 = VLoose 2 = Loose 4 = Medium 8 = Tight
        tauAntiJet = 50 # (bitmask) deepNN: 1 = VVVLoose 2 = VVLoose 4 = VLoose 8 = Loose 16 = Medium 32 = Tight 64 = VTight 128 = VVTight
        tauIso     = 7 
        tauDeltaR  = 0.3

        ############################
        #     Veto object IDs      #
        ############################
        
        ## veto parameters ##
        allowManySameFlavor    = True # allow more than 2 electrons or muons in ee/mumu selection
        vetoSameSignSameFlavor = False # veto events with two light leptons and same charge

        # muons
        minmupt_count = 10. # 3 GeV/c threshold in nanoAOD
        muonIso_count = muonIsoVVLoose
        muonId_count  = 1 # 1 = loose, 2 = medium, 3 = tight
        max_muon_eta  = 2.2
        # electrons
        minelept_count = 10. # 5 GeV/c threshold in nanoAOD
        eleId_count    = 1 #0 = none 1 = WPL, 2 = WP80, 3 = WP90        
        max_ele_eta    = 2.2
        elec_eta_veto_min = 1.442 # veto region for electrons
        elec_eta_veto_max = 1.566
        # taus
        mintaupt_count   = 20.
        tauAntiEle_count = 10 #Loose
        tauAntiMu_count  = 10 #Tight
        tauAntiJet_count =  5 #VLoose
        tauIso_count     = 0
        tauIdDecay_count = True
        tauDeltaR_count  = 0.3 #distance from selected electrons/muons
        max_tau_eta      = 2.2

        ############################
        #      QCD Scale calc      #
        ############################
        doQCDLoose = True
        if doQCDLoose: # if include loose QCD selection events, lower the relevant ID for the final selection
            muonIso_DF = muonIso_count #loose muon selection
            eleId_DF = eleId_count #loose electron selection
            tauAntiJet = tauAntiJet_count #loose tau selection

        ############################
        #     Begin selections     #
        ############################
        
        ### initial filtering ###
        if maxMET > 0 and PuppiMET.pt > maxMET : #cut high MET events
            return False
        cut_flow.Fill(1)
        cut_flow_embed.Fill(3, embedWeight)

        ############################
        #    Trigger selection     #
        ############################
        ### check which triggers are fired ###
        muonTriggered     = False
        muonLowTriggered  = False
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

        cut_flow.Fill(2)
        cut_flow_embed.Fill(4, embedWeight)
        
        ############################
        #      Count leptons       #
        ############################

        nElectrons = 0
        nMuons = 0
        nTaus = 0
        elec_dict = dict() # use a dictionary to store identified leptons
        muon_dict = dict()
        tau_dict  = dict()

        ############################
        #     Count electrons      #
        ############################
        if (self.verbose > 9 and self.seen % 10 == 0) or self.verbose > 10:
            print "Event", self.seen, ": printing electron info..."
        for index in range(len(electrons)) :
            if(self.verbose > 9 and self.seen % 10 == 0) or self.verbose > 10:
                print " Electron", index, "pt =", electrons[index].pt, "eta =", electrons[index].eta, "WPL =", electrons[index].mvaFall17V2Iso_WPL, \
                    "WP80 =", electrons[index].mvaFall17V2Iso_WP80 
            ele_sc_eta = math.fabs(electrons[index].eta + electrons[index].deltaEtaSC)
            ele_eta = math.fabs(electrons[index].eta + electrons[index].deltaEtaSC)
            if (electrons[index].pt > minelept_count and  ele_eta < max_ele_eta
                and (ele_sc_eta < elec_eta_veto_min or ele_sc_eta > elec_eta_veto_max)
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
        ############################
        #       Count taus         #
        ############################
        if ((self.verbose > 9 and self.seen % 10 == 0) or self.verbose > 10):
            print "Event", self.seen, ": printing tau info..."
        for index in range(len(taus)) :
            if(self.verbose > 9 and self.seen % 10 == 0) or self.verbose > 10:
                print " Tau", index, "pt =", taus[index].pt, "AntiMu =", taus[index].idDeepTau2017v2p1VSmu, "AntiEle =", \
                    taus[index].idDeepTau2017v2p1VSe, "AntiJet =", taus[index].idDeepTau2017v2p1VSjet
            if (taus[index].pt > mintaupt_count and abs(taus[index].eta) < max_tau_eta
                and self.tau_id(taus[index], useDeepNNTauIDs, tauAntiEle_count, tauAntiMu_count, tauAntiJet_count)) :
                deltaRCheck = True
                if tauDeltaR_count > 0 : #check for overlap with accepted lepton
                    for i_elec in range(nElectrons):
                        deltaRCheck = deltaRCheck and taus[index].p4().DeltaR(electrons[elec_dict[i_elec]].p4()) > tauDeltaR_count
                        if not deltaRCheck:
                            break
                    for i_muon in range(nMuons):
                        deltaRCheck = deltaRCheck and taus[index].p4().DeltaR(muons[muon_dict[i_muon]].p4()) > tauDeltaR_count
                        if not deltaRCheck:
                            break
                if deltaRCheck:
                    tau_dict[nTaus] = index
                    nTaus = nTaus + 1

        if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
            print "Event",self.seen,"lepton counts: ntau (N before IDs) =",nTaus,"(", len(taus),") nelectron (N before IDs) =",nElectrons,"(", len(electrons),") nmuon (N before IDs) =",\
                nMuons,"(",len(muons),") met =",PuppiMET.pt

        if nElectrons + nMuons + nTaus < 2:
            return False
        cut_flow.Fill(3)
        cut_flow_embed.Fill(5, embedWeight)
        if nElectrons == 1 and nMuons == 1:
            cut_flow_embed.Fill(6, embedWeight)
        if nElectrons == 1 and nTaus == 1:
            cut_flow_embed.Fill(7, embedWeight)
        if nMuons == 1 and nTaus == 1:
            cut_flow_embed.Fill(8, embedWeight)

        ### Add lepton trigger requiring that lepton ###
        electronTriggered = electronTriggered and nElectrons > 0
        muonTriggered = muonTriggered and nMuons > 0
        if not muonTriggered and not electronTriggered:
            return False
        cut_flow.Fill(4)
        cut_flow_embed.Fill(9, embedWeight)

        ####################################
        #  Check leptons against triggers  #
        ####################################
        if doTriggerMatching:
            if muonTriggered:
                muonTrig = False
                # muonLoTrig = False
                # muonHiTrig = False
                #check if a selected muon matches with the muon triggers of interest
                if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
                    print "Event", self.seen, ": printing muon trigger info..."
                for i_muon in range(nMuons):
                    hasFired = self.check_trig(trigObjs, muons[muon_dict[i_muon]], True)
                    if hasFired > 0: # 1 = low, 2 = high, 3 = both
                        muonTrig  = True
                        # muonLoTrig = muonLoTrig or hasFired == 1 or hasFired == 3
                        # muonHiTrig = muonHiTrig or hasFired > 1
                    if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
                        print " Muon",i_muon,"has hasFired =",hasFired
                if self.verbose > 0 and ((muonTriggered and not muonTrig) ): #or (muonLowTriggered and not muonLoTrig) or (muonHighTriggered and not muonHiTrig)) :
                    print "Event", self.seen, "has muon triggered values changed after mapping! There are", nMuons, "muons..."
                    print " Muon triggers before: trig =", muonTriggered, "low =", muonLowTriggered, "high =", muonHighTriggered
                    print " Muon triggers mapped: trig =", muonTrig #, "low =", muonLoTrig, "high =", muonHiTrig
                    print " Electron triggered =", electronTriggered
                muonTriggered     = muonTrig
                # muonLowTriggered  = muonLowTriggered  and muonLoTrig
                # muonHighTriggered = muonHighTriggered and muonHiTrig
            if electronTriggered:
                electronTriggered = False
                if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
                    print "Event", self.seen, ": printing electron trigger info..."
                for i_elec in range(nElectrons):
                    hasFired = self.check_trig(trigObjs, electrons[elec_dict[i_elec]], False)
                    if hasFired > 0:
                        electronTriggered = True
                        break
                    if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
                        print " Electron", i_elec, "has hasFired =", hasFired
                if self.verbose > 0 and not electronTriggered:
                    print "Event", self.seen, "has electron triggered value changed after mapping! There are", nElectrons, "electrons..."
        
        if not electronTriggered and not muonTriggered :
            self.failTrigMap = self.failTrigMap + 1
            return False
        cut_flow.Fill(5)        
        cut_flow_embed.Fill(10, embedWeight)

        ############################
        #  Filter by lepton count  #
        ############################
        if nElectrons + nMuons < 1: #nothing to trigger on
            return False
        if nElectrons + nMuons == 1 and nTaus != 1: #need at least two light leptons or 1 light + 1 tau
            return False
        if nTaus == 0 and nElectrons > 0 and nMuons > 0 and nElectrons + nMuons > 2: #emu, n*e, or n*mu
            return False
        #no trigger-able leptons
        if nElectrons == 0 and not muonTriggered:
            return False
        if nMuons == 0 and not electronTriggered:
            return False
        if nElectrons == 0 and nMuons > 2 and not allowManySameFlavor:
            return False
        if nMuons == 0 and nElectrons > 2 and not allowManySameFlavor:
            return False
        cut_flow.Fill(6)
        cut_flow_embed.Fill(11, embedWeight)

        ############################
        #   Check each selection   #
        ############################
        ## check if the event passes each selection ##
        mutau = False
        etau  = False
        emu   = False
        ee    = False
        mumu  = False

        ## store selected lepton info ##
        leptonOneIndex  = -1
        leptonOneFlavor = 0
        leptonTwoIndex  = -1
        leptonTwoFlavor = 0
        
        ############################
        #          Mu+Tau          #
        ############################
        # mutau
        if nMuons == 1 and nTaus == 1:
            leptonOneIndex = muon_dict[0]
            leptonTwoIndex = tau_dict[0]
            lep1 = muons[muon_dict[0]]
            lep2 = taus[tau_dict[0]]
            leptonOneFlavor = lep1.charge*-13
            leptonTwoFlavor = lep2.charge*-15
            mutau = lep1.tightId and lep1.pfRelIso04_all < muonIso_DF and lep1.pt > minmupt and lep2.pt > mintaupt
            if useDeepNNTauIDs:
                mutau = mutau and lep2.idDeepTau2017v2p1VSe >= tauAntiEle
                mutau = mutau and lep2.idDeepTau2017v2p1VSmu >= tauAntiMu
                mutau = mutau and lep2.idDeepTau2017v2p1VSjet >= tauAntiJet
                mutau = mutau and lep2.idDecayModeNewDMs
            else:
                mutau = mutau and lep2.idAntiEle >= tauAntiEle
                mutau = mutau and lep2.idAntiMu >= tauAntiMu
                mutau = mutau and lep2.idMVAnewDM2017v2 >= tauIso
                mutau = mutau and lep2.idDecayMode
            mutau = mutau and lep1.p4().DeltaR(lep2.p4()) > tauDeltaR
            mutau = mutau and math.fabs(lep1.eta) < 2.2
            mutau = mutau and math.fabs(lep2.eta) < 2.2
        ############################
        #          E+Tau           #
        ############################
        if nElectrons == 1 and nTaus == 1:
            leptonOneIndex = elec_dict[0]
            leptonTwoIndex = tau_dict[0]
            lep1 = electrons[elec_dict[0]]
            lep2 = taus[tau_dict[0]]
            leptonOneFlavor = lep1.charge*-11
            leptonTwoFlavor = lep2.charge*-15
            etau = self.elec_id(lep1, eleId_DF)
            etau = etau and (math.fabs(lep1.eta + lep1.deltaEtaSC) < elec_eta_veto_min or math.fabs(lep1.eta + lep1.deltaEtaSC) > elec_eta_veto_max) 
            etau = etau and lep1.pt > minelept and lep2.pt > mintaupt
            if useDeepNNTauIDs:
                etau = etau and lep2.idDeepTau2017v2p1VSe >= tauAntiEle_etau
                etau = etau and lep2.idDeepTau2017v2p1VSmu >= tauAntiMu
                etau = etau and lep2.idDeepTau2017v2p1VSjet >= tauAntiJet
                etau = etau and lep2.idDecayModeNewDMs
            else:
                etau = etau and lep2.idAntiEle >= tauAntiEle_etau
                etau = etau and lep2.idAntiMu >= tauAntiMu
                etau = etau and lep2.idMVAnewDM2017v2 >= tauIso
                etau = etau and lep2.idDecayMode
            etau = etau and lep1.p4().DeltaR(lep2.p4()) > tauDeltaR
            etau = etau and math.fabs(lep1.eta) < 2.2
            etau = etau and math.fabs(lep2.eta) < 2.2
        # veto from tau categories if passes both (good looking e, mu, and tau)
        if mutau and etau:
            mutau = False
            etau  = False
            self.nTauRejected = self.nTauRejected + 1
        ############################
        #           E+Mu           #
        ############################
        if nElectrons == 1 and nMuons == 1:
            leptonOneIndex = elec_dict[0]
            leptonTwoIndex = muon_dict[0]
            lep1 = electrons[elec_dict[0]]
            lep2 = muons[muon_dict[0]]
            leptonOneFlavor = lep1.charge*-11
            leptonTwoFlavor = lep2.charge*-13
            emu =  lep2.tightId and lep2.pfRelIso04_all < muonIso_DF and self.elec_id(lep1, eleId_DF)
            emu = emu and (math.fabs(lep1.eta + lep1.deltaEtaSC) < elec_eta_veto_min or math.fabs(lep1.eta + lep1.deltaEtaSC) > elec_eta_veto_max)
            emu = emu and lep1.pt > mineleptlow and lep2.pt > minmuptlow
            emu = emu and math.fabs(lep1.eta) < 2.2
            emu = emu and math.fabs(lep2.eta) < 2.2
        ############################
        #          Mu+Mu           #
        ############################
        elif nMuons >= 2 and nElectrons == 0:
            mumu, leptonOneIndex, leptonTwoIndex = self.sameflavor_check(muon_dict, muons, True, minLepM, maxLepM, minmupt, 3, muonIso_SF)
            if mumu: #accepted
                if leptonOneIndex == leptonTwoIndex:
                    print "!!! Warning!",self.seen, "returned the same index values for the MuMu selection!"
                lep1 = muons[leptonOneIndex]
                lep2 = muons[leptonTwoIndex]
                leptonOneFlavor = lep1.charge*-13
                leptonTwoFlavor = lep2.charge*-13
                mumu = mumu and lep1.pt > minmuptlow and lep2.pt > minmuptlow
        ############################
        #           E+E            #
        ############################
        elif nElectrons >= 2 and nMuons == 0:
            ee, leptonOneIndex, leptonTwoIndex = self.sameflavor_check(elec_dict, electrons, False, minLepM, maxLepM, minelept, 2, 0)
            if ee: #accepted
                if leptonOneIndex == leptonTwoIndex:
                    print "!!! Warning!",self.seen, "returned the same index values for the EE selection!"
                lep1 = electrons[leptonOneIndex]
                lep2 = electrons[leptonTwoIndex]
                leptonOneFlavor = lep1.charge*-11
                leptonTwoFlavor = lep2.charge*-11
                ee = ee and lep1.pt > mineleptlow and lep2.pt > mineleptlow

        # overlap shouldn't happen, but remove if it somehow does
        if emu and (mutau or etau):
            mutau = False
            etau = False
            self.nTauRejected = self.nTauRejected + 1
        
        # must pass a selection
        if not (mutau or etau or emu or mumu or ee):
            return False
        cut_flow.Fill(7)
        cut_flow_embed.Fill(12, embedWeight)

        ############################
        #    Further filtering     #
        ############################
        #ensure lepton info is restored
        if mutau:
            leptonOneIndex = muon_dict[0]
            leptonTwoIndex = tau_dict[0]
            lep1 = muons[muon_dict[0]]
            lep2 = taus[tau_dict[0]]
            leptonOneFlavor = lep1.charge*-13
            leptonTwoFlavor = lep2.charge*-15
        elif etau :
            leptonOneIndex = elec_dict[0]
            leptonTwoIndex = tau_dict[0]
            lep1 = electrons[elec_dict[0]]
            lep2 = taus[tau_dict[0]]
            leptonOneFlavor = lep1.charge*-11
            leptonTwoFlavor = lep2.charge*-15
        elif emu :
            leptonOneIndex = elec_dict[0]
            leptonTwoIndex = muon_dict[0]
            lep1 = electrons[elec_dict[0]]
            lep2 = muons[muon_dict[0]]
            leptonOneFlavor = lep1.charge*-11
            leptonTwoFlavor = lep2.charge*-13

        ############################
        #     Mass filtering       #
        ############################
        ## Filter by mass range ##
        lep_mass = (lep1.p4() + lep2.p4()).M()
        if lep_mass < minLepM or lep_mass > maxLepM:
            return False
        cut_flow.Fill(8)
        cut_flow_embed.Fill(13, embedWeight)

        ############################
        #    Trigger filtering     #
        ############################
        ## check proper trigger is fired ##

        if mumu :
            if not muonTriggered:
                return False
            if not muonLowTriggered : #only passed high pt trigger
                if not (lep1.pt > 50 or lep2.pt > 50.) :
                    return False                
        elif ee :
            if not electronTriggered :
                return False
        elif mutau :
            if not muonTriggered:
                return False
            if not muonLowTriggered : #only passed high pt trigger
                if not (lep1.pt > 50) :
                    return False                
        elif etau :
            if not electronTriggered :
                return False
        elif emu:
            #check triggers with threshold on triggering lepton
            if not ((muonTriggered and lep2.pt > minmupt) or (electronTriggered and lep1.pt > minelept)) :
                return False
            if not muonLowTriggered and not (electronTriggered and lep1.pt > minelept)  : #only passed high pt muon trigger
                if not (lep2.pt > 50) :
                    return False                
        else :
            print "ERROR! No selection found!"
            return False
        cut_flow.Fill(9)
        cut_flow_embed.Fill(14, embedWeight)

        if vetoSameSignSameFlavor and leptonOneFlavor == leptonTwoFlavor:
            return False
        cut_flow.Fill(10)
        cut_flow_embed.Fill(15, embedWeight)
        if emu:
            cut_flow_embed.Fill(16, embedWeight)
        if etau:
            cut_flow_embed.Fill(17, embedWeight)
        if mutau:
            cut_flow_embed.Fill(18, embedWeight)
        if lep1.charge*lep2.charge < 0:
            cut_flow_embed.Fill(19, embedWeight)

        if (self.verbose > 1 and self.seen % 100 == 0) or (self.verbose > 2 and self.seen % 10 == 0) or self.verbose > 9:
            print "passing event", self.seen

        ############################
        #      Accept event        #
        ############################

        # Fill outgoing branches
        self.out.fillBranch("M_ll"           , lep_mass)
        self.out.fillBranch("leptonOneFlavor", leptonOneFlavor)
        self.out.fillBranch("leptonOneIndex" , leptonOneIndex)
        self.out.fillBranch("leptonTwoFlavor", leptonTwoFlavor)
        self.out.fillBranch("leptonTwoIndex" , leptonTwoIndex)
        self.out.fillBranch("nElectrons"     , nElectrons)
        self.out.fillBranch("nMuons"         , nMuons)
        self.out.fillBranch("nTaus"          , nTaus)
        # if DY event, fill extra info
        if(self.isDY):
            self.genZInfo(event)
        # Fill trigger info
        self.out.fillBranch("muonLowTrigger", muonLowTriggered)
        self.out.fillBranch("muonHighTrigger", muonHighTriggered)
        self.out.fillBranch("electronTrigger", electronTriggered)

        # #data period information
        # if self.isData :
        #     if self.name

        # get gen level information
        if self.isData == 0 and hasattr(event, 'nGenPart'):
            genParts = Collection(event, "GenPart")
            if lep1.genPartIdx >= 0:
                self.out.fillBranch("leptonOneGenPt", genParts[lep1.genPartIdx].pt)
            else:
                self.out.fillBranch("leptonOneGenPt", 0.)
            if lep2.genPartIdx >= 0:
                self.out.fillBranch("leptonTwoGenPt", genParts[lep2.genPartIdx].pt)
            else:
                self.out.fillBranch("leptonTwoGenPt", 0.)
            self.out.fillBranch("nGenTaus", nGenTaus)
        else:
            self.out.fillBranch("leptonOneGenPt", 0.)
            self.out.fillBranch("leptonTwoGenPt", 0.)
            self.out.fillBranch("nGenTaus"      , 0 )

        print "Event %8i: accepted" % (self.seen)
        if not electronTriggered and not muonLowTriggered:
            print "--> Muon high triggered event"

        # increment selection counts
        if emu:
            self.emu = self.emu+1
        elif etau:
            self.etau = self.etau+1
        elif mutau:
            self.mutau = self.mutau+1
        elif mumu:
            self.mumu = self.mumu+1
        elif ee:
            self.ee = self.ee+1
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
leptonConstr = lambda runningEra, maxEvents, startEvent, isData, saveZ : exampleProducer(runningEra, maxEvents, startEvent, isData, saveZ)
