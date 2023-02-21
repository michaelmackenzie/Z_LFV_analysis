#!/bin/sh

echo "Job submitted on host `hostname` on `date`"
echo ">>> arguments: $@"

### Required parameters #####
COUNT=$1
YEAR=$2
SUFFIX=$4
OUTDIR=$5
ANALYZER=$6

if [[ "$3" == "True" ]]
then
    ISDATA="data"
else
    ISDATA="MC"
fi

### Transfer files, prepare directory ###
TOPDIR=$PWD

# lxplus/lpc
if [[ "${HOSTNAME}" == *"cern.ch"* ]]
then
    echo "Exporting the x509 token location (${USER})"
    export X509_USER_PROXY=/afs/cern.ch/user/m/mimacken/voms_proxy/x509up_u117705
fi

export SCRAM_ARCH=slc7_amd64_gcc820
export CMSSW_VERSION=CMSSW_10_6_29
source /cvmfs/cms.cern.ch/cmsset_default.sh

# temporary fix
tar -xzf source.tar.gz
mv $CMSSW_VERSION tmp_source
scram project CMSSW $CMSSW_VERSION
cp -r tmp_source/src/* $CMSSW_VERSION/src
cd $CMSSW_VERSION/src
eval `scram runtime -sh`

# this used to work, now it don't
#tar -xzf source.tar.gz
#cd $CMSSW_VERSION/src/
#scramv1 b ProjectRename

cmsenv
scramv1 b -j8 #ProjectRename
# cd BLT/BLTAnalysis/scripts
INPUT_TXT_FILENAME=input_${SUFFIX}_${COUNT}.txt
cp $TOPDIR/${INPUT_TXT_FILENAME} ${INPUT_TXT_FILENAME}

echo "Inputs: "
echo $ANALYZER $SUFFIX $YEAR $ISDATA $COUNT
echo "PATH: "
echo $PATH
echo "Starting working dir: "
pwd
cd PhysicsTools/NanoAODTools/
echo "Working dir: "
pwd
mv ../../input_${SUFFIX}_${COUNT}.txt ./
echo "Input file list: "
cat $INPUT_TXT_FILENAME
echo ""

[ ! -d outDir ] && mkdir outDir

### Run the analyzer

COUNTER=0
while IFS= read NANOAOD
do
    # xrdcp to local src folder first
    # analyzer is upto 100x-200x faster than xrd streaming. Ziheng
    echo "Copying ${NANOAOD} locally"
    date
    xrdcp -f ${NANOAOD} ./temp.root
    XRDEXIT=$?
    date
    if [[ $XRDEXIT -ne 0 ]]; then
        echo "!!! NANOAOD file couldn't be copied, re-trying"
        [ -f temp.root ] && rm temp.root
        xrdcp -f ${NANOAOD} ./temp.root
        XRDEXIT=$?
        date
        if [[ $XRDEXIT -ne 0 ]]; then
            rm *.root
            echo "exit code $XRDEXIT, failure in xrdcp"
            exit $XRDEXIT
        fi
    fi
    if [[ ! -f temp.root ]]; then
        echo "No temp file found, exit code 1, failure in xrdcp"
        exit 1
    fi
    if [[ ${NANOAOD} == *"Embedding"* ]]
    then
        ISDATA="Embedded"
    fi
    echo "python python/analyzers/${ANALYZER}.py temp.root ${ISDATA} ${YEAR}"
    python python/analyzers/${ANALYZER}.py temp.root ${ISDATA} ${YEAR}
    if [[ ! -f tree.root ]]; then
        echo "No tree file found, re-running ntupling job"
        ls -l *.root
        python python/analyzers/${ANALYZER}.py temp.root ${ISDATA} ${YEAR}
        if [[ ! -f tree.root ]]; then
            echo "No tree file found, exit code 1, failure in processing"
            ls *.root
            exit 1
        fi
        echo "Second tree processing was successful!"
    fi
    echo "Splitting the output tree into selection trees"
    time root.exe -q -b "condor/split_output_tree.C(\"tree.root\", \"tree-split.root\")"
    rm tree.root
    if [[ ! -f tree-split.root ]]; then
        echo "No split tree file found, exit code 1, failure in processing"
        exit 1
    fi

    echo "Adding event count normalization to the output tree"
    root.exe -q -b -l "condor/add_norm.C(\"temp.root\", \"tree-split.root\")"
    ROOTEXIT=$?
    if [[ ${ROOTEXIT} -ne 0 ]]; then
        echo "Normalization counting failed, exit code 1, failure in processing"
        exit 1
    fi
    mv tree-split.root outDir/tree_${COUNTER}.root
    #get luminosity info
    if [[ ${ISDATA} != "MC" ]]
    then
        python python/analyzers/LumiJSONAnalyzer.py temp.root ${ISDATA} ${YEAR}
        if [[ ! -f file_lumis_JSON.txt ]]
        then
            echo "Luminosity parsing failed!"
        else
            mv file_lumis_JSON.txt outDir/file_lumis_JSON_${COUNTER}.txt
        fi
    fi
    #clean up files
    rm *.root
    COUNTER=$((COUNTER+1))

done <$INPUT_TXT_FILENAME

ls
ls outDir/

### Copy output and cleanup ###
FILE=output_${SUFFIX}_${COUNT}.root
./haddnano.py ${FILE} outDir/*.root

#copy back the data file
for ATTEMPT in {1..10}
do
    echo "Attempt ${ATTEMPT}: Copying back merged file ${FILE} to ${OUTDIR}"
    date
    xrdcp -f ${FILE} ${OUTDIR}/${FILE} 2>&1
    XRDEXIT=$?
    date
    if [[ $XRDEXIT -ne 0 ]]; then
        sleep 60
        continue
    else
        break
    fi
done

if [[ $XRDEXIT -ne 0 ]]; then
    rm *.root
    echo "exit code $XRDEXIT, failure in xrdcp"
    exit $XRDEXIT
fi

#process lumi file if relevant
if [[ ${ISDATA} != "MC" ]]
then
    JSONFILE=lumis_${SUFFIX}_${COUNT}_JSON.txt
    python scripts/combine_json.py outDir/file_lumis_ --out_name ${JSONFILE}
    if [[ ! -f ${JSONFILE} ]]
    then
        echo "failure in lumi file processing, failed to produce merged file"
    else
        xrdcp -f ${JSONFILE} ${OUTDIR}/${JSONFILE} 2>&1
        XRDEXIT=$?
        if [[ $XRDEXIT -ne 0 ]]; then
            echo "exit code $XRDEXIT, failure in json lumi file xrdcp"
            cat ${JSONFILE}
        fi
        rm ${JSONFILE}
    fi
fi

rm ${FILE}
rm -rf outDir

echo "Finished processing"
