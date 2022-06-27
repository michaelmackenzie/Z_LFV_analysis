//Check the N(events) and N(negative events) in a NANOAOD file

int add_norm(const char* file_in, const char* file_out) {
  TFile* f_in  = TFile::Open(file_in , "READ");
  TFile* f_out = TFile::Open(file_out, "UPDATE");
  if(!f_in || !f_out) return 1;

  TTree* Events = (TTree*) f_in ->Get("Events");
  TTree* Runs   = (TTree*) f_out->Get("Runs"  );
  if(!Events || !Runs) {
    std::cout << __func__ << ": ERROR! Events/Runs tree not found\n";
    return 2;
  }

  Long64_t nentries = Events->GetEntriesFast();
  Long64_t nnegative = 0; //default to 0 negative weight events for data
  if(Events->GetBranch("genWeight")) { //not data
    Events->Draw(">>elist","genWeight < 0");
    TEventList *elist = (TEventList*) gDirectory->Get("elist");
    nnegative = elist->GetN();  // number of events passing the cuts
  }

  auto br_nevt = Runs->Branch("NEvents"  , &nentries );
  auto br_nneg = Runs->Branch("NNegative", &nnegative);
  br_nevt->Fill();
  br_nneg->Fill();

  Runs->Write();
  f_out->Close();
  f_in->Close();

  return 0;
}
