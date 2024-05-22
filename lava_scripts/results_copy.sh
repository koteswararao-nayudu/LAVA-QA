#!/bin/sh
set -x

copy_file=$1
copy_destination_path=$2
destination_file=$3
hostname=$4
password="$5"
test_suite=$6

sshpass -v -p "$password" ssh \-o StrictHostKeyChecking=accept-new $hostname "set -x ; mkdir -p $copy_destination_path/$test_suite; chmod 777 -R $copy_destination_path; chmod 777 -R $copy_destination_path/$test_suite "

sshpass -v -p "$password" scp \-o StrictHostKeyChecking=no \-o UserKnownHostsFile=/dev/null -r $copy_file $hostname:$copy_destination_path/$test_suite/$destination_file

sshpass -v -p "$password" ssh \-o StrictHostKeyChecking=accept-new $hostname "chmod 777 -R $copy_destination_path/$test_suite"
