#!/bin/sh
set -x

#tmux_window=$1
tmux_command1=$1
size_packets=$2
build_id=$3
bsp_id=$4
test_name=$5
test_suite=$6


ls -l /usr/bin | grep -i sshpass
if  [ $? == 1 ]
then
	cp /root/lava_scripts/dpdk/sshpass /usr/bin
	chmod 777 /usr/bin/sshpass
fi
rm -rf /root/pktgenclear_0.txt
rm -rf /root/pktgenclear_2.txt
cd /root/lava_scripts/dpdk
sleep 10
ifconfig 
ping 192.168.251.11 -c 2
ping 192.168.251.12 -c 2
./kill_pktgen.expect 192.168.251.11
sleep 10
ping 192.168.251.11 -c 2
ping 192.168.251.12 -c 2
pkill -9 tmux
sleep 3
tmux new -d -s pktgenclear
sleep 3
pwd
tmux new-window -d -t pktgenclear:1
tmux new-window -d -t pktgenclear:2
sleep 3



./tmux_session_commands.sh "pktgenclear" "2" "clear;pwd"
./tmux_session_commands.sh "pktgenclear" "2" "clear"
sleep 3
./tmux_session_commands.sh "pktgenclear" "2" "sshpass -p 'Password\$2021' ssh \-o StrictHostKeyChecking=accept-new equser@192.168.251.11" 
sleep 3
./tmux_session_commands.sh pktgenclear 2 "sudo bash /home/equser/start_pktgen.sh"
sleep 3
./tmux_session_commands.sh pktgenclear 2 "Password\$2021"
sleep 15
./tmux_session_commands.sh "pktgenclear" "2" "stop 0"
sleep 3
./tmux_session_commands.sh "pktgenclear" "2" "quit"
sleep 20


pkill -9 tmux
sleep 5
