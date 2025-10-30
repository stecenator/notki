# Wymagania
- Host ma dostęp do obydwu io_grup
- Host ma skonfigurowane MPIO

Na podstawie dokmunetacji 
- [FS9200](https://www.ibm.com/docs/en/flashsystem-9x00/8.2.x?topic=volumes-moving-volume-between-io-groups-using-cli) i 
- [RHEL8 Multipathing](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html-single/configuring_device_mapper_multipath/index#overview-of-device-mapper-multipathing_configuring-device-mapper-multipath).

Poniższy przykład dotyczy migracji 4 LUNów z puli io1_SAS, w io_grupie 1 do io_grupy0, celem późniejszej ich migracji do puli io0_FCM. 

# Procedura migracji pomiędzy io_grupami
1. `FS7200`: Lista dysków do przeniesienia:
	```
	IBM_FlashSystem:waw6-tsm-v7k-nk00:superuser>lsvdisk -delim : | grep db- | grep io_grp1  | cut -f 1,2 -d ':'
	3:waw6-tsm-srv01-db-01
	4:waw6-tsm-srv01-db-02
	72:waw6-tsm-srv01-db-05
	74:waw6-tsm-srv01-db-07
	```
1. `FS7200`: Dopuszczenie ruchu przez `io_grp0`:
	```
	addvdiskaccess -iogrp io_grp0 waw6-tsm-srv01-db-01
	addvdiskaccess -iogrp io_grp0 waw6-tsm-srv01-db-02
	addvdiskaccess -iogrp io_grp0 waw6-tsm-srv01-db-05
	addvdiskaccess -iogrp io_grp0 waw6-tsm-srv01-db-07
	```
1. `HOST`: Odkrycie nowych ścieżek do dysków.
	Lista obecnych ścieżek:
	```
	[root@waw6-tsm-srv01 ~]# multipath -ll | grep 'db-0[1257]' -A 7
	waw6-tsm-srv01-db-01 (360050768108103b82800000000000007) dm-43 IBM,2145
	size=600G features='1 queue_if_no_path' hwhandler='1 alua' wp=rw
	|-+- policy='service-time 0' prio=50 status=active
	| |- 16:0:1:2  sdfa 129:192 active ready running
	| `- 17:0:3:2  sdez 129:176 active ready running
	`-+- policy='service-time 0' prio=10 status=enabled
	 |- 16:0:3:2  sdgk 132:0   active ready running
	  `- 17:0:1:2  sdgz 132:240 active ready running
	waw6-tsm-srv01-db-07 (360050768108103b82800000000000062) dm-78 IBM,2145
	size=600G features='1 queue_if_no_path' hwhandler='1 alua' wp=rw
	|-+- policy='service-time 0' prio=50 status=active
	| |- 16:0:1:72 sdko 66:448  active ready running
	| `- 17:0:3:72 sdkq 66:480  active ready running
	`-+- policy='service-time 0' prio=10 status=enabled
	  |- 16:0:3:72 sdip 135:144 active ready running
	  `- 17:0:1:72 sdjf 8:400   active ready running
	--
	waw6-tsm-srv01-db-05 (360050768108103b82800000000000060) dm-77 IBM,2145
	size=600G features='1 queue_if_no_path' hwhandler='1 alua' wp=rw
	|-+- policy='service-time 0' prio=50 status=active
	| |- 16:0:3:70 sdin 135:112 active ready running
	| `- 17:0:1:70 sdje 8:384   active ready running
	`-+- policy='service-time 0' prio=10 status=enabled
		|- 16:0:1:70 sdkm 66:416  active ready running
		`- 17:0:3:70 sdkp 66:464  active ready running
	--
	waw6-tsm-srv01-db-02 (360050768108103b82800000000000008) dm-52 IBM,2145 size=600G features='1 queue_if_no_path' hwhandler='1 alua' wp=rw
	|-+- policy='service-time 0' prio=50 status=active
	| |- 16:0:3:3  sdgl 132:16  active ready running
	| `- 17:0:1:3  sdhc 133:32  active ready running
	`-+- policy='service-time 0' prio=10 status=enabled
		|- 16:0:1:3  sdfc 129:224 active ready running
		`- 17:0:3:3  sdfb 129:208 active ready running
	```
1. `HOST`: Lista hostów SCSI do przeskanowania:
	```
	[root@waw6-tsm-srv01 ~]# ls /sys/class/fc_host/
	host1  host15  host16  host17
	```
	Czyli:
	- 1
	- 15
	- 16
	- 17
1. `HOST`: Odkrycie nowych ścieżek przez `io_grp0`:
	```
	[root@waw6-tsm-srv01 ~]# for i in 1 15 16 17; do echo "echo \"- - -\" > /sys/class/scsi_host/host${i}/scan"; done
	echo "- - -" > /sys/class/scsi_host/host1/scan
	echo "- - -" > /sys/class/scsi_host/host15/scan
	echo "- - -" > /sys/class/scsi_host/host16/scan
	echo "- - -" > /sys/class/scsi_host/host17/scan
	```
	Od biedy można też użyć `rescan_scsi_bus.sh`.
1. `HOST`: Weryfikacja czy ścieżki się znalazły:
	```
	[root@waw6-tsm-srv01 ibm]# multipath -ll | grep 'db-0[5]' -A 11
	waw6-tsm-srv01-db-05 (360050768108103b82800000000000060) dm-77 IBM,2145 size=600G features='1 queue_if_no_path' hwhandler='1 alua' wp=rw
	|-+- policy='service-time 0' prio=50 status=active
	| |- 16:0:3:70 sdin 135:112 active ready running
	| `- 17:0:1:70 sdje 8:384   active ready running
	`-+- policy='service-time 0' prio=10 status=enabled
	  |- 16:0:1:70 sdkm 66:416  active ready running
	  |- 17:0:3:70 sdkp 66:464  active ready running
	  |- 1:0:0:70  sdlb 67:400  active ready running
	  |- 1:0:2:70  sdlc 67:416  active ready running
	  |- 15:0:2:70 sdle 67:448  active ready running
	  `- 15:0:0:70 sdld 67:432  active ready running
	```
1. `FS7200`: Przeniesienie vdisków pomiędzy iogrupami:
	```
	movevdisk -iogrp io_grp0 -node 0 waw6-tsm-srv01-db-01
	movevdisk -iogrp io_grp0 -node 0 waw6-tsm-srv01-db-02
	movevdisk -iogrp io_grp0 -node 1 waw6-tsm-srv01-db-05
	movevdisk -iogrp io_grp0 -node 1 waw6-tsm-srv01-db-07
	```
1.  `HOST`: Weryfikacja czy ścieżki się przeniosły:
	```
	[root@waw6-tsm-srv01 ibm]# multipath -ll | grep 'db-0[1]' -A 11
	waw6-tsm-srv01-db-01 (360050768108103b82800000000000007) dm-43 IBM,2145 size=600G features='1 queue_if_no_path' hwhandler='1 alua' wp=rw
	|-+- policy='service-time 0' prio=50 status=active
	| |- 1:0:0:2   sddg 70:224  active ready running
	| `- 15:0:2:2  sdew 129:128 active ready running
	`-+- policy='service-time 0' prio=10 status=enabled
		|- 16:0:1:2  sdfa 129:192 active ready running
		|- 17:0:3:2  sdez 129:176 active ready running
		|- 1:0:2:2   sddk 71:32   active ready running
		|- 15:0:0:2  sdet 129:80  active ready running
		|- 16:0:3:2  sdgk 132:0   active ready running
		`- 17:0:1:2  sdgz 132:240 active ready running
	```
	**Uwaga 1:** Powyższy wydruk dotyczy tylko jednego dysku. Ten krok należy powtórzyć dla wszystkich przenoszonych LUNów.
	**Uwaga 2:** Należy dokładnie sprawdzić, czy nazwy sciezek na liście z priorytetem `prio=50` zostały zmienione. Jeśli nie to warto poczekać kilka minut, aż MPIO się połapie.
1. `FS7200`: Usunąć dostęp do LUNów przez starą IO Grupę:
	```
	rmvdiskaccess -iogrp io_grp1 waw6-tsm-srv01-db-01
	rmvdiskaccess -iogrp io_grp1 waw6-tsm-srv01-db-02
	rmvdiskaccess -iogrp io_grp1 waw6-tsm-srv01-db-05
	rmvdiskaccess -iogrp io_grp1 waw6-tsm-srv01-db-07
	```
1. `HOST`: Sprawdzenie, czy usnięte mapowania zostały odnotowane przez hosta:
	```
	waw6-tsm-srv01-db-01 (360050768108103b82800000000000007) dm-43 IBM,2145 size=600G features='1 queue_if_no_path' hwhandler='1 alua' wp=rw
	|-+- policy='service-time 0' prio=50 status=active
	| |- 1:0:0:2   sddg 70:224  active ready running
	| `- 15:0:2:2  sdew 129:128 active ready running
	`-+- policy='service-time 0' prio=10 status=enabled
		|- 16:0:1:2  sdfa 129:192 active faulty running
		|- 17:0:3:2  sdez 129:176 active faulty running
		|- 1:0:2:2   sddk 71:32   active ready running
		|- 15:0:0:2  sdet 129:80  active ready running
		|- 16:0:3:2  sdgk 132:0   active faulty running
		`- 17:0:1:2  sdgz 132:240 active faulty running
	```
	**Uwaga:** Ścieżki reprezentujące usunięte mapowania powinny mieć status `faulty`.
1. `HOST`: Usuwanie definicji odmapowanych scieżek:
	```
	[root@waw6-tsm-srv01 ibm]# rescan_scsi_bus.sh -r
	```
3. `HOST`: Sprawdzenie na hoście czy śćieżki zostały wyłączone:
	```
	[root@waw6-tsm-srv01 ibm]# multipath -ll | grep 'db-0[1]' -A 7
	waw6-tsm-srv01-db-01 (360050768108103b82800000000000007) dm-43 IBM,2145 size=600G features='1 queue_if_no_path' hwhandler='1 alua' wp=rw
	|-+- policy='service-time 0' prio=50 status=active
	| |- 1:0:0:2   sddg 70:224  active ready running
	| `- 15:0:2:2  sdew 129:128 active ready running
	`-+- policy='service-time 0' prio=10 status=enabled
		|- 1:0:2:2   sddk 71:32   active ready running
		`- 15:0:0:2  sdet 129:80  active ready running
	```
	**Uwaga:** W poleceniu `grep` warto podać też większą wartość parametru `-A`, żeby zyskać pewność, że odmapowane ścieżki naprawdę zostały usunięte.

# Migracja vdisków do nowej puli
Po wykonaniu migracji pomiędzy io_grupami, przenioesione LUNy nadal są w swojej oryginalnej puli, dostępnej z io_grupy 1. Dlatego operacje I/O są bardzo nieoptymalne: Host rozmawia z `io_grp0`, a ta po interconnect z `io_grp1`, dlatego nalęzy fizycznie przemigrować te luny do puli obsługiwanej przez mdiski nalezace do `io_grp0`.

1. Żeby nie umrzeć ze starośći, należy zmodyfikować `sync_rate` przenoszonych LUNów na 100%:
	```
	IBM_FlashSystem:waw6-tsm-v7k-nk00:superuser>chvdisk -syncrate 100 waw6-tsm-srv01-db-01
	IBM_FlashSystem:waw6-tsm-v7k-nk00:superuser>chvdisk -syncrate 100 waw6-tsm-srv01-db-02
	IBM_FlashSystem:waw6-tsm-v7k-nk00:superuser>chvdisk -syncrate 100 waw6-tsm-srv01-db-05
	IBM_FlashSystem:waw6-tsm-v7k-nk00:superuser>chvdisk -syncrate 100 waw6-tsm-srv01-db-07
	```
3. Uruchomienie migracji:
	```
	IBM_FlashSystem:waw6-tsm-v7k-nk00:superuser>migratevdisk -mdiskgrp io0_FCM -vdisk waw6-tsm-srv01-db-01
	IBM_FlashSystem:waw6-tsm-v7k-nk00:superuser>migratevdisk -mdiskgrp io0_FCM -vdisk waw6-tsm-srv01-db-02
	IBM_FlashSystem:waw6-tsm-v7k-nk00:superuser>migratevdisk -mdiskgrp io0_FCM -vdisk waw6-tsm-srv01-db-05
	IBM_FlashSystem:waw6-tsm-v7k-nk00:superuser>migratevdisk -mdiskgrp io0_FCM -vdisk waw6-tsm-srv01-db-07
	```
5. Przywrócenie oryginalnego `sync_rate`:
	```
	IBM_FlashSystem:waw6-tsm-v7k-nk00:superuser>chvdisk -syncrate 60 waw6-tsm-srv01-db-01
	IBM_FlashSystem:waw6-tsm-v7k-nk00:superuser>chvdisk -syncrate 60 waw6-tsm-srv01-db-02
	IBM_FlashSystem:waw6-tsm-v7k-nk00:superuser>chvdisk -syncrate 60 waw6-tsm-srv01-db-05
	IBM_FlashSystem:waw6-tsm-v7k-nk00:superuser>chvdisk -syncrate 60 waw6-tsm-srv01-db-07
	```