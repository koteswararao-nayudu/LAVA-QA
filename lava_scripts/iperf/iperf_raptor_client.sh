#!/bin/sh
set -x



#tmux_window=$1
tmux_command1=$1
size_packets=$2
build_id=$3
bsp_id=$4
test_name=$5
test_suite=$6
ipversion=$7


ls -l /usr/bin | grep -i sshpass
if  [ $? == 1 ]
then
	cp /root/lava_scripts/iperf/sshpass /usr/bin
	chmod 777 /usr/bin/sshpass
fi

rm -rf /root/tmux_0_iperf.txt
rm -rf /root/tmux_1_iperf.txt
rm -rf /root/tmux_2_iperf.txt

cd /root/lava_scripts/iperf

sleep 20
ping 192.168.251.11 -c 2
ping 192.168.251.12 -c 2

pkill -9 tmux
sleep 3
tmux new -d -s iperf
sleep 3
pwd
tmux new-window -d -t iperf:1
tmux new-window -d -t iperf:2
sleep 3

tmux pipe-pane -o -t 1 'cat >> /root/tmux_1_iperf.txt'
sleep 3
tmux pipe-pane -o -t 0 'cat >> /root/tmux_0_iperf.txt'
sleep 3
tmux pipe-pane -o -t 2 'cat >> /root/tmux_2_iperf.txt'
sleep 3


./tmux_session_commands.sh "iperf" "0" "clear;pwd"
./tmux_session_commands.sh "iperf" "0" "clear"
sleep 3
./tmux_session_commands.sh "iperf" "0" "sshpass -p 'Password\$2021' ssh \-o StrictHostKeyChecking=accept-new equser@192.168.251.11"
sleep 3
./tmux_session_commands.sh iperf 0 "ifconfig -a"
./tmux_session_commands.sh iperf 0 "pkill -9 iperf3"
./tmux_session_commands.sh iperf 0 "iperf3 -s &"
./tmux_session_commands.sh iperf 0 "$tmux_command1"
sleep 2


./tmux_session_commands.sh "iperf" "1" ""
./tmux_session_commands.sh "iperf" "1" "pkill -9 iperf3"
./tmux_session_commands.sh "iperf" "1" "$tmux_command1"
sleep 40
sync
/root/lava_scripts/results_copy.sh  /root/tmux_1_iperf.txt /lava/edgeq/perfreports/$build_id/$bsp_id $test_name.txt  equser@192.168.9.160 "Password\$2021" $test_suite
sync


cat /root/tmux_1_iperf.txt
sleep 2
#cat /root/tmux_0_iperf.txt
#cat /root/tmux_2_iperf.txt
./tmux_session_commands.sh iperf 0 "pkill -9 iperf3"
./tmux_session_commands.sh iperf 1 "pkill -9 iperf3"
sleep 3
pkill -9 tmux
sleep 5
journalctl | grep monit;monit status pvtmon_B0;monit status pvtmon_b0
