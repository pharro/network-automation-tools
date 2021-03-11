# Ansible Playbook to update NTP servers, verify if working, and cleanup old NTP settings.

## How to use:
Define new servers to be added.
*This will remove any other servers currently configured.*

For testing, the hosts is currently set to a static host.  Update the playbook to include the group of hosts you wish to update.
Also, the failed_when condition is set to fail when the new NTP is not ".INIT."  Or not yet working.  Just remove the "not" statement in that condition.

During testing, I've found that NTP takes time to sync.  So when deploying in my lab, I deployed small groups of hosts.


## Example output:
```
NTP server to add, sperated by commas: 10.10.10.10,10.11.11.11

PLAY [configure NTP for Site Switches] ***********************************************************************************************************************************************************************

TASK [set_fact] **********************************************************************************************************************************************************************************************
ok: [CAN1-ASW1]

TASK [PRE-CHECK] *********************************************************************************************************************************************************************************************
ok: [CAN1-ASW1]

TASK [PRINT PRE-CHECK] ***************************************************************************************************************************************************************************************
ok: [CAN1-ASW1] => 
  msg:
    vrf:
      default:
        address:
          10.117.255.1:
            isconfigured:
              'True':
                address: 10.117.255.1
                isconfigured: true
            type:
              server:
                address: 10.117.255.1
                type: server
                vrf: default

TASK [CONFIGURE NTP] *****************************************************************************************************************************************************************************************
changed: [CAN1-ASW1] => (item=10.10.10.10)
changed: [CAN1-ASW1] => (item=10.11.11.11)

TASK [POST-CHECK] ********************************************************************************************************************************************************************************************
ok: [CAN1-ASW1] => (item=10.10.10.10)
ok: [CAN1-ASW1] => (item=10.11.11.11)

TASK [Cleanup] ***********************************************************************************************************************************************************************************************
changed: [CAN1-ASW1] => (item={'key': '10.117.255.1', 'value': {'type': {'server': {'address': '10.117.255.1', 'type': 'server', 'vrf': 'default'}}, 'isconfigured': {'True': {'address': '10.117.255.1', 'isconfigured': True}}}})

TASK [Get Final config] **************************************************************************************************************************************************************************************
ok: [CAN1-ASW1]

TASK [PRINT Final config to TERMINAL WINDOW] *****************************************************************************************************************************************************************
ok: [CAN1-ASW1] => 
  msg:
    vrf:
      default:
        address:
          10.10.10.10:
            isconfigured:
              'True':
                address: 10.10.10.10
                isconfigured: true
            type:
              server:
                address: 10.10.10.10
                type: server
                vrf: default
          10.11.11.11:
            isconfigured:
              'True':
                address: 10.11.11.11
                isconfigured: true
            type:
              server:
                address: 10.11.11.11
                type: server
                vrf: default

PLAY RECAP ***************************************************************************************************************************************************************************************************
CAN1-ASW1                  : ok=8    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0  
```
