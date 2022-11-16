#!/bin/sh
set -x

build_id=$1

cd /srv/tftp/koti/master_e2eramdisk
rm -rf *.img

#wget -r -np -l 1 --auth-no-challenge --http-user=software_dev --http-password=dev@1234 http://152.67.16.19:8080/job/MAINLINE%20E2E%20BUILD/$build_id/artifact/uRamdisk.img
wget -q -T200 -r -np -l 1 --auth-no-challenge --http-user=software_dev --http-password=dev@1234 http://152.67.16.19:8080/job/MAINLINE%20E2E%20BUILD/$build_id/artifact/uRamdisk.img

if [ $? -eq 0 ]
then
        echo "wget success"
else
        echo "wget fail"
        exit 1
fi

mv 152.67.*.*\:8080/job/MAINLINE\ E2E\ BUILD/$build_id/artifact/* ./
rm -rf 152.67.*.*
sync
sleep 2

/usr/bin/sh /srv/tftp/koti/master_e2eramdisk/trigger_master_uramdisk.sh $build_id
