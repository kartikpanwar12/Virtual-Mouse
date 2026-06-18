import ipaddress

# Function to find IP class and default mask
def classify_ip(ip):
    first = int(ip.split('.')[0])
    if 1 <= first <= 126: return 'Class A', '255.0.0.0'
    if 128 <= first <= 191: return 'Class B', '255.255.0.0'
    if 192 <= first <= 223: return 'Class C', '255.255.255.0'
    if 224 <= first <= 239: return 'Class D (Multicast)', 'N/A'
    if 240 <= first <= 254: return 'Class E (Reserved)', 'N/A'
    return 'Invalid IP', 'N/A'

# Function to get subnet details
def subnet_info(cidr):
    net = ipaddress.ip_network(cidr, strict=False)
    hosts = net.num_addresses - 2 if net.prefixlen < 31 else net.num_addresses
    host_range = f"{net.network_address+1} - {net.broadcast_address-1}" if net.prefixlen < 31 else "N/A"
    return net.network_address, net.broadcast_address, net.netmask, hosts, host_range

# Example
ip = "192.168.1.1"
cidr = "192.168.1.0/24"

ip_class, default_mask = classify_ip(ip)
print("IP Address:", ip)
print("Class:", ip_class)
print("Default Mask:", default_mask)

net, broad, mask, hosts, hrange = subnet_info(cidr)
print("Network Address:", net)
print("Broadcast Address:", broad)
print("Netmask:", mask)
print("Total Hosts:", hosts)
print("Host Range:", hrange)