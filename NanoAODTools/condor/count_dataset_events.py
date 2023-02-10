#Count the number of events in a dataset using DAS query and by looping over the files
import os
import sys
import math
from subprocess import PIPE, Popen
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]

datastring = sys.argv[1]

query = 'das_client -query="file dataset={}" >| input.txt'.format(datastring)
os.system(query)

filetxt = open('input.txt')
fileList = ["root://cmsxrootd.fnal.gov/" + f.strip() for f in filetxt.readlines()]
filetxt.close()

nFiles = len(fileList)

print "Found %i files" % (nFiles)
if nFiles <= 0:
    exit()

output = cmdline('das_client -query="dataset={} | grep dataset.nevents"'.format(datastring))
ndataset = -1
for l in output.splitlines():
    try: ndataset = int(l); break
    except: continue

#Three different methods for getting the number of events via ROOT files
method = 2 #0 = TChain; 1 = open each individually over XROOTD; 2 = copy each locally and then open
nentries = 0
if method == 0:
    chain = ROOT.TChain("Events")
    for file in fileList:
        chain.Add(file)
    nentries = chain.GetEntries()
elif method == 1:
    for i,file in enumerate(fileList):
        if i % 10 == 0:
            print "Processing file %6i..." % (i)
        f = ROOT.TFile.Open(file, 'READ')
        Events = f.Get("Events")
        nentries = nentries + Events.GetEntriesFast()
        f.Close()
        if i % 10 == 0:
            print "Finished processing file %6i..." % (i)
elif method == 2:
    for i,file in enumerate(fileList):
        os.system('xrdcp -f {} TEMP.root'.format(file))
        if i % 10 == 0:
            print "Processing file          %6i..." % (i)
        f = ROOT.TFile.Open('TEMP.root', 'READ')
        Events = f.Get("Events")
        nentries = nentries + Events.GetEntriesFast()
        f.Close()
        os.system('rm TEMP.root')
        if i % 10 == 0:
            print "Finished processing file %6i, N(entries) = %i..." % (i, nentries)

print "Found %i entries, dataset definition list %i entries" % (nentries, ndataset)
