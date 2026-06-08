---
icon: simple/linux
---

# Konfiguracja OSów pod klaster


!!! Attention "Uwaga"
	Zakładam, ze na razie dyski grupy klastrowej są podłaczone jedynie do węzła __sp-n1__. Większość poniższych komend trzeba wykonać na obu węzłach, ale dopóki nie przejdziesz do sekcji [Dodawanie grupy woluminów do drugiego węzła klastra](#dodawanie-grupy-woluminow-do-drugiego-weza-klastra) polecenia związane z LVM wykonuj tylko na pierwszym węźle!

## Przygotowanie pierwszego węzła

1. Ustaw hasło na użtkownika `hacluster`. Najlpiej na coś dobrze zarządzanego, albo znanego jak :elephant: ;-). 
1. Dodaj usługi klastrowe i Protecta do firewalla i przeładuj regułki.

	```sh title="Dodwanie regułek ha i ISP na teraz i wieki wieków"
	firewall-cmd --add-service=high-availability
	firewall-cmd --add-service=high-availability --permanent
	firewall-cmd --add-port=1500/tcp
	firewall-cmd --add-port=1500/tcp --permanent
	firewall-cmd --add-port=11090/tcp
	firewall-cmd --add-port=11090/tcp --permanent
	```

1. Upewnij się, że _SELinux_ jest ustawiony w _Permissive_ :angry:.

	```sh title="Selinux w permissive"
	getenforce
	```

	Jeśli nie jest to oczyście `setenforce 0`.

1. Włącz usługę `pcsd`.

	```sh title="pcsd teraz i zawsze"
	systemctl start  pcsd
	systemctl enable pcsd
	```

1. Dostosuj konfigurację LVM do pracy w klastrze.

	```sh title="Zamiana system_id_source w /etc/lvm/lvm.conf"
	sudo sed -i '/^[[:space:]]# system_id_source = "none"/a\        system_id_source = "uname"' /etc/lvm/lvm.conf
	```

	!!! Attention "Uwaga"
		Ej-Aj, także ten ze strony RedHata twierdzi, że poniższe opcje nie są potrzebne jeśli, tak jak ja. Ale dla "dorosłych" klastrów to się możę przydać. 


	Używaj `lvm2-lockd`

	```sh title="Zamiana system_id_source w /etc/lvm/lvm.conf"
	sudo sed -i '/^[[:space:]]# use_lvmlockd = 0/a\        use_lvmlockd = 1' /etc/lvm/lvm.conf
	```

1. Włącz i wystartuj `lvmlockd` i `sanlock`:

	```sh title="Lock w LVM"
	systemctl enable lvmlockd
	systemctl enable sanlock
	systemctl start lvmlockd
	systemctl start sanlock
	```

1. Upewnij się, że plik startujący instancję ISP jest na obu nodach. Instancja __nie może strtować automatycznie!!__
1. Upewnij się, że grupy woluminów zawierające klastrowe filesystemy nie są automatycznie montowane.

	```sh title="Wyłączanie automatycznej aktywacji grupy woluminów"
	sudo vgchange --setautoactivation n spvg 
	```

1. Upewnij się, że systemy plików z klastrowej grupy nie będą automatycznie montowane:

	```sh hl_lines="15-20" title="Opcja noauto"
	#
	# /etc/fstab
	# Created by anaconda on Fri Jul  4 20:31:17 2025
	#
	# Accessible filesystems, by reference, are maintained under '/dev/disk/'.
	# See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info.
	#
	# After editing this file, run 'systemctl daemon-reload' to update systemd
	# units generated from this file.
	#
	/dev/mapper/rhel-root   /                       xfs     defaults        0 0
	UUID=47912287-4e97-4c7f-93b2-726fd6711763 /boot                   xfs     defaults        0 0
	/dev/mapper/rhel-home   /home                   xfs     defaults        0 0
	/dev/mapper/rhel-swap   none                    swap    defaults        0 0
	/dev/mapper/spvg-instlv     /sp/inst1           xfs     defaults,noauto    0 0
	/dev/mapper/spvg-actlv      /sp/actlog          xfs     defaults,noauto    0 0
	/dev/mapper/spvg-archlv     /sp/archlog         xfs     defaults,noauto    0 0
	/dev/mapper/spvg-db01lv     /sp/db/01           xfs     defaults,noauto    0 0
	/dev/mapper/spvg-db02lv     /sp/db/02           xfs     defaults,noauto    0 0
	/dev/mapper/spvg-dbblv      /sp/dbb             xfs     defaults,noauto    0 0
	```

1. Zmień grupę `spvg` tak, żeby używała `uname` jako `system_id`:

	```sh title="Dodanie system_id do istniejącej grupy"
	sudo vgchange --systemid "$(uname -n)" spvg
	```

	??? Example "Przykład"

		```sh hl_lines="6"
		$ sudo vgchange --systemid "$(uname -n)" spvg 
		  Volume group "spvg" successfully changed.
		$ sudo vgs -o+systemid
		  VG   #PV #LV #SN Attr   VSize    VFree System ID
		  rhel   1   3   0 wz--n-  <69.00g    0           
		  spvg   6   6   0 wz--n- <307.98g    0  sp-n1  
		```

1. Na wszelki wypadek zreboouj oba nody. 

## Dodawanie grupy-woluminow do drugiego węzła klastra