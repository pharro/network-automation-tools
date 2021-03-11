#!/usr/bin/python3
import yaml
import re

#Example hostlist
#hostlist = [['DC1-OOB-ASW1','10.1.255.100'], ['DC1-ART-SPARE01','10.1.255.101'], ['DC1-ART-SPARE02','10.1.255.102'], ['DC1-ART-SPARE03','10.1.255.103'], ['DC1-ART-SPARE04','10.1.255.104'], ['DC1-ART-SPARE05','10.1.255.105'], ['DC1-ART1','10.1.255.1'], ['DC1-ART2','10.1.255.2'], ['DC1-ASW1','10.1.255.5'], ['DC1-ASW2','10.1.255.6'], ['DC1-DSW1','10.1.255.3'], ['DC1-DSW2','10.1.255.4'], ['DC2-ART1','10.2.255.1'], ['DC2-ART2','10.2.255.2'], ['DC2-ASW1','10.2.255.5'], ['DC2-ASW2','10.2.255.6'], ['DC2-DSW1','10.2.255.3'], ['DC2-DSW2','10.2.255.4'], ['CAN1-ART1','10.117.255.1'], ['CAN1-ASW1','10.117.255.5'], ['LAM1-ART1','10.21.255.1'], ['LAM1-ASW1','10.21.255.5'], ['MAR1-ART1','10.186.255.1'], ['MAR1-DSW1','10.186.255.3'], ['MAR1-DSW2','10.186.255.4'], ['MID1-ART1','10.16.255.1'], ['MID1-DSW1','10.16.255.3'], ['MID1-DSW2','10.16.255.4'], ['ODE1-ART1','10.101.255.5'], ['ODE1-ASW1','10.101.255.5'], ['PAL1-ART1','10.195.255.1'], ['PAL1-ASW1','10.195.255.5'], ['PLE1-ART1','10.94.255.1'], ['PLE1-ASW1','10.94.255.5'], ['SUG1-ART1','10.221.255.1'], ['SUG1-ASW1','10.221.255.5'], ['TYL1-ART1','10.71.255.1'], ['TYL1-DSW1','10.71.255.3'], ['TYL1-DSW2','10.71.255.4'], ['WOO1-ART1','10.200.255.1'], ['WOO1-DSW1','10.200.255.3'], ['WOO1-DSW2','10.200.255.4'], ['SP-ALB1','10.255.255.7'], ['SP-AMA1','10.255.255.9'], ['SP-AUS1','10.255.255.122'], ['SP-BAT1','10.255.255.240'], ['SP-DAL1','10.255.255.112'], ['SP-HOU1','10.255.255.222'], ['SP-LIT1','10.255.255.251'], ['SP-LUB1','10.255.255.115'], ['SP-OAK1','10.255.255.121'], ['SP-SAN1','10.255.255.133']]

hostfile = open('production/hosts')
hostlist = eval(hostfile.read())



#DATA STRUCTURE
prod = {'all':{
            'hosts':{},  #ALL HOSTS
            'children':{
                'sites':{
                    'children':{  #SITES > Hosts
                    }
                },
                'roles':{
                    'children':{ #SITES > Hosts
                    }
                }
            },
            'vars':{
                'ansible_user': 'ansible',
                'ansible_password': 'ansible',
                'ansible_become': 'yes',
                'ansible_become_method': 'enable',
                'ansible_become_password': 'ansible',
                'ansible_connection': 'ansible.netcommon.network_cli',
                'ansible_network_os': 'cisco.ios.ios'
            }
        }
    }

#DATA STRUCTURE FOR A HOST
host = {'hostname_tbd':{'ansible_host': 'tbd'}}


for count, host in enumerate(hostlist):
    hostname = hostlist[count][0]
    address = hostlist[count][1]
    site = hostname.split('-')[0]
    if 'SP' in hostname:
        pass
    elif 'OOB' in hostname:
        role = hostname.split('-')[2][:-1]
    elif 'SPARE' in hostname:
        role = hostname.split('-')[2][:-2]
    else:
        role = hostname.split('-')[1][:-1]
    host = {hostname:{'ansible_host': address}}
    prod['all']['hosts'][hostname] = {'ansible_host': address}
    prod['all']['children']['sites']['children'].setdefault(site, {})
    prod['all']['children']['sites']['children'][site].setdefault('hosts', {})
    prod['all']['children']['sites']['children'][site]['hosts'][hostname] = ""
    prod['all']['children']['roles']['children'].setdefault(role, {})
    prod['all']['children']['roles']['children'][role].setdefault('hosts', {})
    prod['all']['children']['roles']['children'][role]['hosts'][hostname] = ""



# DUMP DICT TO YAML (STR)
hostsyaml = (yaml.dump(prod, explicit_start=True))

#STRIPING EXTRA QOUTES
stripqoutes = re.compile(" ''")
hostsyaml = stripqoutes.sub("", hostsyaml)

#PRINT AND SAVE OUTPUT
print(hostsyaml)
yamlfile = open('/home/pferro/netdevops_scripts/pharro/temp_output/ansible_hosts.yaml', 'w')
yamlfile.write(hostsyaml)
yamlfile.close
