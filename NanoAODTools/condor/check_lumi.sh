#! /bin/bash

DATASET=$1
YEAR=$2
RUNS=$3
#use local json/ or eos
USELOCAL=$4

if [[ "${DATASET}" == "" ]]
then
    DATASET="SingleMuon"
fi
if [[ "${YEAR}" == "" ]]
then
    YEAR=2018
fi

if [[ "${RUNS}" == "" ]]
then
    if [[ "${YEAR}" == "2016" ]]
    then
        RUNS="B C D E F G H"
    elif
        [[ "${YEAR}" == "2017" ]]
    then
        RUNS="B C D E F"
    elif
        [[ "${YEAR}" == "2018" ]]
    then
        RUNS="A B C D"
    fi
fi

FILLER=""
if [[ "${DATASET}" == "Single"* ]]
then
    DATASET="${DATASET}Run${YEAR}"
fi
if [[ "${DATASET}" == "Embed"* ]]
then
    FILLER="-"
fi

[ ! -d lumi ] && mkdir lumi

if [[ "${USELOCAL}" == "" ]]; then
    OUTFILE="lumi/lumi_${DATASET}_${YEAR}.org"
else
    OUTFILE="lumi/${DATASET}_${YEAR}_json.org"
fi

echo "* Summary" >| ${OUTFILE}
echo "+-------+------+-------+-------+-------------------+------------------+" >> ${OUTFILE}
echo "| nfill | nrun | nls   | ncms  | totdelivered(/fb) | totrecorded(/fb) |" >> ${OUTFILE}
echo "+-------+------+-------+-------+-------------------+------------------+" >> ${OUTFILE}

NREC=0
for RUN in $RUNS
do
    if [[ "${USELOCAL}" == "" ]]; then
        BASE="/eos/cms/store/group/phys_smp/ZLFV/lfvanalysis_rootfiles/"
        FILE="${BASE}lumis_LFVAnalysis_${DATASET}${FILLER}${RUN}_${YEAR}.txt"
    else
        BASE="json/"
        FILE="${BASE}${DATASET}${FILLER}${RUN}_${YEAR}_json.txt"
    fi
    if [ -f ${FILE} ]
    then
        COMMAND="brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -u /fb -i"
        echo "${COMMAND} ${FILE}"
        RUNFILE=lumi/lumi_${DATASET}${FILLER}${RUN}_${YEAR}.org
        ${COMMAND} ${FILE} >| ${RUNFILE}
        awk -v d=0 '{
          if($1 == "#Summary:") {
            d = 1;
          } else if($1 ~ /Check/) {
            d = 0;
          } else if(d == 1 && !($1 ~ /+--/) && !($0 ~ /nfill/)) {
            print $0
           }
        }' ${RUNFILE} >> ${OUTFILE}
        SUMMARY=`tail -n 1 ${OUTFILE}`
        echo "+-------+------+-------+-------+-------------------+------------------+"
        echo "| nfill | nrun | nls   | ncms  | totdelivered(/fb) | totrecorded(/fb) |"
        echo ${SUMMARY}
        echo "+-------+------+-------+-------+-------------------+------------------+"
        NREC=`echo ${SUMMARY} | awk -v val1=${NREC} '{print val1+$(NF-1)}'`
        echo "Running lumi sum: ${NREC}"
        # tail -n 4 ${RUNFILE} | head -n 1 >> ${OUTFILE}
    else
        echo "Unknown lumi file ${FILE}"
    fi
done

echo "+-------+------+-------+-------+-------------------+------------------+" >> ${OUTFILE}
echo "|       |      |       |       |                   |    ${NREC}        |" >> ${OUTFILE}
echo "+-------+------+-------+-------+-------------------+------------------+" >> ${OUTFILE}
echo "#+TBLFM:" >> ${OUTFILE}
