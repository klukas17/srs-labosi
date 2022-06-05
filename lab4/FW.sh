#! /bin/sh

IPT=/sbin/iptables

$IPT -P INPUT DROP
$IPT -P OUTPUT DROP
$IPT -P FORWARD DROP

$IPT -F INPUT
$IPT -F OUTPUT
$IPT -F FORWARD

$IPT -A INPUT   -m state --state ESTABLISHED,RELATED -j ACCEPT
$IPT -A OUTPUT  -m state --state ESTABLISHED,RELATED -j ACCEPT
$IPT -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT

#
# za potrebe testiranja dozvoljen je ICMP (ping i sve ostalo)
#
$IPT -A INPUT   -p icmp -j ACCEPT
$IPT -A FORWARD -p icmp -j ACCEPT
$IPT -A OUTPUT  -p icmp -j ACCEPT


# ================ Dodajte ili modificirajte pravila na oznacenim mjestima #
# "anti spoofing" (eth0)
#
$IPT -A INPUT   -i eth0 -s 127.0.0.0/8  -j DROP
$IPT -A FORWARD -i eth0 -s 127.0.0.0/8  -j DROP
# PRAVILO 1:
$IPT -A FORWARD -i eth0 -s 10.0.0.0/24 -j DROP
$IPT -A FORWARD -i eth0 -s 203.0.113.0/24 -j DROP

#
# racunala iz lokalne mreze (LAN) imaju neograniceni pristup posluziteljima u DMZ i Internetu
#
# PRAVILO 2:
$IPT -A FORWARD -i eth1 -s 10.0.0.0/24 -j ACCEPT

#
# iz vanjske mreze (Interneta) dozvoljen je pristup posluzitelju server u DMZ korištenjem 
# protokola SSH (tcp port 22) i DNS (udp i tcp port 53)
#
# PRAVILO 3:
$IPT -A FORWARD -p tcp --dport 22 -i eth0 -d 203.0.113.10 -j ACCEPT
$IPT -A FORWARD -p tcp --dport 53 -i eth0 -d 203.0.113.10 -j ACCEPT
$IPT -A FORWARD -p udp --dport 53 -i eth0 -d 203.0.113.10 -j ACCEPT

#
# pristup iz vanjske mreze i DMZ u lokalnu LAN mrezu je zabranjen, dozvoljen je samo 
# pristup posluzitelju host (u LAN-u) s posluzitelja server (u DMZ) korištenjem protokola SSH
#
# PRAVILO 4:
$IPT -A FORWARD -p tcp --dport 22 -i eth2 -s 203.0.113.10 -d 10.0.0.11 -j ACCEPT

#
# s posluzitelja server je dozvoljen pristup DNS posluziteljima u Internetu (UDP i TCP port 53)
#
# PRAVILO 5:
$IPT -A FORWARD -p tcp --dport 53 -i eth2 -s 203.0.113.10 -j ACCEPT
$IPT -A FORWARD -p udp --dport 53 -i eth2 -s 203.0.113.10 -j ACCEPT

#
# SSH pristup vatrozidu firewall je dozvoljen samo s računala admin (LAN)
#
# PRAVILO 6:
$IPT -A INPUT -p tcp --dport 22 -i eth1 -s 10.0.0.10 -j ACCEPT