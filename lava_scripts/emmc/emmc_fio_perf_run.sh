#!/bin/sh
#set -x

build_id=$1
bsp_id=$2

cp /root/lava_scripts/bin/jq   /bin
chmod 777 /bin/jq
cd /root/lava_scripts/emmc
chmod 777 fio_performance_values.sh
./fio_performance_values.sh > emmc_fio_performance_values_output.txt 2>&1

/root/lava_scripts/results_copy.sh /root/lava_scripts/emmc/emmc_fio_performance_values_output.txt  /lava/edgeq/perfreports/$build_id/$bsp_id emmc_fio_performance_values_output.txt  equser@192.168.251.10 "Password\$2021" emmc

#/root/lava_scripts/results_copy.sh /root/lava_scripts/emmc/emmc_fio_performance_values_output.txt  /lava/edgeq/perfreports/RAPTOR2-GNB-PLFM-B0-raptor2_dev_B0_230224_228/PRODUCT-REL-HAWK-GNB-PLFM-B0-raptor2_dev_B0_230224_228 emmc_fio_performance_values_output.txt  equser@192.168.251.10 "Password\$2021" emmc
