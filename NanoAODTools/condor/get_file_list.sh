#get the file list for a DAS entry

DATASET=$1
DOPROD=$2

if [[ "${DATASET}" == "" ]]; then
    echo "No dataset given"
fi

if [[ "${DOPROD}" == "" ]]; then
    das_client -query="file dataset=${DATASET} "
else
    das_client -query="file dataset=${DATASET} instance=prod/phys03"
fi
