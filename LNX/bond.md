# Bonding na Linuxie

Założenia:

- LACP
- nazwa interfesju bondowego: `adm_bond`
- interfejsy fizyczne:
	- `ens4f0np0` - adm_bond-if1
	- `ens1f0np0` - adm_bond-if1
- Od razu nadaję IP. JAk nie nadam, to trzeba koniecznie wyłączyć DHCP bo się złoży jak nic nie dostanie. 

## Tworzenie bonda

```sh
$ sudo nmcli con add type bond con-name ADM_bond ifname adm_bond mode 802.3ad ip4 10.20.59.6/24
$ sudo nmcli con add type ethernet slave-type bond con-name adm_bond-if1 ifname ens4f0np0 master adm_bond
$ sudo nmcli con add type ethernet slave-type bond con-name adm_bond-if2 ifname ens1f0np0 master adm_bond
$ nmcli c s 
NAME          UUID                                  TYPE      DEVICE    
ADM_bond      716a0118-c82e-4aca-aade-04e202cc50d2  bond      adm_bond  
hb-bond       5b54425e-0a5f-45b1-984a-5e97eb42d9fe  bond      hb-bond   
virbr0        644f81ee-2cef-4289-bb8c-b171612d231c  bridge    virbr0    
adm_bond-if1  7487208d-2eea-4830-905c-5220073e58e9  ethernet  ens4f0np0 
adm_bond-if2  dc6522ad-f9ba-410d-93c7-ce9a439d9572  ethernet  ens1f0np0 
hb-bond-if1   fbe86a37-67ce-4e6c-b514-f6b0e4143030  ethernet  ens9f0    
hb-bond-if2   2e2c46e5-9740-45da-956a-fd8fcaf66576  ethernet  ens9f1    
ens1f0        d2be7a60-d92f-4ad0-9de7-77fa91071c54  ethernet  --        
ens1f1        e5107345-6b6c-49c9-9480-9d983e83ef3f  ethernet  --        
ens4f0        7d9af5c5-5b06-4f92-a033-e27f386cca77  ethernet  --        
ens4f1        0088ac7b-d8e2-42f7-9249-a3bc8ef9c54e  ethernet  --        
ens9f0        c2d4c0b4-2971-401a-ba83-21b8ac782abf  ethernet  --        
ens9f1        0f8142d2-f3a9-4a3c-aebd-cd6983eb09e4  ethernet  --        
ens9f2        3c4c317d-92a8-42a0-b609-ef212bb16cce  ethernet  --        
ens9f3        6767b662-923c-4477-a086-b52c7013420f  ethernet  -- 
```