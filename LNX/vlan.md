# VLAN w RH (nmcli)

Dodanie VLANu do interfejsu (tataj do bonda, ale może być bezpośrednio).

Założenia:

- Dodawany VLAN: `258`
- Interface główny: `adm_bond`
- Interface VLANowy: `vlan258`
- Nazwa połączenia nmcli: `bkp`

## Dodawanie VLANu do interfejsu

```sh
$ sudo nmcli con add type vlan con-name bkp ifname vlan258 vlan.parent adm_bond vlan.id 258 ipv4.method manual ipv4.addresses 10.20.58.1/24
```