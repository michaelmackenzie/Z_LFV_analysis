#!/bin/sh

echo "Job submitted on host `hostname` on `date`"
echo ">>> arguments: $@"

### Required parameters #####
COUNT=$1
YEAR=$2
SUFFIX=$4
OUTDIR=$5
ANALYZER=$6

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

### Determine the JSON mask file
if [[ "${YEAR}" == "2016" ]]; then
    MASK="jsonn/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt"
elif  [[ "${YEAR}" == "2017" ]]; then
    MASK="json/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt"
else
    MASK="json/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt"
fi

### Run the analyzer
LUMIFILE="lumis_${SUFFIX}_${COUNT}.txt"
ROOTFILE="lumis_${SUFFIX}_${COUNT}.root"
time root.exe -q -b "scripts/lumi_from_mini.C(\"$INPUT_TXT_FILENAME\", \"${LUMIFILE}\", \"${MASK}\")"
ls

if [ ! -f ${LUMIFILE} ]; then
    echo "Failure in lumi file processing, exit code 10"
    exit 10
fi

if [ ! -f ${ROOTFILE} ]; then
    echo "Failure in root file processing, exit code 10"
    exit 10
fi

#match the standard output format
mv ${ROOTFILE} output_${SUFFIX}_${COUNT}.root
ROOTFILE="output_${SUFFIX}_${COUNT}.root"

### Copy output and cleanup ###

#copy back the data file
for ATTEMPT in {1..10}
do
    echo "Attempt ${ATTEMPT}: Copying back files ${ROOTFILE} and ${LUMIFILE} to ${OUTDIR}"
    date
    xrdcp -f ${ROOTFILE} ${OUTDIR}/${FILE} 2>&1
    ROOTEXIT=$?
    xrdcp -f ${LUMIFILE} ${OUTDIR}/${FILE} 2>&1
    LUMIEXIT=$?
    date
    if [[ $ROOTEXIT -ne 0 ]]; then
        sleep 60
        continue
    elif [[ $LUMIEXIT -ne 0 ]]; then
        sleep 60
        continue
    else
        break
    fi
done

if [[ $ROOTEXIT -ne 0 ]]; then
    rm *.root
    echo "exit code $ROOTEXIT, failure in xrdcp"
    exit $ROOTEXIT
elif [[ $LUMIEXIT -ne 0 ]]; then
    rm *.root
    echo "exit code $LUMIEXIT, failure in xrdcp"
    exit $LUMIEXIT
fi


rm ${ROOTFILE} ${LUMIFILE}

echo "Finished processing"
