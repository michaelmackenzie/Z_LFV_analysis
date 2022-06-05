JOBNAME=$1
CHECKFILES=$2
RESUBMIT=$3 #"" for nothing, "dryrun" to prepare resubmission, anything else (e.g. "d") to perform resubmission
TAG=$4 #dataset tag to consider
EOSDIR=$5
VERBOSE=$6

if [[ "${EOSDIR}" == "" ]]
then
    EOSDIR="nano_batchout"
fi

echo "Using EOS directory ${EOSDIR}"

if [[ "${VERBOSE}" == "" ]]
then
    VERBOSE=0
else
    echo "Using verbose level ${VERBOSE}"
fi

if [[ "${JOBNAME}" == "" ]]
then
    echo "No jobname given, should be a job listed in batch directory"
else
    NFAILED=0
    echo "Using jobname ${JOBNAME}"
    FAILEDJOBS=""
    for f in `ls -d ${JOBNAME}reports/*.log`
    do
        FILE=`basename ${f} | awk -F "_" '{name=""; for( i = 1; i < NF - 1; i++){ name=name $i; if(i < NF - 2) {name=name "_";}}}END{print name}'`
        JOB=`echo ${f} | awk -F "/" '{print $2}'`
        if  grep -q "${TAG}" <<< "${FILE}"
        then
            if [ ${VERBOSE} -gt 0 ]
            then
                echo "Checking file ${FILE} in job ${JOB}"
            fi
        else
            if [ ${VERBOSE} -gt 0 ]
            then
                echo "Skipping file ${FILE} as tag ${TAG} not found"
            fi
            continue
        fi
        STDLOG="${f/log/stdout}"
        if [ ! -f ${STDLOG} ]
        then
            if [ ${VERBOSE} -gt -1 ]
            then
                echo "Stdout file ${STDLOG} does not exist"
            fi
        else
            XRDEXIT=`grep "exit code" ${STDLOG} | grep "xrdcp"`
            if [[ "${XRDEXIT}" != "" ]]
            then
                echo "xrdcp failed in file ${STDOUT}: ${XRDEXIT}"
                FAILEDJOBS="${FAILEDJOBS} ${FILE}"
                NFAILED=$((1 + $NFAILED))
            fi
        fi
        ROOTFILE="/eos/uscms/store/user/${USER}/${EOSDIR}/${JOB}/output_${FILE}.root"
        if [ ! -f ${ROOTFILE} ]
        then
            if [ ${VERBOSE} -gt -1 ]
            then
                echo "File ${FILE} in job ${JOB} does not exist"
            fi
            if [[ "${XRDEXIT}" == "" ]]
            then
                FAILEDJOBS="${FAILEDJOBS} ${FILE}"
                NFAILED=$((1 + $NFAILED))
            fi
        elif [[ "${CHECKFILES}" != "" ]]
        then
            root.exe -q -l -b "check_batch_file.C(\"${ROOTFILE}\")"
            ROOTSTATUS=$?
            if [[ $ROOTSTATUS -ne 0 ]]
            then
                echo "File ${FILE} failed ROOT file checking"
                #only add it if it hasn't already failed a check
                if [[ "${XRDEXIT}" == "" ]]
                then
                    FAILEDJOBS="${FAILEDJOBS} ${FILE}"
                    NFAILED=$((1 + $NFAILED))
                fi
            fi
        fi
    done
    echo "${NFAILED} jobs failed checks"

    if [[ "${RESUBMIT}" != "" ]]
    then
        if [[ "${FAILEDJOBS}" != "" ]]
        then
            rm ${JOBNAME}recover_*.jdl
        fi
        for FILE in ${FAILEDJOBS}
        do
            DATASET=`echo ${FILE} | awk -F "_" '{name=""; for( i = 1; i < NF; i++){ name=name $i; if(i < NF - 1) {name=name "_";}}}END{print name}'`
            RECOVERY=${JOBNAME}recover_${DATASET}.jdl
            JOBINFO=${JOBNAME}batchJob_${DATASET}.jdl
            COUNT=`echo ${FILE} | awk -F "_" '{print $NF}'`
            if [ ! -f "${RECOVERY}" ]
            then
                echo "Creating recovery jdl for dataset ${DATASET}"
                cat ${JOBINFO} | awk -v d=0 '{if($1 == "Arguments") d=1; if(d == 0) print $0}' > ${RECOVERY}
            fi
            echo "Adding job ${FILE} to recovery file for dataset ${DATASET}"
            cat ${JOBINFO} | awk -v d=0 -v count=${COUNT} '{if($1 == "Arguments") {if($3 == count) {d=1;} else {d=0;}}  if(d==1) {print $0;}}' >> ${RECOVERY}
            if [[ "${RESUBMIT}" != "" ]]
            then
                echo "Storing previous records for this failed job in recovery directory"
                mkdir -p batch/recovery/${JOBNAME}
                mv ${JOBNAME}reports/${FILE}* batch/recovery/${JOBNAME}/
            fi
        done

        if [[ "${RESUBMIT}" != "dryrun" ]]
        then
            cd ${JOBNAME}
            for FILE in `ls recover_*.jdl`
            do
                echo "Submitting recovery job for dataset ${FILE}"
                condor_submit ${FILE}
            done
        else
            echo "Finished resubmission dry-run"
        fi
    fi
fi

echo "Finished processing all jobs"
