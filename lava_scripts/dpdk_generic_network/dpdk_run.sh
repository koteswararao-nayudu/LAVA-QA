#!/bin/sh
#set -x

#tmux_window=$1
tmux_command1=$1
size_packets=$2

udhcpc
mkdir -p /tmp/nfs
df -h | grep 3.230
if  [ $? == 0 ]
then
	mount 192.168.3.230:/lab-nfs /tmp/nfs/
fi
ls -l /usr/bin | grep -i sshpass
if  [ $? == 1 ]
then
	cp /tmp/nfs/koti/lava_scripts/tmp/sshpass /usr/bin
	chmod 777 /usr/bin/sshpass
fi

#ls -l /usr/bin | grep -i sshpass
#if  [ $? == 1 ]
#then
#	cp /root/lava_scripts/dpdk/sshpass /usr/bin
#	chmod 777 /usr/bin/sshpass
#fi
rm -rf /root/tmux_0.txt
rm -rf /root/tmux_2.txt
cd /root/lava_scripts/dpdk
sleep 10
./kill_pktgen.expect 192.168.8.65
pkill -9 tmux
umount /dev/hugepages
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

tmux pipe-pane -o -t 2 'cat >> /root/tmux_2.txt'
#./tmux_session_commands.sh "dpdk" "2" "script /root/server_pktgen.txt"
sleep 3

./tmux_session_commands.sh "dpdk" "2" "clear;pwd"
./tmux_session_commands.sh "dpdk" "2" "clear"
sleep 3
./tmux_session_commands.sh "dpdk" "2" "sshpass -p 'Password\$2021' ssh \-o StrictHostKeyChecking=accept-new equser@192.168.8.65" 
sleep 3
./tmux_session_commands.sh dpdk 2 "sudo bash /home/equser/start_pktgen.sh"
sleep 3
./tmux_session_commands.sh dpdk 2 "Password\$2021"
sleep 3


./tmux_session_commands.sh dpdk 0  "start"
sleep 3
./tmux_session_commands.sh dpdk 0  "show port stats all"
sleep 3


./tmux_session_commands.sh "dpdk" "2" "set 0 src ip \"192.168.6.220/24\""
sleep 3
./tmux_session_commands.sh "dpdk" "2" "set 0 dst ip \"192.168.6.11\""
sleep 3
./tmux_session_commands.sh "dpdk" "2" "set 0 dst mac \"FC:9B:D4:00:04:1F\""
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
sleep 3

./tmux_session_commands.sh dpdk 0 "stop"
sleep 3
./tmux_session_commands.sh dpdk 0 "quit"
sleep 3
./tmux_session_commands.sh dpdk 0 "umount /dev/hugepages"
sleep 3
./tmux_session_commands.sh dpdk 0 "sync"
sleep 3
umount /dev/hugepages
sleep 3
cat /root/tmux_0.txt
