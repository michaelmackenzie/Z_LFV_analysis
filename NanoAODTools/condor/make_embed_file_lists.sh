#! /bin/bash

Help() {
    echo "Create embedding sample file lists using past job submission files"
    echo " 1: Year list"
    echo " 2: Final state list"
    echo " 3: Output directory (default = embed_file_lists)"
}
YEARS=$1
FINALSTATES=$2
OUTDIR=$3

if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
    Help
    exit
fi

if [[ "${YEARS}" == "" ]]; then
    YEARS="2016 2017 2018"
fi

if [[ "${FINALSTATES}" == "" ]]; then
    FINALSTATES="MuTau ETau EMu EE MuMu"
fi

if [[ "${OUTDIR}" == "" ]]; then
    OUTDIR="embed_file_lists"
fi

[ ! -d ${OUTDIR} ] && mkdir -p ${OUTDIR}

echo "Making file lists for years = ${YEARS}, final states = ${FINALSTATES}, with output directory ${OUTDIR}"

for YEAR in ${YEARS}
do
    if [[ "${YEAR}" == "2016" ]]; then
        RUNS="B C D E F G H";
    elif [[ "${YEAR}" == "2017" ]]; then
        RUNS="B C D E F"
    elif [[ "${YEAR}" == "2018" ]]; then
        RUNS="A B C D"
    else
        echo "Unknown year ${YEAR}"
        exit
    fi
    echo "Using ${RUNS} run list for ${YEAR}"
    for RUN in ${RUNS}
    do
        echo "Processing ${YEAR}${RUN}"
        for STATE in ${FINALSTATES}
        do
            FILE=`ls -td batch/*/dasQuery_*_Embed-${STATE}-${RUN}_${YEAR}.txt | head -n 1`
            if [[ ! -f ${FILE} ]]; then
                echo "No file for Embed-${STATE}-${RUN}_${YEAR}.txt found"
                continue
            fi
            if [[ ! -s ${FILE} ]]; then
                echo "Zero file size for file ${FILE} --> removing it"
                rm ${FILE}
                continue
            fi
            OUTFILE="${OUTDIR}/files_Embed-${STATE}-${RUN}_${YEAR}.txt"
            cp ${FILE} ${OUTFILE}
            if [[ ! -s ${OUTFILE} ]]; then
                echo "Zero file size for file ${OUTFILE} from ${FILE}"
                continue
            fi

        done
    done
done
