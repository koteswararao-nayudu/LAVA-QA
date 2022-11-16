#!/usr/bin/sh

set -x

wget_url=$1
build_id=$2
product_line=$3

build_no=`echo $build_id | awk -F _ '{print \$4}'`
echo $build_no
build_id_tar_gz="$build_id.tar.gz"
echo $build_id_tar_gz


cd /lab-nfs/koti/latestimages/

#wget -r -np -l 1 --auth-no-challenge --http-user=platform_dev --http-password=platform@123 $wget_url
wget -q -T200 -r -np -l 1 --auth-no-challenge --http-user=platform_dev --http-password=platform@123 $wget_url

if [ $? -eq 0 ]
then
        echo "wget success"
else
        echo "wget fail"
        exit 1
fi

mv 192.168.*.*\:8080/job/PLATFORM-$product_line/$build_no/artifact/* ./
cp /lab-nfs/koti/latestimages/$build_id_tar_gz /srv/tftp/koti
rm -rf 192.168.*.*
sync
tar -xzvf $build_id_tar_gz
cd /srv/tftp/koti
tar -xzvf $build_id_tar_gz
sleep 2

ssh equser@192.168.3.198 "/home/equser/koti/lava-testcases/board26/trigger_lavacli.sh $build_id"
