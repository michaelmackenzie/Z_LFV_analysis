//Split the analysis tree into selection trees by the selection ID

int split_output_tree(const char* filename_in, const char* filename_out) {
  TFile* fileIn = TFile::Open(filename_in, "READ");
  if(!fileIn) return 1;

  //Retrieve the input data
  TTree* Events = (TTree*) fileIn->Get("Events");
  TTree* Runs   = (TTree*) fileIn->Get("Runs");
  TH1*   events = (TH1*  ) fileIn->Get("events");

  if(!Events || !Runs || !events) {
    cout << "Input data not found\n";
    return 2;
  }

  TFile* fileOut = new TFile(filename_out, "RECREATE");

  //Clone the Runs tree
  auto RunsOut = Runs->CloneTree();
  RunsOut->Write();

  //Clone the normalization histogram
  events->SetName("events_in");
  TH1* eventsOut = (TH1*) events->Clone("events");
  eventsOut->Write();

  fileOut->Close();

  vector<TString> selections = {"MuTau", "ETau", "EMu", "MuMu", "EE"};
  for(TString selec : selections) {
    fileOut = new TFile(filename_out, "UPDATE");
    TString name = selec;
    selec.ToLower();
    cout << " Copying " << selec.Data() << " tree...\n";
    TTree* EventsOut = Events->CopyTree(Form("SelectionFilter_%s", name.Data()));
    if(!EventsOut) {
      cout << "Events tree failed to split the tree!\n";
      fileOut->Close();
      fileIn->Close();
      return 10;
    }
    EventsOut->SetName(selec.Data());
    EventsOut->Write();
    fileOut->Close();
  }
  fileIn->Close();

  return 0;
}
