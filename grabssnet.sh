#!/bin/bash
#PROCESS=14

echo 'GRABSSNET'

CTR=0
while read p; do

    echo 'Counter :'
    echo $CTR
    echo 'File : '
    echo $p

    if [ $CTR -eq $PROCESS ]
    then
	ifdh cp $p ssnetout.root
	break
    fi

    CTR=`expr $CTR + 1`

done <ssnet.txt 