#!/bin/sh
set -x

lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.106/RPC2/ jobs submit /home/equser/koti/lava-testcases/board43/edgeq-raptor2_linux_zephyr_boot.yaml
lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.106/RPC2/ jobs submit /home/equser/koti/lava-testcases/board43/edgeq-raptor2_linux_performance_tests.yaml
lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.106/RPC2/ jobs submit /home/equser/koti/lava-testcases/board43/edgeq-raptor2_linux_RT_zephyr_boot.yaml
lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.106/RPC2/ jobs submit /home/equser/koti/lava-testcases/board43/edgeq-raptor2_linux_RT_performance_tests.yaml
lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.106/RPC2/ jobs submit /home/equser/koti/lava-testcases/board43/edgeq-raptor2_linux_emmc.yaml
lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.106/RPC2/ jobs submit /home/equser/koti/lava-testcases/board43/edgeq-raptor2_linux_zephyr_uboot_reset.yaml
#lavacli --uri http://admin:es3bkjwhjo04oazzl0zqhl7zfr2n8wf1eg3zl246o9gspyyi2pczdsotmufgyc00yzkjuz6o0pl28mymjz7he980artaysb7hj4h4r5tia1u2f3y3ecf94ys1ye32ns0@192.168.3.106/RPC2/ jobs submit /home/equser/koti/lava-testcases/board43/edgeq-raptor2_linux_zephyr_pmic_off_on_stress.yaml

