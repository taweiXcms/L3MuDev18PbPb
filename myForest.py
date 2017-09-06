import FWCore.ParameterSet.Config as cms
process = cms.Process('HiForest')
process.options = cms.untracked.PSet()

#####################################################################################
# Input source
#####################################################################################

process.source = cms.Source("PoolSource",
                            duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
                            fileNames = cms.untracked.vstring(
#                                "file:samples/PbPb_MC_RECODEBUG.root"
"file:/afs/cern.ch/user/t/twang/public/L3MuDevFile/step3_MinBias_PbPb_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_1.root"

                                )
                            )

# Number of events we want to process, -1 = all events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)

#####################################################################################
# Load Global Tag, Geometry, etc.
#####################################################################################

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.Geometry.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')

from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '91X_mcRun2_HeavyIon_v3', '') #for now track GT manually, since centrality tables updated ex post facto
#process.HiForest.GlobalTagLabel = process.GlobalTag.globaltag

#from HeavyIonsAnalysis.Configuration.CommonFunctions_cff import overrideJEC_PbPb5020
#process = overrideJEC_PbPb5020(process)

process.load("RecoHI.HiCentralityAlgos.CentralityBin_cfi")

#####################################################################################
# Define tree output
#####################################################################################

process.TFileService = cms.Service("TFileService",
                                   fileName=cms.string("HiForestAOD.root"))


############################
# Event Analysis
############################
process.load('HeavyIonsAnalysis.EventAnalysis.hievtanalyzer_mc_cfi')
process.hiEvtAnalyzer.doMC = cms.bool(True) #general MC info
process.hiEvtAnalyzer.doHiMC = cms.bool(True) #HI specific MC info
process.load('HeavyIonsAnalysis.EventAnalysis.hltanalysis_cff')
process.hltanalysis.l1results                       = cms.InputTag("gtDigis")
process.hltanalysis.RunParameters.isData            = cms.untracked.bool(True)
process.hltanalysis.OfflinePrimaryVertices0 = cms.InputTag("hiSelectedVertex")
process.load('HeavyIonsAnalysis.EventAnalysis.hltobject_PbPb_cfi')
#process.load("HeavyIonsAnalysis.JetAnalysis.pfcandAnalyzer_cfi")
#process.pfcandAnalyzer.skipCharged = False
#process.pfcandAnalyzer.pfPtMin = 0
#process.load("HeavyIonsAnalysis.JetAnalysis.pfcandAnalyzerCS_cfi")
#process.pfcandAnalyzerCS.skipCharged = False
#process.pfcandAnalyzerCS.pfPtMin = 0

#########################
# Main analysis list
#########################

process.ana_step = cms.Path(
                             process.hltanalysis *  #stage2 HLT broken in 92X?
                            process.hltobject *
                            process.centralityBin *
                            process.hiEvtAnalyzer
							)


#####################################################################################

#########################
# Event Selection
#########################

process.load('HeavyIonsAnalysis.JetAnalysis.EventSelection_cff')
process.pcollisionEventSelection = cms.Path(process.collisionEventSelectionAOD)
process.pHBHENoiseFilterResultProducer = cms.Path( process.HBHENoiseFilterResultProducer )
process.HBHENoiseFilterResult = cms.Path(process.fHBHENoiseFilterResult)
process.HBHENoiseFilterResultRun1 = cms.Path(process.fHBHENoiseFilterResultRun1)
process.HBHENoiseFilterResultRun2Loose = cms.Path(process.fHBHENoiseFilterResultRun2Loose)
process.HBHENoiseFilterResultRun2Tight = cms.Path(process.fHBHENoiseFilterResultRun2Tight)
process.HBHEIsoNoiseFilterResult = cms.Path(process.fHBHEIsoNoiseFilterResult)
process.pprimaryVertexFilter = cms.Path(process.primaryVertexFilter )

process.load('HeavyIonsAnalysis.Configuration.hfCoincFilter_cff')
process.phfCoincFilter1 = cms.Path(process.hfCoincFilter)
process.phfCoincFilter2 = cms.Path(process.hfCoincFilter2)
process.phfCoincFilter3 = cms.Path(process.hfCoincFilter3)
process.phfCoincFilter4 = cms.Path(process.hfCoincFilter4)
process.phfCoincFilter5 = cms.Path(process.hfCoincFilter5)

process.pclusterCompatibilityFilter = cms.Path(process.clusterCompatibilityFilter)

process.pAna = cms.EndPath(process.skimanalysis)
