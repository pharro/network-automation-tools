# MAC Address Scan Tool
This program uses nornir and netmiko to scan Cisco IOS devices to identify which switches have a particular MAC address learned.

To use this tool you would need to specify a Site ID - from how your Nornir Inventory is populated, and a MAC address.

## Requirements in this version:
Need to install nornir, and tabulate.

### Nornir Inventory requirements:
Devices need to have their credentials.
Devices need to have a site.
If you want to do any additional filtering, you will need to update the program's FILTER NORNIR HOSTS section.

### Sample Output:
```
$python3 mac_address_scan.py AUS 1234.1234.1234

Hostname        VLAN  MAC-Addr        Eth-Port    Desc                            Oper Mode
------------  ------  --------------  ----------  ------------------------------  -----------
AUS-DSW1         255  1234.1234.1234  Et1/1       AUS-ASW2   E0/0                 trunk
AUS-ASW1         255  1234.1234.1234  Et0/0       AUS-DSW1   E1/0                 trunk
AUS-OOB-ASW1     255  1234.1234.1234  Et1/3       DO NOT MODIFY: AUS MGMT ACCESS  access
AUS-ASW2         255  1234.1234.1234  Et0/2       Connection to home.lab          trunk
```
