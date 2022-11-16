#!/usr/bin/sh
set -x

build_id=$1
#ssh equser@192.168.3.198 "/home/equser/koti/lava-testcases/e2e_master/board43/trigger.sh  $build_id"
#ssh equser@192.168.3.198 "/home/equser/koti/lava-testcases/e2e_master/board25/trigger.sh  $build_id"
#ssh equser@192.168.3.198 "/home/equser/koti/lava-testcases/e2e_master/board41/trigger.sh  $build_id"
ssh equser@192.168.3.198 "/home/equser/koti/lava-testcases/e2e_master/board46/trigger.sh  $build_id"

