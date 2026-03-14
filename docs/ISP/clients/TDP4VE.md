# Spectrum Protect for Virtual Environmanets

Wrażenia z placu boju po instalacji TDP4VE.

## Linux - wymagania wstępne:

- SELinux - `disabled` lub `permissive`
- Pakiety (poza standardowymi klienckimi)
  - fuse-libs
  - bind-utils
  - vim-enhanced
  - metacity
- System powinien być czysty, **To znaczy żadnych kawałków SP wcześniej zainstalowanych**.

## Porty firewall do otworzenia na DataMoverze

- 1501
- 1502
- 1503 
- 9081 (GUI)
- 3260 (iSCSI)
- 3985 (Mount Proxy)
- 135

Na RedHatopodobnych:

```bash
firewall-cmd --add-port 1501-1503/tcp
firewall-cmd --add-port 1501-1503/tcp --permanent
firewall-cmd --add-port 1581-1583/tcp
firewall-cmd --add-port 1581-1583/tcp --permanent
firewall-cmd --add-port 9081/tcp
firewall-cmd --add-port 9081/tcp --permanent
firewall-cmd --add-port 9080/tcp
firewall-cmd --add-port 9080/tcp --permanent
firewall-cmd --add-port 3260/tcp --permanent
firewall-cmd --add-port 3260/tcp
firewall-cmd --add-port 5985/tcp --permanent
firewall-cmd --add-port 5985/tcp
firewall-cmd --add-port 135/tcp --permanent
firewall-cmd --add-port 135/tcp
```

## Uprawnienia dla użyszkodnika vCenter

- [Uprawnienia](https://www.ibm.com/support/pages/node/713157)

