#!/bin/sh

help(){
	echo ""
	echo "Usage: $0 -p <GUID>"
	echo -e "\t-p PARTUUID of the partition you want to map with the device name"
	exit 1 # Exit script after printing help
}

while getopts "p:" opt
do
	case "$opt" in
	       	p ) PARTUUID="$OPTARG" ;;
		? ) help ;;
	esac
done

# Print helpFunction in case parameters are empty
if [ -z "${PARTUUID}" ];then
	help
fi

export device=`grep -r "${PARTUUID}" partition.disk | cut -d":" -f1`

echo ${device}
