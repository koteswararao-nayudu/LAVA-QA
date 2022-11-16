#!/usr/bin/sh

build_id=$1
rm -rf /home/equser/koti/lava-testcases/e2e/board43/tmp
mkdir -p  /home/equser/koti/lava-testcases/e2e/board43/tmp
cp /home/equser/koti/lava-testcases/e2e/board43/edgeq-raptor2_e2e_gnb_cellup_board43-generic.yaml  /home/equser/koti/lava-testcases/e2e/board43/tmp
cd /home/equser/koti/lava-testcases/e2e/board43/tmp
echo $build_id
grep -rl "BUILD_ID" ./ | xargs sed -i "s/BUILD_ID/${build_id}/g"
sync
sleep 5
ssh equser@192.168.3.143 "echo Password\$2021 | sudo pkill -9 minicom"
 lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.106/RPC2/ devices update edgeq-raptor2-43 --health GOOD
lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.106/RPC2/ jobs submit /home/equser/koti/lava-testcases/e2e/board43/tmp/edgeq-raptor2_e2e_gnb_cellup_board43-generic.yaml

