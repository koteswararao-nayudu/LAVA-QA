#!/bin/bash

i=0

while [ $i -lt 10 ]
do
	ping  192.168.3.245 -c 2
	if [ $? == 0 ]
	then
		break;
	fi
	i=`expr $i + 1 `
done

echo "hai"
