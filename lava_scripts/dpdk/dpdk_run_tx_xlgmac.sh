#!/bin/sh
set -x

/root/lava_scripts/pktgen_port_clear.sh;

systemctl stop vpp.service
ps -aef | grep vpp

#tmux_window=$1
tmux_command1=$1
size_packets=$2
build_id=$3
bsp_id=$4
test_name=$5
test_suite=$6

#udhcpc
#mkdir -p /tmp/nfs
#df -h | grep 3.230
#if  [ $? == 0 ]
#then
#	mount 192.168.3.230:/lab-nfs /tmp/nfs/
#fi
#ls -l /usr/bin | grep -i sshpass
#if  [ $? == 1 ]
#then
#	cp /tmp/nfs/koti/lava_scripts/tmp/sshpass /usr/bin
#	chmod 777 /usr/bin/sshpass
#fi

ls -l /usr/bin | grep -i sshpass
if  [ $? == 1 ]
then
	cp /root/lava_scripts/dpdk/sshpass /usr/bin
	chmod 777 /usr/bin/sshpass
fi
rm -rf /root/tmux_0.txt
rm -rf /root/tmux_2.txt
cd /root/lava_scripts/dpdk
sleep 10
ifconfig 
ping 192.168.251.11 -c 2
sleep 20
ping 192.168.251.11 -c 2
./kill_pktgen.expect 192.168.251.11
sleep 10
ping 192.168.251.11 -c 2
ping 192.168.251.12 -c 2
pkill -9 tmux
#umount /dev/hugepages
sleep 3
tmux new -d -s dpdk 
sleep 3
pwd
tmux new-window -d -t dpdk:1
tmux new-window -d -t dpdk:2
sleep 3
#dpdk-hugepages.py -p 32M --setup 512M

tmux pipe-pane -o -t 0 'cat >> /root/tmux_0.txt'
#./tmux_session_commands.sh dpdk 0 "script /root/target_testpmd.txt"
sleep 3
./tmux_session_commands.sh dpdk 0  "clear;pwd"
./tmux_session_commands.sh dpdk 0  "clear"
sleep 3
#./tmux_session_commands.sh dpdk 0 "dpdk-hugepages.py -p 32M --setup 512M"
#sleep 3
#./tmux_session_commands.sh dpdk 0 "dpdk-testpmd -l 4-5 -n 4 -d /lib/librte_mempool_ring.so -d /lib/librte_net_raptor2.so --vdev=XGMAC0 -- -i --forward-mode=rxonly"
./tmux_session_commands.sh dpdk 0 "$1"
sleep 3
./tmux_session_commands.sh dpdk 0 "set txpkts $2"
sleep 3

tmux pipe-pane -o -t 2 'cat >> /root/tmux_2.txt'
#./tmux_session_commands.sh "dpdk" "2" "script /root/server_pktgen.txt"
sleep 3

./tmux_session_commands.sh "dpdk" "2" "clear;pwd"
./tmux_session_commands.sh "dpdk" "2" "clear"
sleep 3
#./tmux_session_commands.sh "dpdk" "2" "sshpass -p 'Password\$2021' ssh \-o StrictHostKeyChecking=accept-new equser@192.168.251.11" 
#sleep 3
#./tmux_session_commands.sh dpdk 2 "sudo bash /home/equser/start_pktgen.sh"
#sleep 3
#./tmux_session_commands.sh dpdk 2 "Password\$2021"
#sleep 15
#./tmux_session_commands.sh "dpdk" "2" "stop 0"
#sleep 3
#./tmux_session_commands.sh "dpdk" "2" "quit"
#sleep 15
./tmux_session_commands.sh "dpdk" "2" "sshpass -p 'Password\$2021' ssh \-o StrictHostKeyChecking=accept-new equser@192.168.251.11" 
sleep 3
./tmux_session_commands.sh dpdk 2 "sudo bash /home/equser/start_pktgen.sh"
sleep 3
./tmux_session_commands.sh dpdk 2 "Password\$2021"
sleep 15


./tmux_session_commands.sh dpdk 0  "start"
sleep 3
./tmux_session_commands.sh dpdk 0  "show port stats all"
sleep 3


./tmux_session_commands.sh "dpdk" "2" "set 0 src ip \"192.168.251.12/24\""
sleep 3
Target_IP=`ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p' | head -n 1`
./tmux_session_commands.sh "dpdk" "2" "set 0 dst ip $Target_IP "
sleep 3
Target_MAC=`ifconfig eth1 | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'`
./tmux_session_commands.sh "dpdk" "2" "set 0 dst mac $Target_MAC"
sleep 3
./tmux_session_commands.sh "dpdk" "2" "set 0 sport 2152"
sleep 3
./tmux_session_commands.sh "dpdk" "2" "set 0 dport 2152"
sleep 3
./tmux_session_commands.sh "dpdk" "2" "set 0 proto udp"
sleep 3
./tmux_session_commands.sh "dpdk" "2" "set 0 size $size_packets"
sleep 2
./tmux_session_commands.sh "dpdk" "2" "start 0"
sleep 3


./tmux_session_commands.sh dpdk 0  "set promisc 0 off"
sleep 2
./tmux_session_commands.sh dpdk 0  "show port stats all"
sleep 2
./tmux_session_commands.sh dpdk 0  "show port stats all"
sleep 2


echo "wait for 1 min"
sleep  60

./tmux_session_commands.sh dpdk 0  "show port stats all"
sleep 2
./tmux_session_commands.sh dpdk 0  "show port stats all"
sleep 2
./tmux_session_commands.sh dpdk 0  "show port stats all"
sleep 2
./tmux_session_commands.sh dpdk 0  "show port stats all"
sleep 2
./tmux_session_commands.sh dpdk 0  "show port stats all"
sleep 2
./tmux_session_commands.sh dpdk 0  "show port stats all"
sleep 2
./tmux_session_commands.sh dpdk 0  "show port stats all"
sleep 2
./tmux_session_commands.sh dpdk 0  "show port stats all"
sleep 2
./tmux_session_commands.sh dpdk 0  "show port stats all"
sleep 2
sleep 2



./tmux_session_commands.sh "dpdk" "2" "stop 0"
sleep 3
./tmux_session_commands.sh "dpdk" "2" "quit"
sleep 5
./tmux_session_commands.sh dpdk 0 "stop"
sleep 3
./tmux_session_commands.sh dpdk 0 "quit"
sleep 5
#./tmux_session_commands.sh dpdk 0 "umount /dev/hugepages"
sleep 3
./tmux_session_commands.sh dpdk 0 "sync"
sleep 3
#umount /dev/hugepages
sleep 5

sync
/root/lava_scripts/results_copy.sh  /root/tmux_0.txt /lava/edgeq/perfreports/$build_id/$bsp_id $test_name.txt  equser@192.168.251.10 "Password\$2021" $test_suite
sync

cat /root/tmux_0.txt
sleep 3
pkill -9 tmux
sleep 5
journalctl | grep monit;monit status pvtmon_B0;monit status pvtmon_b0
