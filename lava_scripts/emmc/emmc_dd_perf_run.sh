#!/bin/sh

rm -rf ~/emmc_dd_performance_values_out*
build_id=$1
bsp_id=$2
set -x

cd ~/
sleep 2
counter=0
while [ $counter -lt 1 ];
do
  ls -l /coredump
  sleep 10
  df -h
  rm -f /coredump/tmpfile*
  sync
  ls /coredump
  echo "Mounted"

  time dd if=/dev/zero of=/coredump/tmpfile0 conv=fsync bs=1M count=1  >> emmc_dd_performance_values_output_1M_count1.txt 2>&1
  echo $?

  #./emmc_test2.sh /dev/zero /coredump/tmpfile0 1 1000
  sync
  echo "1MB Transfer done"  >> emmc_dd_performance_values_output_1M_count1.txt 2>&1

  time dd if=/dev/zero of=/coredump/tmpfile1 conv=fsync bs=1M count=10  >> emmc_dd_performance_values_output_1M_count10.txt 2>&1
  #./emmc_test2.sh /dev/zero /coredump/tmpfile1 10 1000
  sync
  echo "10MB Transfer done"  >> emmc_dd_performance_values_output_1M_count10.txt 2>&1

  time dd if=/dev/zero of=/coredump/tmpfile2 conv=fsync bs=1M count=100  >> emmc_dd_performance_values_output_1M_count100.txt 2>&1
  #./emmc_test2.sh /dev/zero /coredump/tmpfile2 100 1000
  sync
  echo "100MB Transfer done"  >> emmc_dd_performance_values_output_1M_count100.txt 2>&1

  time dd if=/dev/zero of=/coredump/tmpfile3 conv=fsync bs=1M count=1000  >> emmc_dd_performance_values_output_1M_count1000.txt 2>&1
  #./emmc_test2.sh /dev/zero /coredump/tmpfile3 1000 1000
  sync
  echo "1GB Transfer done"  >> emmc_dd_performance_values_output_1M_count1000.txt 2>&1

  ls -ltrh /coredump
  umount /coredump
  echo "Unmounted"
  #((counter++))
  counter=`expr $counter + 1 `
  #sleep 180  # Delay for 3 minutes
done

/root/lava_scripts/results_copy.sh ~/emmc_dd_performance_values_output_1M_count1.txt  /lava/edgeq/perfreports/$build_id/$bsp_id emmc_dd_performance_values_output_1M_count1.txt  equser@192.168.251.10 "Password\$2021" emmc
/root/lava_scripts/results_copy.sh ~/emmc_dd_performance_values_output_1M_count10.txt  /lava/edgeq/perfreports/$build_id/$bsp_id emmc_dd_performance_values_output_1M_count10.txt  equser@192.168.251.10 "Password\$2021" emmc
/root/lava_scripts/results_copy.sh ~/emmc_dd_performance_values_output_1M_count100.txt  /lava/edgeq/perfreports/$build_id/$bsp_id emmc_dd_performance_values_output_1M_count100.txt  equser@192.168.251.10 "Password\$2021" emmc
/root/lava_scripts/results_copy.sh ~/emmc_dd_performance_values_output_1M_count1000.txt  /lava/edgeq/perfreports/$build_id/$bsp_id emmc_dd_performance_values_output_1M_count1000.txt  equser@192.168.251.10 "Password\$2021" emmc
