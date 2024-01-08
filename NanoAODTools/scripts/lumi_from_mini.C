//Process a MINIAOD file to produce the lumi information
map<unsigned, vector<pair<unsigned, unsigned>>> mask_;
map<unsigned, vector<pair<unsigned, unsigned>>> runs_;
Long64_t entries_ = 0;
Long64_t npass_ = 0;
bool skip_fail_ = true;

//-------------------------------------------------------
// Print the (run, lumi) info out
void print_lumis(const char* out, map<unsigned, vector<pair<unsigned, unsigned>>> runs) {
  if(!out) return;
  ofstream file;
  file.open(out);
  file << "{\n";
  bool first_run = true;
  for(auto run : runs) {
    if(!first_run) file << ",\n";
    first_run = false;
    file << "  \"" << run.first << "\": [";
    bool first_lum = true;
    for(auto lum : run.second) {
      if(!first_lum) file << ", ";
      file << "[" << lum.first << ", " << lum.second << "]";
      first_lum = false;
    }
    file << "]";
  }
  file << "\n}";
  file.close();
}

//-------------------------------------------------------
// Read in the (run, lumi) mask
bool initialize_mask(const char* mask) {
  if(!mask) true;
  ifstream file(mask);
  if(!file.is_open()) return false;
  string line;
  while(getline(file, line)) {
    while(line.size() > 0) {
      size_t run_l = line.find("\"");
      if(run_l > line.size()) break;
      line = line.substr(run_l+1, line.size());
      run_l = line.find("\"");
      string run_s = line.substr(0, run_l);
      unsigned run = stoi(run_s);
      line = line.substr(run_l+1, line.size());
      size_t start = line.find(": [[")+3; //lumi list range
      size_t end = line.find("]]")+1;
      string lumi_list = line.substr(start,end-start);
      mask_[run] = {};
      while(lumi_list.size() > 0) {
        size_t l_start = lumi_list.find("[")+1;
        size_t l_end = lumi_list.find(",");
        TString lum_lo = lumi_list.substr(l_start, l_end-l_start);
        l_start = l_end + 1;
        l_end = lumi_list.find("]");
        TString lum_hi = lumi_list.substr(l_start, l_end-l_start);
        lum_lo.Strip(); lum_hi.Strip();
        unsigned lum_lo_v = stoi(lum_lo.Data());
        unsigned lum_hi_v = stoi(lum_hi.Data());
        lumi_list = lumi_list.substr(l_end, lumi_list.size());
        l_start = lumi_list.find("[");
        lumi_list = (l_start > lumi_list.size()) ? "" : lumi_list.substr(l_start, lumi_list.size());
        mask_[run].push_back(pair<unsigned, unsigned>(lum_lo_v, lum_hi_v));
      }
    }
  }
  return true;
}

//-------------------------------------------------------
// Check if the (run, lumi) is in the mask
bool check_mask(unsigned run_in, unsigned lum_in) {
  for(auto run : mask_) {
    if(run.first == run_in) {
      for(auto lum : run.second) {
        if(lum.first <= lum_in && lum.second >= lum_in) return true;
      }
    }
  }
  return false;
}

//-------------------------------------------------------
// Add the lumi section to the list if not already there
void add_lum(vector<pair<unsigned, unsigned>>& lums, unsigned lum) {
  //loop through current looms to see if it fits in a list
  for(auto l : lums) {
    if(l.first <= lum && l.second >= lum) return; //already seen
  }
  //loop through to see if it can be appended to a list
  for(pair<unsigned, unsigned>& l : lums) {
    if(l.first == lum + 1) { //new low end
      l.first = lum;
      return;
    } else if(l.second == lum - 1) { //new high end
      l.second = lum;
      return;
    }
  }
  //add new lumi list
  lums.push_back(pair<unsigned, unsigned>(lum, lum));
}

//-------------------------------------------------------
// Process a single file
int lumi_from_mini_file(const char* file, const int verbose = 0) {

  // open the MINIAOD file
  TFile* f = nullptr;
  // try a few times to open the file
  const int max_attempts = 2;
  for(int iattempt = 0; iattempt < max_attempts; ++iattempt) {
    f = TFile::Open(file, "READ");
    if(f) break;
    else cout << "Attempt " << iattempt+1 << " failed to open file " << file << endl;
  }
  if(!f) {
    cout << "Failed to open file " << file << endl;
    return 1;
  }

  // retrieve the data block
  TTree* evtBlock = (TTree*) f->Get("Events");
  if(!evtBlock) {
    cout << "Data block not found\n";
    return 2;
  }

  // setup the data block
  edm::EventAuxiliary* evt = new edm::EventAuxiliary();
  evtBlock->SetBranchStatus("*", 0);
  evtBlock->SetBranchStatus("EventAuxiliary", 1);
  evtBlock->SetBranchAddress("EventAuxiliary", &evt);

  //loop through the data, checking against the lumi mask if provided
  const Long64_t entries = evtBlock->GetEntries();
  if(verbose > 0) cout << entries << " entries\n";
  for(Long64_t entry = 0; entry < entries; ++entry) {
    evtBlock->GetEntry(entry);
    unsigned lumiSection = evt->luminosityBlock();
    unsigned run = evt->run();
    if(verbose > 1) cout << " (run, lumi) = (" << run << ", " << lumiSection << ")\n";
    vector<pair<unsigned, unsigned>> lum_list;
    if(mask_.size() > 0 && !check_mask(run, lumiSection)) { //skip due to mask
      if(verbose > 1) cout << " --> skipping!\n";
      continue;
    }
    //add to the (run, lumi) list if not already in the list
    if(runs_.find(run) != runs_.end()) {
      lum_list = runs_[run];
    }
    add_lum(lum_list, lumiSection);
    runs_[run] = lum_list;
    //update the running count of accepted event
    ++npass_;
  }

  //update the total running count of uncut entries
  entries_ += entries;
  f->Close();
  delete evt;
  return 0;
}

//-------------------------------------------------------
// Process a file or file list
int lumi_from_mini(TString file, const char* out = "lumis.txt", const char* mask = nullptr, const int max_files = -1, const int verbose = 0) {

  if(mask && !initialize_mask(mask)) {
    cout << "Mask initialization failed!\n";
    return 3;
  }

  int nfiles(0), nfail(0);
  if(file.EndsWith(".txt")) { //assume a list of files
    ifstream input_list(file.Data());
    if(!input_list.is_open()) {
      cout << "Couldn't retrieve file list " << file.Data() << endl;
      return 10;
    }
    std::string line;
    //process each line in the file
    while(std::getline(input_list, line)) {
      if(line.size() == 0) continue;
      if(max_files > 0 && nfiles >= max_files) break;
      cout << "File: " << line.c_str() << endl;
      const int status = lumi_from_mini_file(line.c_str(), verbose);
      if(status != 0) {
        if(!skip_fail_) {
          cout << "Processing returned status " << status << endl;
          return status;
        } else ++nfail;
      }
      ++nfiles;
    }
    input_list.close();
  } else { //assume a single file
    const int status = lumi_from_mini_file(file.Data(), verbose);
    if(status != 0) {
      if(!skip_fail_) {
        cout << "Processing returned status " << status << endl;
        return status;
      } else ++nfail;
    }
    ++nfiles;
  }

  //print the lumi info out if verbose
  if(verbose > 0) {
    for(auto run : runs_) {
      cout << run.first << endl;
      for(auto list : run.second) {
        cout << " [" << list.first << ", " << list.second << "]";
      }
      cout << endl;
    }
  }

  //print the lumi info to disk
  print_lumis(out, runs_);

  //write out the event count information
  TString root_name = out;
  root_name.ReplaceAll(".txt" , ".root");
  root_name.ReplaceAll(".json", ".root");
  root_name.ReplaceAll(".JSON", ".root");
  TFile* fout = new TFile(root_name.Data(), "RECREATE");
  TH1* hevt = new TH1D("events", "events", 2, 0, 2);
  hevt->SetBinContent(1, entries_);
  hevt->SetBinContent(2, npass_);
  hevt->Write();
  fout->Close();

  if(skip_fail_) cout << "Of " << nfiles << " files, " << nfail << " failed processing\n";
  if(verbose > -1) cout << "Saw " << entries_ << " entries, " << npass_ << " passed (" << (npass_*100.)/entries_ << "%)\n";
  return 0;
}
