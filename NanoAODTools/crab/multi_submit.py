import os


from ZMuE_files import samples_out
print samples_out

fltr="SgnZMuE"
submit=True #to test the command before submit


for sample in samples_out:
   if (fltr!=None) and (fltr not in sample["Name"]):
     continue
   cmd="python crab_cfg.py --name "+sample["Name"]+" --sample "+sample["Path"]+" --units "+sample["Units"]
   opt = 'options={"outputName":None,"build_GenSignalDecay_ZMuE":'+str(sample["GenZMuE"])+',"build_GenSignalDecay_ZMuTau":'+str(sample["GenZMuTau"])+',"build_GenSignalDecay_ZETau":'+str(sample["GenZETau"])+',"Data":'+str(sample["Data"])+'}'
   with open("options_ZMuE.py","w") as txt:
     txt.write(opt)
   txt.close()

   if sample["Phys3"]:
      cmd+=" --phys"
   if sample["Lumibased"]:
      cmd+=" --lumibased"
   print "name",sample["Name"],"sample",sample["Path"]
   print cmd
   if submit:
      os.system(cmd)
   os.system('wait')
