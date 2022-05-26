#!/bin/bash
# simple script to check multiple jobs
COM=status #status, resubmit or kill 

DIR=Nano_2021Sep26/
SAMPLES=( $DIR/* )
echo $SAMPLES
#samples=(
 # crab_BuToKEE_part2
 # crab_BuToKJpsi_ToEE_part2
#)

for sample in "${SAMPLES[@]}";
do 
 echo "processing" $sample
 #IN="$( find $sample/ -maxdepth 1 -type d )"
 IN="$( ls $sample/ )"
 echo ${#IN[@]}
 echo $IN
 if [[ ${#IN[@]} -eq 1 ]]; then
   crab ${COM} -d ${sample}/$IN
 else
   rab ${COM} -d ${sample}
 fi
done
