import requests

# Function to get organization data from an IP address
def get_organization_data(ip, token):
    url = f"https://ipinfo.io/{ip}/json?token={token}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('org', 'N/A')  # Extract organization field
    else:
        return None

# Function to process IP addresses from input file and write valid subnets to output file
def process_ip_file(input_file, output_file, token):
    processed_subnets = set()  # Use a set to store unique subnets

    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue  # Skip empty lines

            # Extract IP and subnet
            if "/" in line:
                ip, subnet = line.split('/')
            else:
                continue  # Invalid format, skip

            subnet = int(subnet)  # Convert subnet mask to an integer
            ip_parts = ip.split('.')
            base_third_octet = int(ip_parts[2])  # The Y in X.X.Y.Z

            # Modify last octet to .15 for the first request
            first_ip = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.15"
            print(f"Checking {first_ip} for organization...")

            # Get the initial organization
            first_org = get_organization_data(first_ip, token)
            if first_org is None:
                print(f"Failed to get org data for {first_ip}, skipping...")
                continue
            
            print(f"Org for {first_ip}: {first_org}")

            # Store all matching subnets
            matching_subnets = set()
            matching_subnets.add(f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/{subnet}")  # Keep original subnet

            # Determine step size based on subnet mask
            if subnet == 24:
                step = 1
            elif subnet == 23:
                step = 2
            elif subnet == 22:
                step = 4  # Corrected for /22
            else:
                continue  # Unsupported subnet, skip

            # Check decreasing third octet
            for decrement in range(step, 10, step):
                new_third_octet = base_third_octet - decrement
                if new_third_octet < 0:
                    break  # Stop if we go negative

                new_ip = f"{ip_parts[0]}.{ip_parts[1]}.{new_third_octet}.15"
                print(f"Checking {new_ip}...")

                org_data = get_organization_data(new_ip, token)
                if org_data == first_org:
                    matching_subnets.add(f"{ip_parts[0]}.{ip_parts[1]}.{new_third_octet}.0/{subnet}")
                else:
                    break  # Stop checking downward when org changes

            # Check increasing third octet
            for increment in range(step, 10, step):
                new_third_octet = base_third_octet + increment
                if new_third_octet > 255:
                    break  # Stop if we exceed the valid range

                new_ip = f"{ip_parts[0]}.{ip_parts[1]}.{new_third_octet}.15"
                print(f"Checking {new_ip}...")

                org_data = get_organization_data(new_ip, token)
                if org_data == first_org:
                    matching_subnets.add(f"{ip_parts[0]}.{ip_parts[1]}.{new_third_octet}.0/{subnet}")
                else:
                    break  # Stop checking upward when org changes

            # Add unique subnets to final set
            processed_subnets.update(matching_subnets)

    # Write unique sorted subnets to the output file
    with open(output_file, 'w') as output:
        for subnet in sorted(processed_subnets, key=lambda x: tuple(map(int, x.split('.')[0:3]))):
            output.write(subnet + "\n")

# Example usage
input_file_for_ip_check = 'Test.txt'  # Input file
output_file = 'Output.txt'  # Output file
token = 'YOUR_IPINFO_TOKEN'  # Replace with your actual IPInfo token

process_ip_file(input_file_for_ip_check, output_file, token)
