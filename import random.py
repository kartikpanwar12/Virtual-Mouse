import random
import time

class Packet:
    def _init_(self, src_ip, dst_ip, data):
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.data = data

class Host:
    def _init_(self, name, ip, mac):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.network = None

    def send_packet(self, dst_ip, data):
    
        packet = Packet(self.ip, dst_ip, data)
        event = f"{self.name} sending packet to {dst_ip} with data: {data}"
        self.network.log_event(event)
        self.network.deliver_packet(self, packet)

    def receive_packet(self, packet):
        if packet.dst_ip == self.ip:
            event = f"{self.name} received packet: {packet.data}"
        else:
            event = f"{self.name} dropped packet not for me"
        self.network.log_event(event)

class Network:
    def _init_(self, name):
        self.name = name
        self.hosts = []
        self.events = []  # dashboard log

    def add_host(self, host):
        host.network = self
        self.hosts.append(host)
        self.log_event(f"{host.name} joined {self.name} with IP {host.ip}")

    def deliver_packet(self, sender, packet):
        delivered = False
        for host in self.hosts:
            if host.ip == packet.dst_ip:
                host.receive_packet(packet)
                delivered = True
                break
        if not delivered:
            self.log_event(f"Packet from {packet.src_ip} to {packet.dst_ip} LOST in {self.name}")

    def log_event(self, event):
        timestamp = time.strftime("%H:%M:%S")
        entry = f"[{timestamp}] {event}"
        self.events.append(entry)
        print(entry)

    def show_dashboard(self):
        print("\n=== NETWORK DASHBOARD ===")
        print(f"Network: {self.name}")
        print(f"Hosts: {[host.name for host in self.hosts]}")
        print("\n--- Event Log ---")
        for event in self.events:
            print(event)
        print("=========================\n")


# Example Usage with 5 Nodes
net1 = Network("LAN1")

# Create 5 hosts
h1 = Host("Host1", "192.168.1.2", "AA:BB:CC:01")
h2 = Host("Host2", "192.168.1.3", "AA:BB:CC:02")
h3 = Host("Host3", "192.168.1.4", "AA:BB:CC:03")
h4 = Host("Host4", "192.168.1.5", "AA:BB:CC:04")
h5 = Host("Host5", "192.168.1.6", "AA:BB:CC:05")

# Add them to the network
net1.add_host(h1)
net1.add_host(h2)
net1.add_host(h3)
net1.add_host(h4)
net1.add_host(h5)

# Send some packets between them
h1.send_packet("192.168.1.3", "Hi bro this is sachin")  # valid
h2.send_packet("192.168.1.4", "Hello baby!")              # valid
h3.send_packet("192.168.1.10", "Testing unknown host")     # lost packet
h4.send_packet("192.168.1.6", "jai mata di")                # valid
h5.send_packet("192.168.1.2", "Replying to Host1!")        # valid

# Show the dashboard
net1.show_dashboard()