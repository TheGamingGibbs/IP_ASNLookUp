import requests
import re
import argparse
from ipaddress import ip_network

TokenIPINFO = 'YourTokenFromIPINFO'  # Replace with token from ipinfo.io

def Query_TypeCheck(Query, Token):
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'  #Reg pattern for IP address
    asn_pattern = r'\b(?:AS|as)\d{1,5}\b'  #Match both 'AS' or 'as' followed by 1 to 5 digits
    json_request1 = f"https://ipinfo.io/{Query}/json?token={Token}"  #JSON GET request to ipinfo.io
    json_response1 = requests.get(json_request1)  #JSON response after sending GET request to IPINFO
    ASNApi_JsonRequest = f"https://api.hackertarget.com/aslookup/?q={Query}&output=json"  #JSON GET request to hackertarget limited to 25 request per reqesting IP
    ASNApi_JsonResponse1 = requests.get(ASNApi_JsonRequest)  #JSON response to JSON GET

    if re.fullmatch(ip_pattern, Query):  #Regex logic for IPs
        print("You inputted an IP: " + Query)
        FormatIPJson(json_response1)  #Process IP data (no return value needed)
        return None  #Return None because there are no prefixes for IPs
    elif re.fullmatch(asn_pattern, Query, re.IGNORECASE):  #Regex logic for ASN
        print("You inputted an AS Number: " + Query)
        prefixesForIPs = FormatASNJson(ASNApi_JsonResponse1)  #Get ASN data
        return prefixesForIPs  #Return ASN prefixes for use in another function
    else:
        print("Invalid input. Please enter a valid IP or AS number.")
        return None

def FormatIPJson(json_response):
    data = json_response.json()  #Converts JSON response to a dictionary 
    #Display info
    print("\nExtracted Information:")
    print(f"IP: {data.get('ip', 'N/A')}")
    print(f"Hostname: {data.get('hostname', 'N/A')}")
    print(f"City: {data.get('city', 'N/A')}")
    print(f"Region: {data.get('region', 'N/A')}")
    print(f"Country: {data.get('country', 'N/A')}")
    print(f"Location: {data.get('loc', 'N/A')}")
    print(f"Organization: {data.get('org', 'N/A')}")
    print(f"Postal Code: {data.get('postal', 'N/A')}")
    print(f"Timezone: {data.get('timezone', 'N/A')}")
    print(f"Anycast: {data.get('anycast', 'N/A')}")

def FormatASNJson(json_response):
    data = json_response.json()  #Converts JSON response to a dictionary
    #Display info
    print("\nExtracted Information (ASN):")
    print(f"ASN: {data.get('asn', 'N/A')}")
    print(f"ASN NAME: {data.get('asn_name', 'N/A')}")
    print(f"IP BLOCKS: {data.get('prefixes', 'N/A')}")
    prefixesForIPs = data.get('prefixes', 'N/A')
    return prefixesForIPs  #Return the prefixes for further processing

def OrderIPAddressesSaveToFile(prefixesForIPsSave):
    if prefixesForIPsSave == 'N/A' or not prefixesForIPsSave:
        print("No IP blocks to save.")
        return

    #Convert to IP network objects
    ipv4_networks = sorted([ip_network(ip) for ip in prefixesForIPsSave if ":" not in ip])  # IPv4
    ipv6_networks = sorted([ip_network(ip) for ip in prefixesForIPsSave if ":" in ip])  # IPv6

    #Group IPv4 networks by first three octets (A.B.C.X)
    grouped_ipv4 = {}
    for net in ipv4_networks:
        #Extract the first three octets as integers for proper sorting
        octets = str(net.network_address).split(".")[:3]
        key = tuple(int(octet) for octet in octets)  # Create a tuple of integers for sorting
        grouped_ipv4.setdefault(key, []).append(str(net))

    #Open the file for writing the output
    with open("IPOutput.txt", "w") as f:
        def write_and_print(text=""):
            print(text)
            f.write(text + "\n")

        #Write sorted and grouped IPv4 networks to the file
        write_and_print("### Sorted and Grouped IPv4 Prefixes ###\n")
        for key in sorted(grouped_ipv4):  #Sort the groups by the tuple (A, B, C)
            for subnet in grouped_ipv4[key]:
                write_and_print(subnet)
        write_and_print()  #Empty line for separation

        #Write and save IPv6 networks to the file
        if ipv6_networks:
            write_and_print("### Sorted IPv6 Prefixes ###\n")
            for net in ipv6_networks:
                write_and_print(str(net))

def SaveToFile():
    print("Saving to file...")

def main():
    InputForQuery = argparse.ArgumentParser(description="Input either IPv4 address or ASN")
    InputForQuery.add_argument('-query', type=str, help="Input either IPv4 address or ASN")
    args = InputForQuery.parse_args()
    if args.query:
        SpecialData = Query_TypeCheck(args.query, TokenIPINFO)
        if SpecialData:  #Ensure data exists before proceeding
            print(SpecialData)
            SaveToFileAsk = input("Would you like to save IP blocks to a file? (y/n)").strip().lower()
            if SaveToFileAsk == 'y':
                OrderIPAddressesSaveToFile(SpecialData)  #Save IP blocks to file
            else:
                print("Goodbye")
        else:
            print("No data to process.")
    else:
        Query1 = input("Enter IP or ASN: ")
        SpecialData = Query_TypeCheck(Query1, TokenIPINFO)
        if SpecialData:
            print(SpecialData)
            SaveToFileAsk = input("Would you like to save IP blocks to a file? (y/n)").strip().lower()
            if SaveToFileAsk == 'y':
                OrderIPAddressesSaveToFile(SpecialData)  #Save IP blocks to file
            else:
                print("Goodbye")

if __name__ == "__main__":
    main()
