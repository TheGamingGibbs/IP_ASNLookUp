# IP_ASNLookUp
Some Python tools to allow you to lookup IP address info

IPScriptLookup.py queries ipinfo.io and hackertarget.com based off your input

`python3 IPScriptLookup.py`


`python3 IPScriptLookup.py -query 8.8.8.8`

```text
You inputted an IP: 8.8.8.8
Extracted Information:
IP: 8.8.8.8
Hostname: dns.google
City: Mountain View
Region: California
Country: US
Location: 38.0088,-122.1175
Organization: AS15169 Google LLC
Postal Code: 94043
Timezone: America/Los_Angeles
Anycast: True
No data to process.
```

`python3 IPScriptLookup.py -query as15169`

```text
You inputted an AS Number: as15169

Extracted Information (ASN):
ASN: 15169
ASN NAME: GOOGLE, US
IP BLOCKS: ['173.194.206.0/24',...TRUNCATED DATA...]
Would you like to save IP blocks to a file? (y/n)
```

If you say yes it will save the blocks out, you can then take that file and just copy the IPv4 block and pump it into IPIteratorLookup.py, this will check the whole file and see if the IPs above and below the IPs in the file are owned by the same ASN Org. it then outputs it into another text file

`python3 IPIteratorLookup.py`

This will take an input file of IP address ranges and check the ranges next to it to see if the ASN Org is the same, useful if youre trying to make a block list, there are some wonky stuff with /22 and /23 addresses, will be fixed later.
