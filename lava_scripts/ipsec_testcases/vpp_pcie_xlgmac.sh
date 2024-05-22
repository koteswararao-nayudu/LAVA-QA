#!/bin/sh
set -x
#cp /root/ipsec_testcases/startup_pcie.conf /etc/vpp/startup.conf
#sed -i 's|XGMAC0|eth1-0|g' /etc/vpp/startup.conf
#sed -i 's|eth0-0|eth1-0|g' /etc/vpp/startup.conf

#sed -i 's|ACTIVE_ETH_INTERFACE=.*|ACTIVE_ETH_INTERFACE="eth1"|g' /etc/vpp/init.sh
#sed -i 's|eth0|eth1|g' /etc/vpp/init_ipsec.sh
##sed -i 's|XGMAC_VIRT0|XGMAC_VIRT1|g' /etc/vpp/startup.conf

#sed -i 's|export VPP_INTERFACES=.*|export VPP_INTERFACES=("eth1")|g' /etc/vpp_service.sh
#sed -i 's|VPP_IPSEC_STATIC_TUNNEL_ENABLE=.*|VPP_IPSEC_STATIC_TUNNEL_ENABLE="false"|g' /etc/vpp/init.sh
#sed -i 's|VPP_IPSEC_SERVER=.*|VPP_IPSEC_SERVER="127.0.0.0"|g' /etc/vpp/init.sh

sed -i 's|export VPP_INTERFACES=.*|export VPP_INTERFACES=("eth1")|g' /etc/vpp_service.sh
sed -i 's|VPP_IPSEC_ENABLE=.*|VPP_IPSEC_ENABLE="false"|g' /etc/vpp/init.sh
sed -i 's|VPP_IPSEC_SERVER=.*|VPP_IPSEC_SERVER="127.0.0.0"|g' /etc/vpp/init.sh
sed -i 's|VPP_PCIE_ENABLE=.*|VPP_PCIE_ENABLE="true"|g' /etc/vpp/init.sh

cat /etc/vpp/startup.conf

/root/lava_scripts/pktgen_port_clear.sh;

#tmux_window=$1
tmux_command1=$1
size_packets=$2
build_id=$3
bsp_id=$4
test_name=$5
test_suite=$6

mkdir -p /var/log/vpp
systemctl stop vpp.service
sleep 2
sync
#killall  vpp
#sed -i 's|#plugin raptor2_app_plugin.so|plugin raptor2_app_plugin.so|g' /etc/vpp/startup.conf

ls -l /usr/bin | grep -i sshpass
if  [ $? == 1 ]
then
	cp /root/lava_scripts/ipsec_testcases/sshpass /usr/bin
	chmod 777 /usr/bin/sshpass
fi
rm -rf /root/tmux_0_ipsec.txt
rm -rf /root/tmux_1_ipsec.txt
rm -rf /root/tmux_2_ipsec.txt

cd /root/lava_scripts/ipsec_testcases

sleep 10
ifconfig 
ping 192.168.251.11 -c 2
sleep 20
ping 192.168.251.11 -c 2
./kill_pktgen.expect 192.168.251.11
sleep 20
ping 192.168.251.11 -c 2
ping 192.168.251.12 -c 2

pkill -9 tmux
sleep 3
tmux new -d -s ipsec 
sleep 3
pwd
tmux new-window -d -t ipsec:1
tmux new-window -d -t ipsec:2
sleep 3

tmux pipe-pane -o -t 1 'cat >> /root/tmux_1_ipsec.txt'
sleep 3
./tmux_session_commands.sh ipsec 1  "clear;pwd"
./tmux_session_commands.sh ipsec 1  "clear"
sleep 3
#./tmux_session_commands.sh ipsec 1 "vpp -c /etc/vpp/startup.conf"
./tmux_session_commands.sh ipsec 1 "systemctl stop vpp.service"
sleep 10
./tmux_session_commands.sh ipsec 1 "ps -aef | grep -i vpp"
./tmux_session_commands.sh ipsec 1 "systemctl start vpp.service"
sleep 20
./tmux_session_commands.sh ipsec 1 "ps -aef | grep -i vpp"
./tmux_session_commands.sh ipsec 1 "vppctl"
sleep 20
./tmux_session_commands.sh ipsec 1 "show int"

cat /etc/vpp/init.txt

tmux pipe-pane -o -t 0 'cat >> /root/tmux_0_ipsec.txt'
sleep 3
./tmux_session_commands.sh ipsec 0  "clear;pwd"
./tmux_session_commands.sh ipsec 0  "clear"
sleep 3
./tmux_session_commands.sh ipsec 0 "$1"
sleep 5
./tmux_session_commands.sh ipsec 0  "start"
sleep 3
./tmux_session_commands.sh ipsec 0  "show port stats all"
sleep 3


ping 192.168.251.11 -c 2
ping 192.168.251.12 -c 2

tmux pipe-pane -o -t 2 'cat >> /root/tmux_2_ipsec.txt'
sleep 3

./tmux_session_commands.sh "ipsec" "2" "clear;pwd"
./tmux_session_commands.sh "ipsec" "2" "clear"
sleep 3
./tmux_session_commands.sh "ipsec" "2" "sshpass -p 'Password\$2021' ssh \-o StrictHostKeyChecking=accept-new equser@192.168.251.11" 
sleep 3
./tmux_session_commands.sh ipsec 2 "cd /home/equser/lava/ipsec_testcases"
./tmux_session_commands.sh ipsec 2 "sudo bash  ./pktgen_server_scripts/start_pktgen.sh"
sleep 3
./tmux_session_commands.sh ipsec 2 "Password\$2021"
sleep 30
./tmux_session_commands.sh "ipsec" "2" "set 0 src ip \"192.168.251.12/24\""
sleep 3
Target_IP=`ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p' | head -n 1`
./tmux_session_commands.sh "ipsec" "2" "set 0 dst ip $Target_IP "
sleep 3
Target_MAC=`ifconfig eth1 | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'`
./tmux_session_commands.sh "ipsec" "2" "set 0 dst mac $Target_MAC"
sleep 3
./tmux_session_commands.sh "ipsec" "2" "set 0 sport 2152"
sleep 3
./tmux_session_commands.sh "ipsec" "2" "set 0 dport 2152"
sleep 3
./tmux_session_commands.sh "ipsec" "2" "set 0 proto udp"
sleep 3
./tmux_session_commands.sh "ipsec" "2" "set 0 size $size_packets"
sleep 2
./tmux_session_commands.sh "ipsec" "2" "start 0"
sleep 3


./tmux_session_commands.sh ipsec 0  "set promisc 0 off"
sleep 2
./tmux_session_commands.sh ipsec 0  "show port stats all"
sleep 2
./tmux_session_commands.sh ipsec 0  "show port stats all"
sleep 2


echo "wait for 1 min"
sleep  60

./tmux_session_commands.sh ipsec 0  "show port stats all"
sleep 2
./tmux_session_commands.sh ipsec 0  "show port stats all"
sleep 2
./tmux_session_commands.sh ipsec 0  "show port stats all"
sleep 2
./tmux_session_commands.sh ipsec 0  "show port stats all"
sleep 2
./tmux_session_commands.sh ipsec 0  "show port stats all"
sleep 2
./tmux_session_commands.sh ipsec 0  "show port stats all"
sleep 2
./tmux_session_commands.sh ipsec 0  "show port stats all"
sleep 2
./tmux_session_commands.sh ipsec 0  "show port stats all"
sleep 2
./tmux_session_commands.sh ipsec 0  "show port stats all"
sleep 2
./tmux_session_commands.sh ipsec 1 "show int"
sleep 2
./tmux_session_commands.sh ipsec 1 "show int"
sleep 2
./tmux_session_commands.sh ipsec 1 "show errors"



./tmux_session_commands.sh "ipsec" "2" "stop 0"
sleep 10
./tmux_session_commands.sh "ipsec" "2" "quit"
sleep 10

./tmux_session_commands.sh ipsec 1 "quit"
sleep 10

./tmux_session_commands.sh ipsec 0 "stop"
sleep 10
./tmux_session_commands.sh ipsec 0 "quit"
sleep 10
#./tmux_session_commands.sh ipsec 0 "umount /dev/hugepages"
sleep 3
./tmux_session_commands.sh ipsec 0 "sync"
sleep 3
#umount /dev/hugepages
sleep 3

sync
/root/lava_scripts/results_copy.sh  /root/tmux_0_ipsec.txt /lava/edgeq/perfreports/$build_id/$bsp_id $test_name.txt  equser@192.168.251.10 "Password\$2021" $test_suite
sync


cat /root/tmux_1_ipsec.txt
sleep 2
cat /root/tmux_0_ipsec.txt
#cat /root/tmux_2_ipsec.txt
sleep 3
pkill -9 tmux
sleep 5
journalctl | grep monit;monit status pvtmon_B0;monit status pvtmon_b0
