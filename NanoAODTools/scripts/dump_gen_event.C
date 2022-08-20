//Dump gen event info

int dump_gen_event(const char* file, int nevents = 1) {
  TFile* f = TFile::Open(file, "READ");
  if(!f) return 1;

  TTree* Events = (TTree*) f->Get("Events");
  if(!Events) {
    cout << "Events ntuple not found!\n";
    return 2;
  }

  Long64_t nentries = nevents < 0 ? Events->GetEntries() : nevents;

  //Data fields
  const int n = 500;
  UInt_t nGenPart;
  float GenPart_pt[n], GenPart_eta[n], GenPart_phi[n], GenPart_mass[n];
  int GenPart_pdgId[n], GenPart_status[n], GenPart_statusFlags[n], GenPart_genPartIdxMother[n];
  UInt_t nMuon;
  float Muon_pt[n], Muon_eta[n], Muon_phi[n], Muon_mass[n];
  int Muon_genPartIdx[n];
  UInt_t nElectron;
  float Electron_pt[n], Electron_eta[n], Electron_phi[n], Electron_mass[n];
  int Electron_genPartIdx[n];

  Events->SetBranchAddress("nGenPart"                , &nGenPart                );
  Events->SetBranchAddress("GenPart_pt"              , &GenPart_pt              );
  Events->SetBranchAddress("GenPart_eta"             , &GenPart_eta             );
  Events->SetBranchAddress("GenPart_phi"             , &GenPart_phi             );
  Events->SetBranchAddress("GenPart_mass"            , &GenPart_mass            );
  Events->SetBranchAddress("GenPart_pdgId"           , &GenPart_pdgId           );
  Events->SetBranchAddress("GenPart_status"          , &GenPart_status          );
  Events->SetBranchAddress("GenPart_statusFlags"     , &GenPart_statusFlags     );
  Events->SetBranchAddress("GenPart_genPartIdxMother", &GenPart_genPartIdxMother);

  Events->SetBranchAddress("nMuon"                   , &nMuon                   );
  Events->SetBranchAddress("Muon_pt"                 , &Muon_pt                 );
  Events->SetBranchAddress("Muon_eta"                , &Muon_eta                );
  Events->SetBranchAddress("Muon_phi"                , &Muon_phi                );
  Events->SetBranchAddress("Muon_mass"               , &Muon_mass               );
  Events->SetBranchAddress("Muon_genPartIdx"         , &Muon_genPartIdx         );

  Events->SetBranchAddress("nElectron"               , &nElectron               );
  Events->SetBranchAddress("Electron_pt"             , &Electron_pt             );
  Events->SetBranchAddress("Electron_eta"            , &Electron_eta            );
  Events->SetBranchAddress("Electron_phi"            , &Electron_phi            );
  Events->SetBranchAddress("Electron_mass"           , &Electron_mass           );
  Events->SetBranchAddress("Electron_genPartIdx"     , &Electron_genPartIdx     );

  for(Long64_t entry = 0; entry < nentries; ++entry) {
    Events->GetEntry(entry);
    cout << "*** Printing event information for entry " << entry << endl;

    //Gen particles
    cout << " N(gen particles) = " << nGenPart << endl;
    cout << " Idx:     pt       eta   phi      mass  pdgId   status    flags isDirectTauDecay isPromptTauDecay isLastCopy mother Idx\n";
    for(int ipart = 0; ipart < nGenPart; ++ipart) {
      printf(" %3i: %6.1f %9.2f %5.2f  %8.2e %6i %8i %8i        %i                %i            %i        %3i\n",
             ipart,
             GenPart_pt[ipart], GenPart_eta[ipart], GenPart_phi[ipart], GenPart_mass[ipart],
             GenPart_pdgId[ipart], GenPart_status[ipart], GenPart_statusFlags[ipart],
             (GenPart_statusFlags[ipart] & (1 << 4)) != 0,
             (GenPart_statusFlags[ipart] & (1 << 3)) != 0,
             (GenPart_statusFlags[ipart] & (1 << 13)) != 0,
             GenPart_genPartIdxMother[ipart]);
    }

    //Reco muons
    cout << " N(muons) = " << nMuon << endl;
    cout << " Idx:     pt       eta   phi      mass  Gen Idx\n";
    for(int ipart = 0; ipart < nMuon; ++ipart) {
      printf(" %3i: %6.1f %9.2f %5.2f  %8.2e %3i\n",
             ipart,
             Muon_pt[ipart], Muon_eta[ipart], Muon_phi[ipart], Muon_mass[ipart],
             Muon_genPartIdx[ipart]);
    }

    //Reco electrons
    cout << " N(electrons) = " << nElectron << endl;
    cout << " Idx:     pt       eta   phi      mass  Gen Idx\n";
    for(int ipart = 0; ipart < nElectron; ++ipart) {
      printf(" %3i: %6.1f %9.2f %5.2f  %8.2e %3i\n",
             ipart,
             Electron_pt[ipart], Electron_eta[ipart], Electron_phi[ipart], Electron_mass[ipart],
             Electron_genPartIdx[ipart]);
    }
  }
  f->Close();
  return 0;
}
