---
icon: simple/redhat
---

# Instalacja RedHat :simple-redhat:


## Kickstart z http

Szczególnie przydatna, gdy muszę "nakocić" kilka podobnych maszyn. 


Wymagania:

- [x] Serwer http do podawania plików _kickstart_
- [x] Plik _Kickstart_ odpowiedni dla Twojego :simple-redhat:


!!! Warning
	Red Hat wprowdział sporo zmian pomiędzy 9.7 -> 9.8 oraz 10.1 -> 10.2 na tle _Post Quatnum Cryptography_, np w sposobie szyfrowania haseł. Dlatego _kickstarty_ mogą nie pasować.

=== "RH 10"

	``` title="Przykładowy plik ks.cfg dla RH10"
	--8<-- "scripts/rh10-ks.cfg"
	```

=== "RH 9"

	``` title="Przykładowy plik ks.cfg dla RH9"
	--8<-- "scripts/rh9-ks.cfg"
	```

Przepis:

1. Wygeneruj sobie hasło/hasła i wstaw je do pliku _kickstart_. Red Hat 10 używa _yescrypt_. 
	Dla starszych możliwe, że trzeba będzie użyć _SHA512_ albo nawet _SHA256_:

	=== "RH10 (yescrypt)"

		``` bash title="Generowanie hasha hasła"
		$ mkpasswd -m yescrypt
		Hasło: 
		$y$j9T$boglaVj1.UyxOG5HBVUSd.$T9is4YpudJOh7Ssl0hkw7.W7WUq9EJBOCWthV4naCkA
		```
	
	=== "RH9 (SHA512)"

		``` bash title="Generowanie hasha hasła"
		$ mkpasswd -m sha512crypt
		Hasło: 
		$y$j9T$boglaVj1.UyxOG5HBVUSd.$T9is4YpudJOh7Ssl0hkw7.W7WUq9EJBOCWthV4naCkA
		```

	!!! Note

		Możesz nie trudzić się nad tym hasłem-przykładem. Nigdzie tego go nie użyłem :wink:.

1. Zabootować LPAR/pudło/vmkę z CD.

	!!! Tip
		Powera zabootować do SMS a potem czary mary z _Select/install boot device_.

1. W Menu startowym wybrać opcję edycji wiersza poleceń bootloadera.

	``` hl_lines="4"
		                               GRUB version 2.12

	 +----------------------------------------------------------------------------+
	 |*Install Red Hat Enterprise Linux 10.1 (64-bit kernel)                      | 
	 | Test this media & install Red Hat Enterprise Linux 10.1  (64-bit kernel)   |
	 | Install Red Hat Enterprise Linux 10.1 (64-bit kernel) in FIPS mode         |
	 | Rescue a Red Hat Enterprise Linux system (64-bit kernel)                   |
	 | Other options...                                                           |
	 |                                                                            |
	 |                                                                            |
	 |                                                                            |
	 |                                                                            |
	 |                                                                            |
	 |                                                                            |
	 |                                                                            | 
	 +----------------------------------------------------------------------------+

	      Use the ^ and v keys to select which entry is highlighted.          
	      Press enter to boot the selected OS, `e' to edit the commands       
	      before booting or `c' for a command-line.                           
	                                                     
	```

1. Dopisać 

	```
	inst.ks=http://10.10.13.14/data/ks/gpfs04.cfg ip=10.10.13.34::10.10.10.1:255.255.0.0::env2:none nameserver=10.10.13.14 inst.repo=cdrom:/dev/sr0 
	```

	do linijki z kernelem:


	``` hl_lines="6-8 19"
		                               GRUB version 2.12

	 +----------------------------------------------------------------------------+
	 |setparams 'Install Red Hat Enterprise Linux 10.1 (64-bit kernel)'           | 
	 |                                                                            |
	 |      linux /ppc/ppc64/vmlinuz inst.stage2=hd:LABEL=RHEL-10-1-BaseOS-ppc64l\|
	 |e ro inst.ks=http://10.10.13.14/data/ks/gpfs03.cfg ip=10.10.13.33::10.10.10\|
	 |.1:255.255.0.0::env2:none nameserver=10.10.13.14 inst.repo=cdrom:/dev/sr0   |
	 |      initrd /ppc/ppc64/initrd.img                                          |
	 |                                                                            |
	 |                                                                            |
	 |                                                                            |
	 |                                                                            |
	 |                                                                            |
	 |                                                                            | 
	 +----------------------------------------------------------------------------+

	      Minimum Emacs-like screen editing is supported. TAB lists           
	      completions. Press Ctrl-x or F10 to boot, Ctrl-c or F2 for          
	      a command-line or ESC to discard edits and return to the GRUB menu.
	```

1. Pstryknąć Ctrl-x i iśc na kawę. 

## Instalator graficzny na :IBM-Power: IBM Power

!!! Bug

	Dopiszę jak będę miał czas.