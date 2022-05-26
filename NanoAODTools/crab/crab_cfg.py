from CRABClient.UserUtilities import config, ClientException  #, getUsernameFromSiteDB

import argparse
import datetime

production_tag = datetime.date.today().strftime('%Y%b%d')

config = config()


config.section_("General")
config.General.transferLogs = False
#config.General.transferOutputs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_ZMuE.sh'
# hadd nano will not be needed once nano tools are in cmssw
config.JobType.allowUndistributedCMSSW = True
config.JobType.inputFiles = ['../python/postprocessing/run/runZMuE.py', 'haddnano.py', '../python/postprocessing/run/keep_and_drop_in.txt','../python/postprocessing/run/keep_and_drop_out.txt','../python/postprocessing/run/signal_files.py']
config.JobType.sendPythonFolder = True
config.section_("Data")
#config.Data.inputDBS = 'global'
#config.Data.splitting = 'FileBased'
#config.Data.unitsPerJob = 1
#config.Data.totalUnits = 10

config.Data.publication = False
#config.Data.outputDatasetTag = 'NanoTestPost'
config.section_("Site")

config.Site.storageSite = "T2_CH_CERN"
# config.section_("User")
#config.User.voGroup = 'dcms'

if __name__ == '__main__':

  from CRABAPI.RawCommand import crabCommand
  from CRABClient.ClientExceptions import ClientException
  from httplib import HTTPException
  from multiprocessing import Process

  def submit(config):
      try:
          crabCommand('submit', config = config)
      except HTTPException as hte:
          print "Failed submitting task: %s" % (hte.headers)
      except ClientException as cle:
          print "Failed submitting task: %s" % (cle)
  
  parser = argparse.ArgumentParser(description="My parser")
  parser.add_argument("--sample",dest='sample', type=str)
  parser.add_argument("--name",dest='name',type=str)
  parser.add_argument("--units",dest='units',type=int,default=1)
  parser.add_argument("--lumibased",dest='lumibased',action='store_true',default=False)
  parser.add_argument("--phys",dest='phys',action='store_true',default=False)
  
  args=parser.parse_args()

  
  config.General.workArea = 'Nano_'+args.name+"_"+str(production_tag)
  config.General.requestName = 'Nano_'+args.name+"_"+str(production_tag)
  config.Data.outLFNDirBase = '/store/group/cmst3/group/bpark/gkaratha/%s' % (config.General.workArea)
  config.Data.inputDataset = args.sample
  if args.phys:
    config.Data.inputDBS = 'phys03'
  else:
    config.Data.inputDBS = 'global'
  config.Data.unitsPerJob = args.units
  if args.lumibased:
     config.Data.splitting = 'LumiBased'
  else:
     config.Data.splitting = 'FileBased'


  print config
  submit(config)
 
