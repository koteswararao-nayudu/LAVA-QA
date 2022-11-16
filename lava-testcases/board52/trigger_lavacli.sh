#!/usr/bin/sh 
set -x

build_id_name=$1
cd /home/equser/koti/lava-testcases/board52
rm -rf /home/equser/koti/lava-testcases/board52/tmp
mkdir /home/equser/koti/lava-testcases/board52/tmp
cp /home/equser/koti/lava-testcases/board52/evb-v1-all-functional-tests-generic.yaml /home/equser/koti/lava-testcases/board52/tmp/
cp /home/equser/koti/lava-testcases/board52/evb-v1-edgeq-raptor2_eMMCboot-generic.yaml /home/equser/koti/lava-testcases/board52/tmp/
cd /home/equser/koti/lava-testcases/board52/tmp
echo $build_id_name
grep -rl "BUILD_ID" ./ | xargs sed -i "s/BUILD_ID/${build_id_name}/g"
sync
sleep 5
password="Password\$2021"
#ssh equser@192.168.3.152 "echo Password\$2021 | sudo pkill -9 minicom"
#echo $password | ssh -tt equser@192.168.3.152 "sudo pkill -9 minicom"
#echo $password | ssh -tt equser@192.168.3.152 "sudo pkill -9 openocd*"
echo $password | ssh -tt equser@192.168.3.113 "sudo pkill -9 minicom"
echo $password | ssh -tt equser@192.168.3.113 "sudo pkill -9 openocd*"
#lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.106/RPC2/ devices update edgeq-raptor2-52 --health GOOD
lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.106/RPC2/ devices update edgeq-raptor2-13 --health GOOD

lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.106/RPC2/ jobs submit /home/equser/koti/lava-testcases/board52/tmp/evb-v1-all-functional-tests-generic.yaml
lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.106/RPC2/ jobs submit /home/equser/koti/lava-testcases/board52/tmp/evb-v1-edgeq-raptor2_eMMCboot-generic.yaml
lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.106/RPC2/ jobs submit /home/equser/koti/lava-testcases/board52/tmp/evb-v1-edgeq-raptor2_eMMCboot-generic.yaml
lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.106/RPC2/ jobs submit /home/equser/koti/lava-testcases/board52/tmp/evb-v1-edgeq-raptor2_eMMCboot-generic.yaml
lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.106/RPC2/ jobs submit /home/equser/koti/lava-testcases/board52/tmp/evb-v1-edgeq-raptor2_eMMCboot-generic.yaml
