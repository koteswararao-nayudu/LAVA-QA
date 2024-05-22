#!/bin/sh

rm -rf ~/usb_dd_performance_values_out*
build_id=$1
bsp_id=$2
set -x

cd ~/
umount /dev/sd*
echo "y" | mkfs.ext4 /dev/sda1
sleep 2
counter=0
while [ $counter -lt 1 ];
do
  echo "Mounting"
  mount /dev/sda1 /mnt
  sleep 10
  df -h
  rm -f /mnt/tmpfile*
  sync
  ls /mnt
  echo "Mounted"

  time dd if=/dev/zero of=/mnt/tmpfile0 conv=fsync bs=1M count=1  >> usb_dd_performance_values_output_1M_count1.txt 2>&1
  echo $?

  #./usb_test2.sh /dev/zero /mnt/tmpfile0 1 1000
  sync
  echo "1MB Transfer done"  >> usb_dd_performance_values_output_1M_count1.txt 2>&1

  time dd if=/dev/zero of=/mnt/tmpfile1 conv=fsync bs=1M count=10  >> usb_dd_performance_values_output_1M_count10.txt 2>&1
  #./usb_test2.sh /dev/zero /mnt/tmpfile1 10 1000
  sync
  echo "10MB Transfer done"  >> usb_dd_performance_values_output_1M_count10.txt 2>&1

  time dd if=/dev/zero of=/mnt/tmpfile2 conv=fsync bs=1M count=100  >> usb_dd_performance_values_output_1M_count100.txt 2>&1
  #./usb_test2.sh /dev/zero /mnt/tmpfile2 100 1000
  sync
  echo "100MB Transfer done"  >> usb_dd_performance_values_output_1M_count100.txt 2>&1

  time dd if=/dev/zero of=/mnt/tmpfile3 conv=fsync bs=1M count=1000  >> usb_dd_performance_values_output_1M_count1000.txt 2>&1
  #./usb_test2.sh /dev/zero /mnt/tmpfile3 1000 1000
  sync
  echo "1GB Transfer done"  >> usb_dd_performance_values_output_1M_count1000.txt 2>&1

  ls -ltrh /mnt
  umount /mnt
  echo "Unmounted"
  #((counter++))
  counter=`expr $counter + 1 `
  #sleep 180  # Delay for 3 minutes
done

/root/lava_scripts/results_copy.sh ~/usb_dd_performance_values_output_1M_count1.txt  /lava/edgeq/perfreports/$build_id/$bsp_id usb_dd_performance_values_output_1M_count1.txt  equser@192.168.251.10 "Password\$2021" usb
/root/lava_scripts/results_copy.sh ~/usb_dd_performance_values_output_1M_count10.txt  /lava/edgeq/perfreports/$build_id/$bsp_id usb_dd_performance_values_output_1M_count10.txt  equser@192.168.251.10 "Password\$2021" usb
/root/lava_scripts/results_copy.sh ~/usb_dd_performance_values_output_1M_count100.txt  /lava/edgeq/perfreports/$build_id/$bsp_id usb_dd_performance_values_output_1M_count100.txt  equser@192.168.251.10 "Password\$2021" usb
/root/lava_scripts/results_copy.sh ~/usb_dd_performance_values_output_1M_count1000.txt  /lava/edgeq/perfreports/$build_id/$bsp_id usb_dd_performance_values_output_1M_count1000.txt  equser@192.168.251.10 "Password\$2021" usb
