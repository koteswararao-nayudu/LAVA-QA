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
	cp /root/lava_scripts/l2fwd/sshpass /usr/bin
	chmod 777 /usr/bin/sshpass
fi

rm -rf /root/tmux_0_l2fwd.txt
rm -rf /root/tmux_1_l2fwd.txt
rm -rf /root/tmux_2_l2fwd.txt

cd /root/lava_scripts/l2fwd

sleep 20
ping 192.168.6.221 -c 2
ping 192.168.6.220 -c 2

pkill -9 tmux
sleep 3
tmux new -d -s l2fwd
sleep 3
pwd
tmux new-window -d -t l2fwd:1
tmux new-window -d -t l2fwd:2
sleep 3

tmux pipe-pane -o -t 1 'cat >> /root/tmux_1_l2fwd.txt'
sleep 3
tmux pipe-pane -o -t 0 'cat >> /root/tmux_0_l2fwd.txt'
sleep 3
tmux pipe-pane -o -t 2 'cat >> /root/tmux_2_l2fwd.txt'
sleep 3


./tmux_session_commands.sh "l2fwd" "0" "clear;pwd"
./tmux_session_commands.sh "l2fwd" "0" "clear"
sleep 3
./tmux_session_commands.sh "l2fwd" "0" "sshpass -p 'Password\$2021' ssh \-o StrictHostKeyChecking=accept-new equser@192.168.8.226"
sleep 3
./tmux_session_commands.sh l2fwd 0 "ifconfig -a"
./tmux_session_commands.sh l2fwd 0 "$tmux_command1"
sleep 30

#if [ "$ipversion" = "IPV6" ]
#then
#        ## you can get the ipv6 addres for BLR  pktgen using "sudo dhclient -6 -i enp10s0f1"
#        ./tmux_session_commands.sh ipsec 1 "ip route add ::/0 via fdc1:42c4:3237::a0a3:e697 Ethernet0"
#        sleep 5
#        ./tmux_session_commands.sh ipsec 1 "set ip neighbor Ethernet0 fdc1:42c4:3237::a0a3:e697 b4:96:91:b6:2a:97 static"
#
#        #PKTGEN_IPV6=`ifconfig enp10s0f1 | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}|([0-9a-fA-F]{0,4}:){1,7}[0-9a-fA-F]{0,4}' | sed -n '6 p'`
#        #PKTGEN_IP="fdc1:42c4:3237:0:b696:91ff:feb6:2a97"
#        PKTGEN_IP="fdc1:42c4:3237::a0a3:e697"
#        #Target_IP=`ifconfig eth0 | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}|([0-9a-fA-F]{0,4}:){1,7}[0-9a-fA-F]{0,4}' | sed -n '13 p'`
#        #Target_IP=`ifconfig eth0 | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}|([0-9a-fA-F]{0,4}:){1,7}[0-9a-fA-F]{0,4}' | sed -n '7 p'`
#        Target_IP=`ifconfig eth0 | grep "Scope:Global" | grep -Eo '[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}|([0-9a-fA-F]{0,4}:){1,7}[0-9a-fA-F]{0,4}' | sed -n '2 p'`
#	echo "Target_IP=$Target_IP"
#        ./tmux_session_commands.sh "ipsec" "2" "set 0 src ip \"$PKTGEN_IP/64\""
#        sleep 3
#        ./tmux_session_commands.sh "ipsec" "2" "set 0 dst ip $Target_IP "
#fi
#
#if [ "$ipversion" = "IPV4" ]
#then
#        ./tmux_session_commands.sh ipsec 1 "set ip neighbor Ethernet0 192.168.251.12 b4:96:91:b6:2a:97 static"
#
#        #PKTGEN_IPV4=`ifconfig enp10s0f1 | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}|([0-9a-fA-F]{0,4}:){1,7}[0-9a-fA-F]{0,4}' | sed -n '2 p'`
#        PKTGEN_IP="192.168.251.12"
#        Target_IP=`ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p' | head -n 1`
#        ./tmux_session_commands.sh "ipsec" "2" "set 0 src ip \"$PKTGEN_IP/24\""
#        sleep 3
#        ./tmux_session_commands.sh "ipsec" "2" "set 0 dst ip $Target_IP "
#fi


sync
/root/lava_scripts/results_copy.sh  /root/tmux_0_l2fwd.txt /lava/edgeq/perfreports/$build_id/$bsp_id $test_name.txt  equser@192.168.9.160 "Password\$2021" $test_suite
sync


cat /root/tmux_1_l2fwd.txt
sleep 2
cat /root/tmux_0_l2fwd.txt
cat /root/tmux_2_l2fwd.txt
sleep 3
pkill -9 tmux
sleep 5
journalctl | grep monit;monit status pvtmon_B0;monit status pvtmon_b0
