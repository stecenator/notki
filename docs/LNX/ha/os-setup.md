---
icon: simple/linux
---

# Konfiguracja OSów pod klaster

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

	!!! Danger "Uwaga"
		Tu się coś pozmieniało, od czasu gdy to konfigurowałem na RH7. Na raie pomijam ten fragment. Prawdopodobnie to się konfiguruje teraz "per-grupa", przy dodawaniu VG do klastra.

1. Upewnij się, że plik startujący instancję ISP jest na obu nodach. Instancja __nie może strtować automatycznie!!__