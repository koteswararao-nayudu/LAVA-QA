#!/usr/bin/sh
set -x

build_id=$1
rm -rf /home/equser/koti/lava-testcases/e2e/board41/tmp
mkdir -p  /home/equser/koti/lava-testcases/e2e/board41/tmp
cp /home/equser/koti/lava-testcases/e2e/board41/cell_attach_test/edgeq-raptor2_e2e_gnb_cellup_board41-generic1_RC2.yaml /home/equser/koti/lava-testcases/e2e/board41/tmp
cp /home/equser/koti/lava-testcases/e2e/board41/cell_attach_test/edgeq-raptor2_e2e_gnb_cellup_board41-generic1_RC3.yaml /home/equser/koti/lava-testcases/e2e/board41/tmp
cp /home/equser/koti/lava-testcases/e2e/board41/cell_attach_test/edgeq-raptor2_e2e_gnb_cellup_board41-generic1_RC5.yaml /home/equser/koti/lava-testcases/e2e/board41/tmp
cp /home/equser/koti/lava-testcases/e2e/board41/cell_attach_test/edgeq-raptor2_e2e_gnb_cellup_board41-generic1_RC5.1.yaml /home/equser/koti/lava-testcases/e2e/board41/tmp
cp /home/equser/koti/lava-testcases/e2e/board41/cell_attach_test/edgeq-raptor2_e2e_gnb_cellup_board41-generic1_RC5.1_tmp.yaml /home/equser/koti/lava-testcases/e2e/board41/tmp
#cp /home/equser/koti/lava-testcases/e2e/board41/cell_attach_test/edgeq-raptor2_e2e_gnb_cellup_board41-generic.yaml /home/equser/koti/lava-testcases/e2e/board41/tmp
#cp /home/equser/koti/lava-testcases/e2e/board41/edgeq-raptor2_e2e_gnb_cellup_board41-generic.yaml  /home/equser/koti/lava-testcases/e2e/board41/tmp
cd /home/equser/koti/lava-testcases/e2e/board41/tmp
echo $build_id
grep -rl "BUILD_ID" ./ | xargs sed -i "s/BUILD_ID/${build_id}/g"
sync
sleep 5
password="Password\$2021"
#ssh equser@192.168.3.143 'echo $password | sudo pkill -9 minicom'
#ssh equser@192.168.3.174 'echo $password | sudo -S pkill -9 minicom'
#ssh equser@192.168.3.174 'sudo -S pkill -9 minicom << echo $password'
#echo $password | ssh -tt equser@192.168.3.174 "sudo pkill -9 minicom"
#echo $password | ssh -tt equser@192.168.3.174 "sudo pkill -9 openocd*"
echo $password | ssh -tt equser@192.168.3.146 "sudo pkill -9 minicom"
echo $password | ssh -tt equser@192.168.3.146 "sudo pkill -9 openocd*"
#ssh equser@192.168.3.174 'sudo -S pkill -9 minicom << echo $password'
#lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.198/RPC2/ devices update edgeq-raptor2-41 --health GOOD
lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.198/RPC2/ devices update edgeq-raptor2-46 --health GOOD
#lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.198/RPC2/ jobs submit /home/equser/koti/lava-testcases/e2e/board41/tmp/edgeq-raptor2_e2e_gnb_cellup_board41-generic.yaml
#lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.198/RPC2/ jobs submit /home/equser/koti/lava-testcases/e2e/board41/tmp/edgeq-raptor2_e2e_gnb_cellup_board41-generic1.yaml

