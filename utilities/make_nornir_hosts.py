#!/usr/bin/python3

import yaml

#Example Host List
#hostlist = [['DC1-OOB-ASW1','10.1.255.100'], ['DC1-ART-SPARE01','10.1.255.101'], ['DC1-ART-SPARE02','10.1.255.102'], ['DC1-ART-SPARE03','10.1.255.103'], ['DC1-ART-SPARE04','10.1.255.104'], ['DC1-ART-SPARE05','10.1.255.105'], ['DC1-ART1','10.1.255.1'], ['DC1-ART2','10.1.255.2'], ['DC1-ASW1','10.1.255.5'], ['DC1-ASW2','10.1.255.6'], ['DC1-DSW1','10.1.255.3'], ['DC1-DSW2','10.1.255.4'], ['DC2-ART1','10.2.255.1'], ['DC2-ART2','10.2.255.2'], ['DC2-ASW1','10.2.255.5'], ['DC2-ASW2','10.2.255.6'], ['DC2-DSW1','10.2.255.3'], ['DC2-DSW2','10.2.255.4'], ['CAN1-ART1','10.117.255.1'], ['CAN1-ASW1','10.117.255.5'], ['LAM1-ART1','10.21.255.1'], ['LAM1-ASW1','10.21.255.5'], ['MAR1-ART1','10.186.255.1'], ['MAR1-DSW1','10.186.255.3'], ['MAR1-DSW2','10.186.255.4'], ['MID1-ART1','10.16.255.1'], ['MID1-DSW1','10.16.255.3'], ['MID1-DSW2','10.16.255.4'], ['ODE1-ART1','10.101.255.5'], ['ODE1-ASW1','10.101.255.5'], ['PAL1-ART1','10.195.255.1'], ['PAL1-ASW1','10.195.255.5'], ['PLE1-ART1','10.94.255.1'], ['PLE1-ASW1','10.94.255.5'], ['SUG1-ART1','10.221.255.1'], ['SUG1-ASW1','10.221.255.5'], ['TYL1-ART1','10.71.255.1'], ['TYL1-DSW1','10.71.255.3'], ['TYL1-DSW2','10.71.255.4'], ['WOO1-ART1','10.200.255.1'], ['WOO1-DSW1','10.200.255.3'], ['WOO1-DSW2','10.200.255.4'], ['SP-ALB1','10.255.255.7'], ['SP-AMA1','10.255.255.9'], ['SP-AUS1','10.255.255.122'], ['SP-BAT1','10.255.255.240'], ['SP-DAL1','10.255.255.112'], ['SP-HOU1','10.255.255.222'], ['SP-LIT1','10.255.255.251'], ['SP-LUB1','10.255.255.115'], ['SP-OAK1','10.255.255.121'], ['SP-SAN1','10.255.255.133']]

hostfile = open('production/hosts')
hostlist = eval(hostfile.read())

list = {}
for count, host in enumerate(hostlist):
    hostname = hostlist[count][0]
    address = hostlist[count][1]
    site = hostname.split('-')[0]
    if 'OOB' in hostname:
        role = hostname.split('-')[2][:-1]
    elif 'SPARE' in hostname:
        role = hostname.split('-')[2][:-2]
    else:
        role = hostname.split('-')[1][:-1]
    list[hostname] = {
        'hostname': address,
        'platform': 'ios',
        'username': 'ansible',
        'password': 'ansible',
        'data': {
            'site': site,
            'role': role
            }
        }




print(yaml.dump(list, explicit_start=True))
#yamlfile = open('./Output/hosts.yaml', 'w')
#yamlfile.write(yaml.dump(list, explicit_start=True))
#yamlfile.close

"""
Outputs a file that looks like:
---
CAN1-ART1:
  data:
    role: ART
    site: CAN1
  groups:
  - site_router
  hostname: 10.117.255.1
  platform: ios
CAN1-ASW1:
  data:
    role: ASW
    site: CAN1
  groups:
  - site_switch
  hostname: 10.117.255.5
  platform: ios
"""
