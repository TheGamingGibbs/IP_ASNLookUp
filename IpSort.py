from ipaddress import ip_network

# List of provided IP prefixes
ip_prefixes = [
    "x.x.x.x/24", "x.x.x.y/24",
]

# Convert to IP network objects
ipv4_networks = sorted([ip_network(ip) for ip in ip_prefixes if ":" not in ip])  # IPv4
ipv6_networks = sorted([ip_network(ip) for ip in ip_prefixes if ":" in ip])  # IPv6

# Group IPv4 networks by first three octets
grouped_ipv4 = {}
for net in ipv4_networks:
    # Extract the first three octets as integers for proper sorting
    octets = str(net.network_address).split(".")[:3]
    key = tuple(int(octet) for octet in octets)  # Create a tuple of integers for sorting
    grouped_ipv4.setdefault(key, []).append(str(net))

# Print sorted and grouped IPv4 networks
print("\n### Sorted and Grouped IPv4 Prefixes ###\n")
for key in sorted(grouped_ipv4):
    print("\n".join(grouped_ipv4[key]))
    print()  # Empty line for separation

# Print IPv6 separately
if ipv6_networks:
    print("\n### Sorted IPv6 Prefixes ###\n")
    for net in ipv6_networks:
        print(net)