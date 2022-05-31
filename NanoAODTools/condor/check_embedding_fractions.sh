#! /bin/bash

YEAR=$1
FINALSTATES=$2
VERBOSE=$3

if [[ "${YEAR}" == "" ]]
then
    YEAR=2016
fi

if [[ "${FINALSTATES}" == "" ]]
then
    FINALSTATES="ElMu ElTau MuTau MuMu ElEl"
fi

if [[ "${VERBOSE}" == "" ]]
then
    VERBOSE=0
fi

RUNS="B C D E F G H"
if [[ "${YEAR}" == "2017" ]]
then
    RUNS="B C D E F"
elif [[ "${YEAR}" == "2018" ]]
then
    RUNS="A B C D"
fi

#Add the search tag for the MiniAOD dataset based on the year
MINITAG="FinalState-inputDoubleMu_94X"
if [[ "${YEAR}" == "2016" ]]
then
    MINITAG="FinalState-inputDoubleMu_94X_Legacy_miniAOD-v5"
elif [[ "${YEAR}" == "2018" ]]
then
    MINITAG="FinalState-inputDoubleMu_102X"
fi

#Loop through each final state for the given year
for FINALSTATE in $FINALSTATES
do
    NEVENTS_MINI=0
    NEVENTS_NANO=0
    for RUN in $RUNS
    do
        if [[ "${YEAR}" == "2016" ]]
        then
            FILE=`das_client -query="dataset=/EmbeddingRun${YEAR}${RUN}/pellicci-Embedded${FINALSTATE}_*10222V2*/USER instance=prod/phys03" 2>/dev/null | tail -n 1`
        else
            FILE=`das_client -query="dataset=/EmbeddingRun${YEAR}${RUN}/pellicci-Embedded${FINALSTATE}*/USER instance=prod/phys03" 2>/dev/null | tail -n 1`
        fi
        if [ ${VERBOSE} -gt 0 ]
        then
            echo "NanoAOD File = ${FILE}"
        fi
        if [[ "${FILE}" == "" ]]
        then
            echo "Error! NanoAOD file for Final state ${FINALSTATE}, Run ${RUN}, and Year ${YEAR} not found, continuing..."
            continue
        fi
        NNANO=`das_client -query="dataset=${FILE} instance=prod/phys03 | grep dataset.nevents" 2>/dev/null | awk '{if(NF == 1) print $0}' | xargs`
        if [ ${VERBOSE} -gt 0 ]
        then
            echo "Nano number = ${NNANO}"
        fi

        if [[ "${FINALSTATE}" == "ElEl" ]]
        then
            FILE=`das_client -query="dataset=/EmbeddingRun${YEAR}${RUN}/ElectronEmbedding*/USER instance=prod/phys03" 2>/dev/null | tail -n 1`
        elif [[ "${FINALSTATE}" == "MuMu" ]]
        then
             FILE=`das_client -query="dataset=/EmbeddingRun${YEAR}${RUN}/MuonEmbedding*/USER instance=prod/phys03" 2>/dev/null | tail -n 1`
        else
            FILE=`das_client -query="dataset=/EmbeddingRun${YEAR}${RUN}/${FINALSTATE}${MINITAG}*/USER instance=prod/phys03" 2>/dev/null | tail -n 1`
        fi
        if [ ${VERBOSE} -gt 0 ]
        then
            echo "MiniAOD File = ${FILE}"
        fi
        if [[ "${FILE}" == "" ]]
        then
            echo "Error! MiniAOD file for Final state ${FINALSTATE}, Run ${RUN}, and Year ${YEAR} not found, continuing..."
            continue
        fi
        NMINI=`das_client -query="dataset=${FILE} instance=prod/phys03 | grep dataset.nevents" 2>/dev/null | awk '{if(NF == 1) print $0}' | xargs`
        echo "Run ${YEAR}${RUN} Final State ${FINALSTATE}: Mini / Nano = ${NMINI}/${NNANO} = `echo "scale=4 ; $NMINI / $NNANO" | bc`"
        NEVENTS_NANO=$(($NNANO + $NEVENTS_NANO))
        NEVENTS_MINI=$(($NMINI + $NEVENTS_MINI))
    done
    echo "--- Total ${YEAR} ${FINALSTATE} Mini / Nano = ${NEVENTS_MINI}/${NEVENTS_NANO} = `echo "scale=4 ; $NEVENTS_MINI / $NEVENTS_NANO" | bc`"
done

echo "Processed all records"
