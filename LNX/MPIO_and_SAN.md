# Usuwanie LUNu z Linuxa

## Wstęp

Zamontowane dwa filesytemy:

```
/dev/mapper/pwpwvg-pwpwlv               10G  104M  9.9G   2% /pwpw
/dev/mapper/pwpw_origvg-pwpwlv          10G  104M  9.9G   2% /pwpw_orig
```

W takich grupach:

```
  pwpw_origvg           1   1   0 wz--n-  <128.00g <118.00g
  pwpwvg                1   1   0 wz--n-  <128.00g <118.00g
```

## Procedura

Na przykładzie:

- grupy `pwpwvg`
- LV `pwpw-lv`
- urządzenia 

 ```
mpathd (36005076300808505d000000000000070) dm-17 IBM,2145
size=128G features='1 queue_if_no_path' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| |- 2:0:3:2 sdw  65:96  active ready running
| |- 2:0:4:2 sdx  65:112 active ready running
| |- 4:0:4:2 sdz  65:144 active ready running
| `- 4:0:6:2 sdaa 65:160 active ready running
`-+- policy='service-time 0' prio=10 status=enabled
  |- 2:0:0:2 sdu  65:64  active ready running
  |- 2:0:1:2 sdv  65:80  active ready running
  |- 4:0:0:2 sdy  65:128 active ready running
  `- 4:0:7:2 sdab 65:176 active ready running
 ```

1. Odmontuj filesystem

	```
  [root@pandora ~]# umount /pwpw
  [root@pandora ~]# umount /pwpw_orig
  ```

1. Deaktywyj grupy woluminów

	```
  [root@pandora ~]# vgchange -an pwpwvg 
    0 logical volume(s) in volume group "pwpwvg" now active
  [root@pandora ~]# vgchange -an pwpw_origvg 
    0 logical volume(s) in volume group "pwpw_origvg" now active
  ```

1. Pewnie trzeba je wyeksportować albo usunać.
1.  
