---
icon: simple/ansible
---

# Ansible

Rzeczy związane z automatyzacją. Rozkminiam moduły IBMa, ale jest tu też trochę generycznych tematów linuxowych.

## Wartości zmiennych

Wyświetlanie zmiennych dostępnych dla hostów zdefiniowanych pliku inventory (tutaj to `hsm-tsma.pcss`):

```
ansible-inventory -i hsm-tsma.pcss --list
```

To polecenie można także wołać z opcją `-l host-albo-grupa` żeby podglądać wartości tylko wybranych celów.

Outut jest w JSONie. (przykład przycięty:

```json
{
    "_meta": {
        "hostvars": {
            "hsm01.adm.pcss": {
                "ibm_admns": [
                    {
                        "enc_pass": "$6$5uVfNxmpWExCDKq7$gbkIYM0/vl92x/XWYZhdzRTWvQrl/FWqDwtfACO7hCB2lxL0YVt5Gks2GnWMyEERMRcwBBOvqjfBhB3OwKtQK/",
                        "gecos": "Ajbiem Juzer",
                        "ssh_key": "{{ playbook_dir }}/files/marcinek.pub",
                        "username": "ibm"
                    }
                ],
                "inst_src_dir": "/home/ibm/install",
                "node_name": "hsm01",
                "pkgs": [
                    "chrony",
                    "setroubleshoot",
                    "device-mapper-multipath",
                    "vim-enhanced",
                    "tmux",
                    "wget"
                ],
                "ssh_pub_keys": [
                    "{{ playbook_dir }}/files/marcinek.pub",
                    "{{ playbook_dir }}/files/tomek.pub",
                    "{{ playbook_dir }}/files/robert.pub",
                    "{{ playbook_dir }}/files/laszlo.pub",
                    "{{ playbook_dir }}/files/marpan.pub"
                ],
                "tsm_pacemaker_primary": false
            }
         }
}
```