# Zabawy z Inventory Ansibla

## Wartości zmiennych

Wyświetlanie zmiennych dostępnych dla hostów zdefiniowanych pliku inventory (tutaj to `hsm-tsma.pcss`:

```sh
$ ansible-inventory -i hsm-tsma.pcss --list
```

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