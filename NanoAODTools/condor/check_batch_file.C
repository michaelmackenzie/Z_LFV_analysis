int check_batch_file(const char* file) {
  TFile* f = TFile::Open(file, "READ");
  if(!f) return 1;
  if(!f->Get("Events")) return 2;
  if(!f->Get("events")) return 3;
  return 0;
}
