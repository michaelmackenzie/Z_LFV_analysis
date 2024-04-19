//Test the effect on the normalization due to the theory scale weights

int test_theory_scale_norm_effect(TString file, const char* cut = "1") {

  if(file.BeginsWith("/store")) file = "root://cmsxrootd.fnal.gov//" + file;
  TFile* f = TFile::Open(file.Data(), "READ");
  if(!f) return 1;

  TTree* t = (TTree*) f->Get("Events");
  if(!t) return 2;

  TH1* h = new TH1D("h", "h", 1, -1.e10, 1.e10);

  //Get the nominal yield
  t->Draw("LHEScaleWeight[4] >> h", Form("LHEScaleWeight[4]/LHEScaleWeight[4]*(%s)", cut), "goff");
  const double nominal = h->Integral();

  //test renomalization scale (weight indices 1 and 7 correspond to 0.5 and 2)
  t->Draw("LHEScaleWeight[4] >> h", Form("LHEScaleWeight[1]/LHEScaleWeight[4]*(%s)", cut), "goff");
  const double val_r_down = h->Integral();
  t->Draw("LHEScaleWeight[4] >> h", Form("LHEScaleWeight[7]/LHEScaleWeight[4]*(%s)", cut), "goff");
  const double val_r_up = h->Integral();

  printf("Integral changes from %.1f to %.1f/%.1f (%.3f/%.3f) for up/down renormalization scale shifts\n",
         nominal, val_r_up, val_r_down, val_r_up/nominal, val_r_down/nominal);

  //test factorization scale (weight indices 3 and 5 correspond to 0.5 and 2)
  t->Draw("LHEScaleWeight[4] >> h", Form("LHEScaleWeight[3]/LHEScaleWeight[4]*(%s)", cut), "goff");
  const double val_f_down = h->Integral();
  t->Draw("LHEScaleWeight[4] >> h", Form("LHEScaleWeight[5]/LHEScaleWeight[4]*(%s)", cut), "goff");
  const double val_f_up = h->Integral();

  printf("Integral changes from %.1f to %.1f/%.1f (%.3f/%.3f) for up/down factorization scale shifts\n",
         nominal, val_f_up, val_f_down, val_f_up/nominal, val_f_down/nominal);
  return 0;
}
