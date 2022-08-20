from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import os
import numpy as np
import itertools

ROOT.PyConfig.IgnoreCommandLineOptions = True

_rootLeafType2rootBranchType = {
    'UChar_t': 'b', 'Char_t': 'B', 'UInt_t': 'i', 'Int_t': 'I', 'Float_t': 'F',
    'Double_t': 'D', 'ULong64_t': 'l', 'Long64_t': 'L', 'Bool_t': 'O'}


class GenZllAnalyzer(Module):
    def __init__(self, variables, motherName="GenZll", skip=False, verbose=0):
        self.motherName=motherName #base name of the variable branches
        self.variables=variables
        self.skip=skip
        self.verbose=verbose
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("%s_Idx"        % (self.motherName),'I')
        self.out.branch("%s_LepOne_Idx" % (self.motherName),'I')
        self.out.branch("%s_LepTwo_Idx" % (self.motherName),'I')
        self.out.branch("%s_LepOne_DecayIdx" % (self.motherName),'I')
        self.out.branch("%s_LepTwo_DecayIdx" % (self.motherName),'I')
        for var in self.variables:
            self.out.branch("%s_%s"%(self.motherName,var),'F')
            #Assumes Z->ll(') decays, so two daughters
            self.out.branch("%s_LepOne_%s"%(self.motherName,var),'F') 
            self.out.branch("%s_LepTwo_%s"%(self.motherName,var),'F') 
        pass
 

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def filterBranchNames(self, branches, collection):
        out = []
        for br in branches:
            name = br.GetName()
            if not name.startswith(collection + '_'):
                continue
            out.append(name.replace(collection + '_', ''))
            self.branchType[out[-1]] = br.FindLeaf(br.GetName()).GetTypeName()
        return out

    def fillWithDefaults(self):
        self.out.fillBranch("%s_Idx"        % (self.motherName), -99)
        self.out.fillBranch("%s_LepOne_Idx" % (self.motherName), -99)
        self.out.fillBranch("%s_LepTwo_Idx" % (self.motherName), -99)
        self.out.fillBranch("%s_LepOne_DecayIdx" % (self.motherName), -99)
        self.out.fillBranch("%s_LepTwo_DecayIdx" % (self.motherName), -99)

        for vr in self.variables:
            self.out.fillBranch("%s_%s"        % (self.motherName, vr), -99)
            self.out.fillBranch("%s_LepOne_%s" % (self.motherName, vr), -99)
            self.out.fillBranch("%s_LepTwo_%s" % (self.motherName, vr), -99)
        pass

    def print_gen(self, gens):
        print "Printing Gen collection:\n index:   pdg        pt      eta    mother-idx status isLastCopy"
        for igen,gen in enumerate(gens):
            print "%6i: %5i %10.1f %10.2f %7i %7i %7i"%(igen, gen.pdgId, gen.pt, gen.eta, gen.genPartIdxMother,gen.status,(gen.statusFlags & (1<<13) != 0))

    def get_decay_list(self, idx, gens):
        daughters = []
        for igen,gen in enumerate(gens):
            if gen.genPartIdxMother == idx:
                daughters.append(igen)
        return daughters

    def get_tau_decay(self, idx, gens):
        self_decay = True
        pdgId = gens[idx].pdgId
        while self_decay:
            self_decay = False
            daughters = self.get_decay_list(idx, gens)
            #descend down the decay chain until no longer radiative decays, etc.
            for ipart in daughters:
                if gens[ipart].pdgId == pdgId:
                    self_decay = True
                    idx = ipart
        #identify if it's leptonic or hadronic decay
        for ipart in daughters:
            pdgId = gens[ipart].pdgId
            if abs(pdgId) == 11 or abs(pdgId) == 13:
                return ipart
        return -1
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if not hasattr(event, "nGenPart"): #Data does not have gen-particle information
            self.fillWithDefaults()
            return True

        gens = Collection(event, "GenPart")
        mother_id = -1
        lepone_id = -1
        leptwo_id = -1
        for igen,gen in enumerate(gens):
            absID = abs(gen.pdgId)
            if absID == 23: #Z boson
                if(gen.statusFlags & (1<<13)): #check if isLastCopy()
                    mother_id = igen
            elif absID == 11 or absID == 13 or absID == 15: #charged lepton
                lep_mother = gen.genPartIdxMother
                if lep_mother >= 0 and abs(gens[lep_mother].pdgId) == 23: #parent is a Z boson or no parent
                    if lepone_id < 0:
                        lepone_id = igen
                    elif leptwo_id < 0:
                        leptwo_id = igen
                    else:
                        print "GenZllAnalyzer: More than two Z->ll charged leptons found (indices %i,%i,%i)! Skipping the event"%(lepone_id,leptwo_id,igen)
                        if self.verbose > 1:
                            self.print_gen(gens)
                        if self.skip:
                            return False
                        self.fillWithDefaults()
                        return True

        #if no mother boson found, try to identify primary leptons
        if lepone_id < 0 and leptwo_id < 0:
            if self.verbose > 2:
                print "GenZllAnalyzer: No Z boson found, looking for primary leptons"
                self.print_gen(gens)
            for igen,gen in enumerate(gens):
                absID = abs(gen.pdgId)
                if absID == 11 or absID == 13 or absID == 15: #charged lepton
                    lep_mother = gen.genPartIdxMother
                    if lep_mother == 0: #no parent
                        if lepone_id < 0:
                            lepone_id = igen
                        elif leptwo_id < 0:
                            leptwo_id = igen
                        else:
                            print "GenZllAnalyzer: More than two Z->ll charged leptons found (indices %i,%i,%i)! Skipping the event"%(lepone_id,leptwo_id,igen)
                            if self.verbose > 1:
                                self.print_gen(gens)
                            if self.skip:
                                return False
                            self.fillWithDefaults()
                            return True

        # end particle loops
        if lepone_id < 0 or leptwo_id < 0:
            if self.verbose > -1:
                print "GenZllAnalyzer: Two Z->ll charged leptons not found! Skipping the event"
            if self.verbose > 1:
                self.print_gen(gens)
            if self.skip:
                return False
            self.fillWithDefaults()
            return True

        if mother_id < 0 and self.verbose > 0:
            print "GenZllAnalyzer: Mother Z boson not found! Filling mother branch values with defaults..."

        self.out.fillBranch("%s_Idx"        % (self.motherName), mother_id)
        self.out.fillBranch("%s_LepOne_Idx" % (self.motherName), lepone_id)
        self.out.fillBranch("%s_LepTwo_Idx" % (self.motherName), leptwo_id)

        # fill extra tau decay information if applicable
        if abs(gens[lepone_id].pdgId) == 15:
            lepone_decay = self.get_tau_decay(lepone_id, gens)
        else:
            lepone_decay = -99
        self.out.fillBranch("%s_LepOne_DecayIdx" % (self.motherName), lepone_decay)
        if abs(gens[leptwo_id].pdgId) == 15:
            leptwo_decay = self.get_tau_decay(leptwo_id, gens)
        else:
            leptwo_decay = -99
        self.out.fillBranch("%s_LepTwo_DecayIdx" % (self.motherName), leptwo_decay)

        # if abs(gens[lepone_id].pdgId) == 15:
        #     print " LepOne decay = %i LepTwo decay = %i" % (lepone_decay, leptwo_decay)
        #     self.print_gen(gens)

        #fill daughter variables
        for vr in self.variables:
            if mother_id < 0:
                self.out.fillBranch("%s_%s" % (self.motherName, vr), -99)
            else:
                out = getattr(gens[mother_id],vr)
                self.out.fillBranch("%s_%s" % (self.motherName, vr), out)
            out = getattr(gens[lepone_id],vr)
            self.out.fillBranch("%s_LepOne_%s" % (self.motherName, vr), out)
            out = getattr(gens[leptwo_id],vr)
            self.out.fillBranch("%s_LepTwo_%s" % (self.motherName, vr), out)
          
        return True
