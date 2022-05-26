# this fake PSET is needed for local test and for crab to figure the output
# filename you do not need to edit it unless you want to do a local test using
# a different input file than the one marked below
#import FWCore.PythonUtilities.LumiList as LumiList
#import FWCore.ParameterSet.Types as CfgTypes
import FWCore.ParameterSet.Config as cms
process = cms.Process('NANO')
process.source = cms.Source(
    "PoolSource",
    fileNames=cms.untracked.vstring(),
    # lumisToProcess=cms.untracked.VLuminosityBlockRange("254231:1-254231:24")
)
process.source.fileNames = [
    'root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAOD/WJetsToLNu_HT-70To100_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/102X_upgrade2018_realistic_v15-v1/30000/0A998ABC-8469-3041-980E-4570396D4FF7.root'  # you can change only this line
]
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(10))
process.output = cms.OutputModule("PoolOutputModule",
                                  fileName=cms.untracked.string('tree.root'))
process.out = cms.EndPath(process.output)
