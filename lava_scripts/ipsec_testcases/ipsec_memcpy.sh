#!/bin/sh
set -x

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
#killall vpp
sleep 2
systemctl stop vpp
ps -aef | grep vpp
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

ifconfig 
ping 192.168.251.11 -c 2
sleep 10
ping 192.168.251.11 -c 2
./kill_pktgen.expect 192.168.251.11
sleep 10
ping 192.168.251.11 -c 2
ping 192.168.251.12 -c 2


#cp /root/ipsec_testcases/startup_pcie_ipsec.conf /etc/vpp
#cp /root/ipsec_testcases/startup_memcpy_ipsec.conf /etc/vpp/startup.conf
#cp /root/ipsec_testcases/ipsecScript.sh /etc/vpp
#cp /root/ipsec_testcases/load_crss_fw.sh /etc/vpp
#sed -i 's|XGMAC0|eth0-0|g' /etc/vpp/startup.conf
#sed -i 's|XGMAC1|eth1-0|g' /etc/vpp/startup.conf
#sed -i 's|ACTIVE_ETH_INTERFACE=.*|ACTIVE_ETH_INTERFACE="eth0"|g' /etc/vpp/init.sh
#cat /etc/vpp/startup.conf
cd /etc/vpp

#chmod +x init_ipsec.sh
#./init_ipsec.sh 192.168.251.12
#sed -i 's|export VPP_INTERFACES=.*|export VPP_INTERFACES=("eth0")|g' /etc/vpp_service.sh
#sed -i 's|VPP_IPSEC_STATIC_TUNNEL_ENABLE=.*|VPP_IPSEC_STATIC_TUNNEL_ENABLE="true"|g' /etc/vpp/init.sh
#sed -i 's|VPP_IPSEC_SERVER=.*|VPP_IPSEC_SERVER="192.168.251.12"|g' /etc/vpp/init.sh

sed -i 's|export VPP_INTERFACES=.*|export VPP_INTERFACES=("eth0")|g' /etc/vpp_service.sh
sed -i 's|VPP_IPSEC_ENABLE=.*|VPP_IPSEC_ENABLE="true"|g' /etc/vpp/init.sh
sed -i 's|VPP_IPSEC_SERVER=.*|VPP_IPSEC_SERVER="192.168.251.12"|g' /etc/vpp/init.sh
sed -i 's|VPP_IPSEC_BYPASS=.*|VPP_IPSEC_BYPASS="192.168.251.11"|g' /etc/vpp/init.sh
sed -i 's|VPP_PCIE_ENABLE=.*|VPP_PCIE_ENABLE="false"|g' /etc/vpp/init.sh
cat /etc/vpp_service.sh

cat /etc/vpp/init.sh

cd /root/lava_scripts/ipsec_testcases
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
#./tmux_session_commands.sh ipsec 1 "vppctl"
#sleep 20
./tmux_session_commands.sh ipsec 1 "export VPP_IPSEC_SERVER="192.168.251.12""
./tmux_session_commands.sh ipsec 1 "export VPP_IPSEC_BYPASS="192.168.251.11""
./tmux_session_commands.sh ipsec 1 "export UPF_VPP_INTERFACE="Ethernet0""
./tmux_session_commands.sh ipsec 1 "export UPF_LINUX_INTERFACE="eth0""
./tmux_session_commands.sh ipsec 1 "line=\"\$(ip -f inet addr show \$UPF_LINUX_INTERFACE | grep -i \"scope global\" | sed 's/    //g')\""
sleep 1
./tmux_session_commands.sh ipsec 1 "ip4_addr_full=\"\$(echo \$line | cut -d ' ' -f 2)\""
./tmux_session_commands.sh ipsec 1 "ip4_addr=\"\${ip4_addr_full%/*}\""
./tmux_session_commands.sh ipsec 1 "vppctl ipsec sa add 5 spi 5 esp crypto-alg aes-gcm-128 crypto-key c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3 salt 0xc3c3c3c3 tunnel src \$ip4_addr dst \$VPP_IPSEC_SERVER"
sleep 1
#./tmux_session_commands.sh ipsec 1 "sleep 2"
./tmux_session_commands.sh ipsec 1 "vppctl ipsec sa add 6 spi 256 crypto-alg aes-gcm-128 crypto-key c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3c3 salt 0xc3c3c3c3 tunnel src \$VPP_IPSEC_SERVER dst \$ip4_addr"
sleep 1
./tmux_session_commands.sh ipsec 1 "vppctl set interface ipsec spd Ethernet0 1"
sleep 1
#./tmux_session_commands.sh ipsec 1 "sleep 2"
./tmux_session_commands.sh ipsec 1 "vppctl ipsec spd add 1"
sleep 1
#./tmux_session_commands.sh ipsec 1 "sleep 2"
./tmux_session_commands.sh ipsec 1 "vppctl set interface ipsec spd \$UPF_VPP_INTERFACE 1"
sleep 1
#./tmux_session_commands.sh ipsec 1 "sleep 2"
./tmux_session_commands.sh ipsec 1 "vppctl ipsec policy add spd 1 priority 100 inbound action bypass protocol 50"
sleep 1
#./tmux_session_commands.sh ipsec 1 "sleep 2"
./tmux_session_commands.sh ipsec 1 "vppctl ipsec policy add spd 1 priority 100 outbound action bypass protocol 50"
sleep 1
#./tmux_session_commands.sh ipsec 1 "sleep 2"
./tmux_session_commands.sh ipsec 1 "vppctl ipsec policy add spd 1 priority 10 outbound action protect sa 5 local-ip-range \$ip4_addr - \$ip4_addr remote-ip-range \$VPP_IPSEC_SERVER - \$VPP_IPSEC_SERVER"
sleep 1
#./tmux_session_commands.sh ipsec 1 "sleep 2"
./tmux_session_commands.sh ipsec 1 "vppctl ipsec policy add spd 1 priority 10 inbound action protect sa 6 local-ip-range \$ip4_addr - \$ip4_addr remote-ip-range \$VPP_IPSEC_SERVER - \$VPP_IPSEC_SERVER"
sleep 1
#./tmux_session_commands.sh ipsec 1 "sleep 2"
./tmux_session_commands.sh ipsec 1 "vppctl ipsec policy add spd 1 priority 200 inbound action bypass local-ip-range \$ip4_addr - \$ip4_addr remote-ip-range \$VPP_IPSEC_BYPASS - \$VPP_IPSEC_BYPASS"
sleep 1
#./tmux_session_commands.sh ipsec 1 "sleep 2"
./tmux_session_commands.sh ipsec 1 "vppctl ipsec policy add spd 1 priority 200 outbound action bypass local-ip-range \$ip4_addr - \$ip4_addr remote-ip-range \$VPP_IPSEC_BYPASS - \$VPP_IPSEC_BYPASS"
sleep 1
#./tmux_session_commands.sh ipsec 1 "sleep 2"
./tmux_session_commands.sh ipsec 1 "vppctl set interface ipsec spd Ethernet0 1"
sleep 1
#./tmux_session_commands.sh ipsec 1 "sleep 2"
./tmux_session_commands.sh ipsec 1 "vppctl sh ipsec all"
sleep 1

./tmux_session_commands.sh ipsec 1 "vppctl show int"

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
./tmux_session_commands.sh ipsec 2 "sudo bash  ./pktgen_server_scripts/start_pktgen.sh $size_packets"
sleep 3
./tmux_session_commands.sh ipsec 2 "Password\$2021"
sleep 3
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
./tmux_session_commands.sh ipsec 1 "vppctl show int"
sleep 2
./tmux_session_commands.sh ipsec 1 "vppctl show int"
./tmux_session_commands.sh ipsec 1 "systemctl status vpp"
./tmux_session_commands.sh ipsec 1 "journalctl -u vpp -n 50"
sleep 2
./tmux_session_commands.sh ipsec 1 "vppctl show errors"



./tmux_session_commands.sh "ipsec" "2" "stop 0"
sleep 10
./tmux_session_commands.sh "ipsec" "2" "quit"
sleep 10

#./tmux_session_commands.sh ipsec 1 "quit"
sleep 5
./tmux_session_commands.sh ipsec 1 "export VPP_IPSEC_BYPASS="192.168.251.10""
sleep 1
./tmux_session_commands.sh ipsec 1 "vppctl ipsec policy add spd 1 priority 200 inbound action bypass local-ip-range \$ip4_addr - \$ip4_addr remote-ip-range \$VPP_IPSEC_BYPASS - \$VPP_IPSEC_BYPASS"
sleep 1
#./tmux_session_commands.sh ipsec 1 "sleep 2"
./tmux_session_commands.sh ipsec 1 "vppctl ipsec policy add spd 1 priority 200 outbound action bypass local-ip-range \$ip4_addr - \$ip4_addr remote-ip-range \$VPP_IPSEC_BYPASS - \$VPP_IPSEC_BYPASS"
sleep 1

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

ping 192.168.251.10 -c 2 
sync
/root/lava_scripts/results_copy.sh  /root/tmux_0_ipsec.txt /lava/edgeq/perfreports/$build_id/$bsp_id $test_name.txt  equser@192.168.251.10 "Password\$2021" $test_suite
sync


cat /root/tmux_1_ipsec.txt
#sleep 2
cat /root/tmux_0_ipsec.txt
#cat /root/tmux_2_ipsec.txt
sleep 3
pkill -9 tmux
sleep 5
journalctl | grep monit;monit status pvtmon_B0;monit status pvtmon_b0



