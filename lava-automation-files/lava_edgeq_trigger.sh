#!/usr/bin/sh

set -x

build_id=$1
echo $build_id
build_no=`echo $build_id | awk -F _ '{print \$4}'`
echo $build_no
build_id_tar_gz="$build_id.tar.gz"
echo $build_id_tar_gz

cd /lab-nfs/koti/latestimages
#wget -q -T200 -r -np -l 1 --auth-no-challenge --http-user=platform_dev --http-password=platform@123 http://192.168.1.240:8080/job/PLATFORM-CI/$build_no/artifact/$build_id_tar_gz
touch 2.txt
/usr/bin/sh /lab-nfs/koti/latestimages/trigger.sh http://192.168.1.240:8080/job/PLATFORM-CI/$build_no/artifact/$build_id_tar_gz $build_id CI
