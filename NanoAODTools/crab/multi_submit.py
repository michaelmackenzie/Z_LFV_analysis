import os

samples="ZMuE_files.txt"
fltr="BkgDYJets2"
units="2" #2 for BKG/central signal; 10 for private signal; 2 for data
phys=False
lumibased=False # default: False both for data and MC

with open(samples,'r') as txt:
  lines=txt.readlines()
  for line in lines:
    sample=line.split(":")
    if len(sample)!=2:
       continue
    if (fltr != None) and (fltr not in sample[0]):
       continue
    if phys:
       cmd="python crab_cfg.py --phys --units "+units+" --name "+sample[0]+" --sample "+sample[1]
    else:
       cmd="python crab_cfg.py --units "+units+" --name "+sample[0]+" --sample "+sample[1]
    if lumibased:
       cmd+=" --lumibased"
    print "name",sample[0],"sample",sample[1]
    print cmd
    os.system(cmd)
