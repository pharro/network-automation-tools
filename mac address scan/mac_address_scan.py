#!/usr/bin/python3
#mac_address_scan.py
# Inputs:   A Site id,  A Mac address
#
# Dependancy:   NORNIR (For site filtering), Netmiko w/ net_textfsm
#

import sys
from tabulate import tabulate
from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir.core.filter import F
import nornir_netmiko
import re


def fail_if_not_found(task: Task, mac_find) -> Result:
    #print(mac_find)
    if 'Invalid' in mac_find:
        raise Exception("Invalid input")
    mac_parse = re.search('^\s+(\d+)\s+(\w+\.\w+\.\w+)\s+\w+\s+(\w+\d+/\d+)', mac_find, re.M)
    if not mac_parse:
        raise Exception("MAC not found")
    
    return Result(
        host = task.host,
        result = mac_parse
    )

def MAC_SCAN(task: Task, mac_search):
    hostname = str(task.host)
    mac_find = task.run(
        name = "Check mac address table for mac_target",
        task = nornir_netmiko.netmiko_send_command,
        command_string=f'show mac address-table address {mac_search}',
    )
    check = task.run(
        name = "Check if found",
        task = fail_if_not_found,
        mac_find = mac_find.result
    )
    mac_parse_dict = {}
    if check.result:
        mac_parse_dict = {'hostname': hostname, 'vlan':check.result.group(1), 'mac':check.result.group(2), 'port':check.result.group(3)}

    if mac_parse_dict:
        interface_description = task.run(
            name = "Get interface description",
            task = nornir_netmiko.netmiko_send_command,
            command_string=f'show interfaces {mac_parse_dict["port"]} description',
        )
        interface_parse = re.search('^\w+\d+/\d+\s+\w+\s+\w+\s+(.*)', interface_description.result, re.M)
        mac_parse_dict['description'] = interface_parse.group(1)
   
    if mac_parse_dict:
        trunk_ports = task.run(
            name = "Get trunk ports",
            task = nornir_netmiko.netmiko_send_command,
            command_string=f'show interfaces {mac_parse_dict["port"]} switchport | in Operational Mode',
        )
        if 'trunk' in trunk_ports.result:
            mac_parse_dict['type'] = 'trunk'
        else:
            mac_parse_dict['type'] = 'access'
    
    if mac_parse_dict:
        table_result.append(mac_parse_dict)



def main():
    global table_result
    table_result = []
    site_filter = ''
    mac_search = ''
    if len(sys.argv) > 1:
        site_filter = sys.argv[1]
        mac_search = sys.argv[2]
    else:
        print('Input the Site ID:')
        site_filter = input()   # INPUT REQUIRED
        print('Input the MAC as: (####.####.####)')
        mac_search = input()  # INPUT REQUIRED

    if not site_filter or not mac_search:
        print('No input, closing program')
        sys.exit()

    # INITIALIZE NORNIR 
    nr = InitNornir(
        config_file="/home/pferro/netdevops_scripts/pharro/projects/MAC_address_Scan/config.yml"
    )

    # FILTER NORNIR HOSTS
    nr_site_hosts = nr.filter(F(site=site_filter) & ~F(role="ART") & ~F(role="SPARE"))

    # EXECUTE PLAYBOOK
    output = nr_site_hosts.run(
        name = "MAC SCAN PLAYBOOK",
        task = MAC_SCAN,
        mac_search = mac_search
    )

    if len(output.failed_hosts) == len(nr_site_hosts.inventory.hosts):
        print(f'{mac_search} was not found at {site_filter}')
    else:
        headers=["Hostname", "VLAN", "MAC-Addr", "Eth-Port", "Desc", "Oper Mode"]
        table = []
        for item in table_result:
            table.append([item['hostname'], item['vlan'], item['mac'], item['port'], item['description'], item['type']])
        print(tabulate(table, headers=headers))

if __name__ == '__main__':
    main()
