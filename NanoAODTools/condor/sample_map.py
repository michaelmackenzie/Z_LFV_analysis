
class DataSample():
    '''Class for a single data sample information'''
    def __init__(self, name, year, isdata, path, inputDBS = "global", nEvtPerJob = 5,
                 user_redir = None, user_nfiles = 10, user_tag = None
    ):
        self._name       = name
        self._year       = year
        self._isdata     = isdata
        self._path       = path
        self._inputDBS   = inputDBS
        self._nEvtPerJob = nEvtPerJob

        #Access data samples not in DAS
        self._user_redir  = user_redir
        self._user_nfiles = user_nfiles
        self._user_tag    = user_tag

    def Print(self):
        print "DataSample:\n Name      : %s\n Year      : %i\n Data      : %o\n Path      : %s\n DBS       : %s\n N(evt)/job: %.2f" % (self._name, self._year,
                                                                                                                                       self._isdata, self._path,
                                                                                                                                       self._inputDBS, self._nEvtPerJob)
        if self._user_redir is not None:
            print " User redir: %s\n User N(files): %i\n" % (self._user_redir, self._user_nfiles)
            if self._user_tag is not None:
                print " User tag  : %s" % (self._user_tag)

class SampleMap():
    '''Class for storing data sample infomation'''
    def __init__(self):
        self._data = {}
        # self.load_samples(self._data)

    def load_data(self, data):
        #################################################
        #                                               #
        #---------------  Running data   ---------------#
        #                                               #
        #################################################

        # Single Electron
        data['2016_SingleElectron'] = [
            DataSample(name = "SingleElectronRun2016B", year = 2016, isdata = True, path = '/SingleElectron/Run2016B-02Apr2020_ver2-v1/NANOAOD'),
            DataSample(name = "SingleElectronRun2016C", year = 2016, isdata = True, path = '/SingleElectron/Run2016C-02Apr2020-v1/NANOAOD'     ),
            DataSample(name = "SingleElectronRun2016D", year = 2016, isdata = True, path = '/SingleElectron/Run2016D-02Apr2020-v1/NANOAOD'     ),
            DataSample(name = "SingleElectronRun2016E", year = 2016, isdata = True, path = '/SingleElectron/Run2016E-02Apr2020-v1/NANOAOD'     ),
            DataSample(name = "SingleElectronRun2016F", year = 2016, isdata = True, path = '/SingleElectron/Run2016F-02Apr2020-v1/NANOAOD'     ),
            DataSample(name = "SingleElectronRun2016G", year = 2016, isdata = True, path = '/SingleElectron/Run2016G-02Apr2020-v1/NANOAOD'     ),
            DataSample(name = "SingleElectronRun2016H", year = 2016, isdata = True, path = '/SingleElectron/Run2016H-02Apr2020-v1/NANOAOD'     ),
        ]
        data['2017_SingleElectron'] = [ 
            DataSample(name = 'SingleElectronRun2017B',  year = 2017, isdata = True, path = '/SingleElectron/Run2017B-02Apr2020-v1/NANOAOD'),
            DataSample(name = 'SingleElectronRun2017C',  year = 2017, isdata = True, path = '/SingleElectron/Run2017C-02Apr2020-v1/NANOAOD'),
            DataSample(name = 'SingleElectronRun2017D',  year = 2017, isdata = True, path = '/SingleElectron/Run2017D-02Apr2020-v1/NANOAOD'),
            DataSample(name = 'SingleElectronRun2017E',  year = 2017, isdata = True, path = '/SingleElectron/Run2017E-02Apr2020-v1/NANOAOD'),
            DataSample(name = 'SingleElectronRun2017F',  year = 2017, isdata = True, path = '/SingleElectron/Run2017F-02Apr2020-v1/NANOAOD'),
        ]
        data['2018_SingleElectron'] = [ 
            DataSample(name = 'SingleElectronRun2018A',  year = 2018, isdata = True, path = '/EGamma/Run2018A-02Apr2020-v1/NANOAOD'),
            DataSample(name = 'SingleElectronRun2018B',  year = 2018, isdata = True, path = '/EGamma/Run2018B-02Apr2020-v1/NANOAOD'),
            DataSample(name = 'SingleElectronRun2018C',  year = 2018, isdata = True, path = '/EGamma/Run2018C-02Apr2020-v1/NANOAOD'),
            DataSample(name = 'SingleElectronRun2018D',  year = 2018, isdata = True, path = '/EGamma/Run2018D-02Apr2020-v1/NANOAOD'),
        ]

        # Single Muon
        data['2016_SingleMuon'] = [
            DataSample(name = "SingleMuonRun2016B", year = 2016, isdata = True, path = '/SingleMuon/Run2016B-02Apr2020_ver2-v1/NANOAOD'),
            DataSample(name = "SingleMuonRun2016C", year = 2016, isdata = True, path = '/SingleMuon/Run2016C-02Apr2020-v1/NANOAOD'     ),
            DataSample(name = "SingleMuonRun2016D", year = 2016, isdata = True, path = '/SingleMuon/Run2016D-02Apr2020-v1/NANOAOD'     ),
            DataSample(name = "SingleMuonRun2016E", year = 2016, isdata = True, path = '/SingleMuon/Run2016E-02Apr2020-v1/NANOAOD'     ),
            DataSample(name = "SingleMuonRun2016F", year = 2016, isdata = True, path = '/SingleMuon/Run2016F-02Apr2020-v1/NANOAOD'     ),
            DataSample(name = "SingleMuonRun2016G", year = 2016, isdata = True, path = '/SingleMuon/Run2016G-02Apr2020-v1/NANOAOD'     ),
            DataSample(name = "SingleMuonRun2016H", year = 2016, isdata = True, path = '/SingleMuon/Run2016H-02Apr2020-v1/NANOAOD'     ),
        ]
        data['2017_SingleMuon'] = [ 
            DataSample(name = 'SingleMuonRun2017B',  year = 2017, isdata = True, path = '/SingleMuon/Run2017B-02Apr2020-v1/NANOAOD'),
            DataSample(name = 'SingleMuonRun2017C',  year = 2017, isdata = True, path = '/SingleMuon/Run2017C-02Apr2020-v1/NANOAOD'),
            DataSample(name = 'SingleMuonRun2017D',  year = 2017, isdata = True, path = '/SingleMuon/Run2017D-02Apr2020-v1/NANOAOD'),
            DataSample(name = 'SingleMuonRun2017E',  year = 2017, isdata = True, path = '/SingleMuon/Run2017E-02Apr2020-v1/NANOAOD'),
            DataSample(name = 'SingleMuonRun2017F',  year = 2017, isdata = True, path = '/SingleMuon/Run2017F-02Apr2020-v1/NANOAOD'),
        ]
        data['2018_SingleMuon'] = [ 
            DataSample(name = 'SingleMuonRun2018A',  year = 2018, isdata = True, path = '/SingleMuon/Run2018A-02Apr2020-v1/NANOAOD'),
            DataSample(name = 'SingleMuonRun2018B',  year = 2018, isdata = True, path = '/SingleMuon/Run2018B-02Apr2020-v1/NANOAOD'),
            DataSample(name = 'SingleMuonRun2018C',  year = 2018, isdata = True, path = '/SingleMuon/Run2018C-02Apr2020-v1/NANOAOD'),
            DataSample(name = 'SingleMuonRun2018D',  year = 2018, isdata = True, path = '/SingleMuon/Run2018D-02Apr2020-v1/NANOAOD'),
        ]

    def load_embed(self, data, include_mini = False):
        #################################################
        #                                               #
        #---------- Running Embedded Samples -----------#
        #                                               #
        #################################################

        # 2016 Embedded samples
        data['2016_embed_emu'] = [
            DataSample(path='/EmbeddingRun2016B/pellicci-EmbeddedElMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-EMu-B', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016C/pellicci-EmbeddedElMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-EMu-C', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016D/pellicci-EmbeddedElMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-EMu-D', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016E/pellicci-EmbeddedElMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-EMu-E', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016F/pellicci-EmbeddedElMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-EMu-F', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016G/pellicci-EmbeddedElMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-EMu-G', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016H/pellicci-EmbeddedElMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-EMu-H', inputDBS="phys03"),
        ]
        data['2016_embed_etau'] = [
            DataSample(path='/EmbeddingRun2016B/pellicci-EmbeddedElTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-ETau-B', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016C/pellicci-EmbeddedElTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-ETau-C', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016D/pellicci-EmbeddedElTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-ETau-D', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016E/pellicci-EmbeddedElTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-ETau-E', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016F/pellicci-EmbeddedElTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-ETau-F', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016G/pellicci-EmbeddedElTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-ETau-G', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016H/pellicci-EmbeddedElTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-ETau-H', inputDBS="phys03"),
        ]
        data['2016_embed_mutau'] = [
            DataSample(path='/EmbeddingRun2016B/pellicci-EmbeddedMuTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-MuTau-B', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016C/pellicci-EmbeddedMuTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-MuTau-C', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016D/pellicci-EmbeddedMuTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-MuTau-D', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016E/pellicci-EmbeddedMuTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-MuTau-E', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016F/pellicci-EmbeddedMuTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-MuTau-F', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016G/pellicci-EmbeddedMuTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-MuTau-G', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016H/pellicci-EmbeddedMuTau_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-MuTau-H', inputDBS="phys03"),
        ]
        data['2016_embed_ee'] = [
            DataSample(path='/EmbeddingRun2016B/pellicci-EmbeddedElEl_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-EE-B', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016C/pellicci-EmbeddedElEl_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-EE-C', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016D/pellicci-EmbeddedElEl_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-EE-D', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016E/pellicci-EmbeddedElEl_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-EE-E', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016F/pellicci-EmbeddedElEl_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-EE-F', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016G/pellicci-EmbeddedElEl_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-EE-G', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016H/pellicci-EmbeddedElEl_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-EE-H', inputDBS="phys03"),
        ]
        data['2016_embed_mumu'] = [
            DataSample(path='/EmbeddingRun2016B/pellicci-EmbeddedMuMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-MuMu-B', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016C/pellicci-EmbeddedMuMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-MuMu-C', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016D/pellicci-EmbeddedMuMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-MuMu-D', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016E/pellicci-EmbeddedMuMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-MuMu-E', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016F/pellicci-EmbeddedMuMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-MuMu-F', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016G/pellicci-EmbeddedMuMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-MuMu-G', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2016H/pellicci-EmbeddedMuMu_NANOAOD_10222V2-eb4bd41e0cecc0e67477f0cf9aac775c/USER',
                       year=2016, isdata=False, name='Embed-MuMu-H', inputDBS="phys03"),
        ]

        # 2017 Embedded samples
        data['2017_embed_emu'] = [
            DataSample(path='/EmbeddingRun2017B/pellicci-EmbeddedElMu_NANOAOD_10222V2-6e995938c955340423734eed12836829/USER',
                       year=2017, isdata=False, name='Embed-EMu-B', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2017C/pellicci-EmbeddedElMu_NANOAOD_10222V4-6e995938c955340423734eed12836829/USER',
                       year=2017, isdata=False, name='Embed-EMu-C', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2017D/pellicci-EmbeddedElMu_NANOAOD_10222V4-6e995938c955340423734eed12836829/USER',
                       year=2017, isdata=False, name='Embed-EMu-D', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2017E/pellicci-EmbeddedElMu_NANOAOD_10222V4-6e995938c955340423734eed12836829/USER',
                       year=2017, isdata=False, name='Embed-EMu-E', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2017F/pellicci-EmbeddedElMu_NANOAOD_10222V4-6e995938c955340423734eed12836829/USER',
                       year=2017, isdata=False, name='Embed-EMu-F', inputDBS="phys03"),
        ]
        data['2017_embed_etau'] = [
            DataSample(path='/EmbeddingRun2017B/pellicci-EmbeddedElTau_NANOAOD_10222V2-6e995938c955340423734eed12836829/USER',
                       year=2017, isdata=False, name='Embed-ETau-B', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2017C/pellicci-EmbeddedElTau_NANOAOD_10222V4-6e995938c955340423734eed12836829/USER',
                       year=2017, isdata=False, name='Embed-ETau-C', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2017D/pellicci-EmbeddedElTau_NANOAOD_10222V4-6e995938c955340423734eed12836829/USER',
                       year=2017, isdata=False, name='Embed-ETau-D', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2017E/pellicci-EmbeddedElTau_NANOAOD_10222V4-6e995938c955340423734eed12836829/USER',
                       year=2017, isdata=False, name='Embed-ETau-E', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2017F/pellicci-EmbeddedElTau_NANOAOD_10222V4-6e995938c955340423734eed12836829/USER',
                       year=2017, isdata=False, name='Embed-ETau-F', inputDBS="phys03"),
        ]
        data['2017_embed_mutau'] = [
            DataSample(path='/EmbeddingRun2017B/pellicci-EmbeddedMuTau_NANOAOD_10222V2-6e995938c955340423734eed12836829/USER',
                       year=2017, isdata=False, name='Embed-MuTau-B', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2017C/pellicci-EmbeddedMuTau_NANOAOD_10222V4-6e995938c955340423734eed12836829/USER',
                       year=2017, isdata=False, name='Embed-MuTau-C', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2017D/pellicci-EmbeddedMuTau_NANOAOD_10222V4-6e995938c955340423734eed12836829/USER',
                       year=2017, isdata=False, name='Embed-MuTau-D', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2017E/pellicci-EmbeddedMuTau_NANOAOD_10222V4-6e995938c955340423734eed12836829/USER',
                       year=2017, isdata=False, name='Embed-MuTau-E', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2017F/pellicci-EmbeddedMuTau_NANOAOD_10222V4-6e995938c955340423734eed12836829/USER',
                       year=2017, isdata=False, name='Embed-MuTau-F', inputDBS="phys03"),
        ]
        data['2017_embed_ee'] = [
            DataSample(path='/EmbeddingRun2017B/pellicci-EmbeddedElEl_NANOAOD_10222V2-6e995938c955340423734eed12836829/USER',
                       year=2017, isdata=False, name='Embed-EE-B', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2017C/pellicci-EmbeddedElEl_NANOAOD_10222V2-6e995938c955340423734eed12836829/USER',
                       year=2017, isdata=False, name='Embed-EE-C', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2017D/pellicci-EmbeddedElEl_NANOAOD_10222V4-6e995938c955340423734eed12836829/USER',
                       year=2017, isdata=False, name='Embed-EE-D', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2017E/pellicci-EmbeddedElEl_NANOAOD_10222V4-6e995938c955340423734eed12836829/USER',
                       year=2017, isdata=False, name='Embed-EE-E', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2017F/pellicci-EmbeddedElEl_NANOAOD_10222V4-6e995938c955340423734eed12836829/USER',
                       year=2017, isdata=False, name='Embed-EE-F', inputDBS="phys03"),
        ]
        data['2017_embed_mumu'] = [
            DataSample(path='/EmbeddingRun2017B/pellicci-EmbeddedMuMu_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
                       year=2017, isdata=False, name='Embed-MuMu-B', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2017C/pellicci-EmbeddedMuMu_NANOAOD_10222V2-6e995938c955340423734eed12836829/USER',
                       year=2017, isdata=False, name='Embed-MuMu-C', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2017D/pellicci-EmbeddedMuMu_NANOAOD_10222V2-6e995938c955340423734eed12836829/USER',
                       year=2017, isdata=False, name='Embed-MuMu-D', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2017E/pellicci-EmbeddedMuMu_NANOAOD_10222V4-6e995938c955340423734eed12836829/USER',
                       year=2017, isdata=False, name='Embed-MuMu-E', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2017F/pellicci-EmbeddedMuMu_NANOAOD_10222V1-6e995938c955340423734eed12836829/USER',
                       year=2017, isdata=False, name='Embed-MuMu-F', inputDBS="phys03"),
        ]

        # 2018 Embedded samples
        data['2018_embed_emu'] = [
            DataSample(path='/EmbeddingRun2018A/pellicci-EmbeddedElMu_NANOAOD_2018_10222V2-9b11f648cb233dc346c2d0860bbea8f9/USER',
                       year=2018, isdata=False, name='Embed-EMu-A', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2018B/pellicci-EmbeddedElMu_NANOAOD_2018_10222V2-9b11f648cb233dc346c2d0860bbea8f9/USER',
                       year=2018, isdata=False, name='Embed-EMu-B', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2018C/pellicci-EmbeddedElMu_NANOAOD_2018_10222V2-9b11f648cb233dc346c2d0860bbea8f9/USER',
                       year=2018, isdata=False, name='Embed-EMu-C', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2018D/pellicci-EmbeddedElMu_NANOAOD_2018_10222V4-9b11f648cb233dc346c2d0860bbea8f9/USER',
                       year=2018, isdata=False, name='Embed-EMu-D', inputDBS="phys03"),
        ]
        data['2018_embed_etau'] = [
            DataSample(path='/EmbeddingRun2018A/pellicci-EmbeddedElTau_NANOAOD_2018_10222V2-9b11f648cb233dc346c2d0860bbea8f9/USER',
                       year=2018, isdata=False, name='Embed-ETau-A', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2018B/pellicci-EmbeddedElTau_NANOAOD_2018_10222V2-9b11f648cb233dc346c2d0860bbea8f9/USER',
                       year=2018, isdata=False, name='Embed-ETau-B', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2018C/pellicci-EmbeddedElTau_NANOAOD_2018_10222V2-9b11f648cb233dc346c2d0860bbea8f9/USER',
                       year=2018, isdata=False, name='Embed-ETau-C', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2018D/pellicci-EmbeddedElTau_NANOAOD_2018_10222V4-9b11f648cb233dc346c2d0860bbea8f9/USER',
                       year=2018, isdata=False, name='Embed-ETau-D', inputDBS="phys03"),
        ]
        data['2018_embed_mutau'] = [
            DataSample(path='/EmbeddingRun2018A/pellicci-EmbeddedMuTau_NANOAOD_2018_10222V2-9b11f648cb233dc346c2d0860bbea8f9/USER',
                       year=2018, isdata=False, name='Embed-MuTau-A', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2018B/pellicci-EmbeddedMuTau_NANOAOD_2018_10222V2-9b11f648cb233dc346c2d0860bbea8f9/USER',
                       year=2018, isdata=False, name='Embed-MuTau-B', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2018C/pellicci-EmbeddedMuTau_NANOAOD_2018_10222V2-9b11f648cb233dc346c2d0860bbea8f9/USER',
                       year=2018, isdata=False, name='Embed-MuTau-C', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2018D/pellicci-EmbeddedMuTau_NANOAOD_2018_10222V4-9b11f648cb233dc346c2d0860bbea8f9/USER',
                       year=2018, isdata=False, name='Embed-MuTau-D', inputDBS="phys03"),
        ]
        data['2018_embed_ee'] = [
            DataSample(path='/EmbeddingRun2018A/pellicci-EmbeddedElEl_NANOAOD_2018_10222V2-9b11f648cb233dc346c2d0860bbea8f9/USER',
                       year=2018, isdata=False, name='Embed-EE-A', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2018B/pellicci-EmbeddedElEl_NANOAOD_2018_10222V2-9b11f648cb233dc346c2d0860bbea8f9/USER',
                       year=2018, isdata=False, name='Embed-EE-B', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2018C/pellicci-EmbeddedElEl_NANOAOD_2018_10222V2-9b11f648cb233dc346c2d0860bbea8f9/USER',
                       year=2018, isdata=False, name='Embed-EE-C', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2018D/pellicci-EmbeddedElEl_NANOAOD_2018_10222V4-9b11f648cb233dc346c2d0860bbea8f9/USER',
                       year=2018, isdata=False, name='Embed-EE-D', inputDBS="phys03"),
        ]
        data['2018_embed_mumu'] = [
            DataSample(path='/EmbeddingRun2018A/pellicci-EmbeddedMuMu_NANOAOD_2018_10222V2-9b11f648cb233dc346c2d0860bbea8f9/USER',
                       year=2018, isdata=False, name='Embed-MuMu-A', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2018B/pellicci-EmbeddedMuMu_NANOAOD_2018_10222V2-9b11f648cb233dc346c2d0860bbea8f9/USER',
                       year=2018, isdata=False, name='Embed-MuMu-B', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2018C/pellicci-EmbeddedMuMu_NANOAOD_2018_10222V1-9b11f648cb233dc346c2d0860bbea8f9/USER',
                       year=2018, isdata=False, name='Embed-MuMu-C', inputDBS="phys03"),
            DataSample(path='/EmbeddingRun2018D/pellicci-EmbeddedMuMu_NANOAOD_2018_10222V4-9b11f648cb233dc346c2d0860bbea8f9/USER',
                       year=2018, isdata=False, name='Embed-MuMu-D', inputDBS="phys03"),
        ]

        ###############################################
        # MINIAOD paths
        ###############################################

        if include_mini:
            # 2017 Embedded samples
            data['2017_embed_mini_emu'] = [
                DataSample(path='/EmbeddingRun2017B/ElMuFinalState-inputDoubleMu_94X_miniAOD-v2/USER',
                           year=2017, isdata=False, name='Embed-MINI-EMu-B', inputDBS="phys03"),
                DataSample(path='/EmbeddingRun2017C/ElMuFinalState-inputDoubleMu_94X_miniAOD-v2/USER',
                           year=2017, isdata=False, name='Embed-MINI-EMu-C', inputDBS="phys03"),
                DataSample(path='/EmbeddingRun2017D/ElMuFinalState-inputDoubleMu_94X_miniAOD-v2/USER',
                           year=2017, isdata=False, name='Embed-MINI-EMu-D', inputDBS="phys03"),
                DataSample(path='/EmbeddingRun2017E/ElMuFinalState-inputDoubleMu_94X_miniAOD-v2/USER',
                           year=2017, isdata=False, name='Embed-MINI-EMu-E', inputDBS="phys03"),
                DataSample(path='/EmbeddingRun2017F/ElMuFinalState-inputDoubleMu_94X_miniAOD-v2/USER',
                           year=2017, isdata=False, name='Embed-MINI-EMu-F', inputDBS="phys03"),
            ]
            data['2017_embed_mini_etau'] = [
                DataSample(path='/EmbeddingRun2017B/ElTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER',
                           year=2017, isdata=False, name='Embed-MINI-ETau-B', inputDBS="phys03"),
                DataSample(path='/EmbeddingRun2017C/ElTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER',
                           year=2017, isdata=False, name='Embed-MINI-ETau-C', inputDBS="phys03"),
                DataSample(path='/EmbeddingRun2017D/ElTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER',
                           year=2017, isdata=False, name='Embed-MINI-ETau-D', inputDBS="phys03"),
                DataSample(path='/EmbeddingRun2017E/ElTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER',
                           year=2017, isdata=False, name='Embed-MINI-ETau-E', inputDBS="phys03"),
                DataSample(path='/EmbeddingRun2017F/ElTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER',
                           year=2017, isdata=False, name='Embed-MINI-ETau-F', inputDBS="phys03"),
            ]
            data['2017_embed_mini_mutau'] = [
                DataSample(path='/EmbeddingRun2017B/MuTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER',
                           year=2017, isdata=False, name='Embed-MINI-MuTau-B', inputDBS="phys03"),
                DataSample(path='/EmbeddingRun2017C/MuTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER',
                           year=2017, isdata=False, name='Embed-MINI-MuTau-C', inputDBS="phys03"),
                DataSample(path='/EmbeddingRun2017D/MuTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER',
                           year=2017, isdata=False, name='Embed-MINI-MuTau-D', inputDBS="phys03"),
                DataSample(path='/EmbeddingRun2017E/MuTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER',
                           year=2017, isdata=False, name='Embed-MINI-MuTau-E', inputDBS="phys03"),
                DataSample(path='/EmbeddingRun2017F/MuTauFinalState-inputDoubleMu_94X_miniAOD-v2/USER',
                           year=2017, isdata=False, name='Embed-MINI-MuTau-F', inputDBS="phys03"),
            ]
            data['2017_embed_mini_ee'] = [
                DataSample(path='/EmbeddingRun2017B/ElectronEmbedding-inputDoubleMu_94X_miniAOD-v2/USER',
                           year=2017, isdata=False, name='Embed-MINI-EE-B', inputDBS="phys03"),
                DataSample(path='/EmbeddingRun2017C/ElectronEmbedding-inputDoubleMu_94X_miniAOD-v2/USER',
                           year=2017, isdata=False, name='Embed-MINI-EE-C', inputDBS="phys03"),
                DataSample(path='/EmbeddingRun2017D/ElectronEmbedding-inputDoubleMu_94X_miniAOD-v2/USER',
                           year=2017, isdata=False, name='Embed-MINI-EE-D', inputDBS="phys03"),
                DataSample(path='/EmbeddingRun2017E/ElectronEmbedding-inputDoubleMu_94X_miniAOD-v2/USER',
                           year=2017, isdata=False, name='Embed-MINI-EE-E', inputDBS="phys03"),
                DataSample(path='/EmbeddingRun2017F/ElectronEmbedding-inputDoubleMu_94X_miniAOD-v2/USER',
                           year=2017, isdata=False, name='Embed-MINI-EE-F', inputDBS="phys03"),
            ]
            data['2017_embed_mini_mumu'] = [
                DataSample(path='/EmbeddingRun2017B/MuonEmbedding-inputDoubleMu_94X_miniAOD-v2/USER',
                           year=2017, isdata=False, name='Embed-MINI-MuMu-B', inputDBS="phys03"),
                DataSample(path='/EmbeddingRun2017C/MuonEmbedding-inputDoubleMu_94X_miniAOD-v2/USER',
                           year=2017, isdata=False, name='Embed-MINI-MuMu-C', inputDBS="phys03"),
                DataSample(path='/EmbeddingRun2017D/MuonEmbedding-inputDoubleMu_94X_miniAOD-v2/USER',
                           year=2017, isdata=False, name='Embed-MINI-MuMu-D', inputDBS="phys03"),
                DataSample(path='/EmbeddingRun2017E/MuonEmbedding-inputDoubleMu_94X_miniAOD-v2/USER',
                           year=2017, isdata=False, name='Embed-MINI-MuMu-E', inputDBS="phys03"),
                DataSample(path='/EmbeddingRun2017F/MuonEmbedding-inputDoubleMu_94X_miniAOD-v2/USER',
                           year=2017, isdata=False, name='Embed-MINI-MuMu-F', inputDBS="phys03"),
            ]
            
    def load_samples(self, data, include_mini = False):
        self.load_data(data)
        self.load_embed(data, include_mini)

