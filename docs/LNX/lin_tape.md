# Konfiguracja `lin_tape`  i persistent names

Ta notka dotyczy TS4500. Ale będzie działać też dla TS4300. Tyle, że TS4300 nie ma CLI. :material-emoticon-sad:.  `TS4500CLI.jar` jest do pobrania z fix central. 

## Plan i założenia

- [x] Fajnie jest mieć konfigurację _persistent names_ i dodatkowych opcji modułu przed jego zbudowaniem i uruchomieniem.
- [x] TS4500 oszukuje na element numbers, dlatego jedynym sensownym identyfiaktrem napędu w tej bibliotece jest jego fizyczna lokalizacja określona przez `<FRAME><COLUMN><ROW>`, dlatego np dla napędu: 

	```
	F2, C4, R1,            CLEANING,        3592-60F,           Empty,       598D ,   00000786ED2A,  500507604422f50c,             257,   TSM_C
	```

	Będzie użyta nazwa: `/dev/lin_tape/drv_F2C4R2`

!!! Tip "Wskazówka"
	Jestem fanem jednolitego nazewnictwa napędów: od biblioteki, poprzez zoning, OSa, aż do TSMa. Np.:

	- Naped w bibliotece `X` jest w Frame 1, Column 2, Row 3: `F1C2R3`
	- Alias w zoningu będzie `lib_x_drvF1C2R3`
	- w OSie nazwę to: `/dev/lin_tape/drv_F1C2R3`
	- W Protekcie: `def drive lib_x drv_F1C2R3`

	Dzięki temu. przy jakichkolwiek kłopotach na którejś z tych warstw, wiem co monitorować w sąsiednich.


## Konfiguracja `lin_tape` w OSie

1. Pobierz informacje o interesujących Cię napędach z biblioteki

	```shell
	$ java -jar /home/marcinek/soft/tools/ts4500cli/TS4500CLI.jar   -u ja -p moje_hasło -ip TS4500-LLC1.mgmt  --viewDriveSummary | grep TSM_C | tr -d " " | cut -f 1-3,8 -d "," > ts4500_drives.csv

	$ cat ts4500_drives.csv
	F2,C4,R1,00000786ED2A
	F7,C4,R4,00000786ED9A
	F2,C1,R3,00000787319A
	F2,C4,R2,00000786ED4A
	F2,C4,R3,00000786ECBA
	F2,C4,R4,00000786EDEA
	F7,C1,R4,000007872F2A
	F7,C4,R1,00000786ED0A
	F7,C4,R2,00000786EC2A
	F7,C4,R3,00000786E8EA
	```

1. Wygeneruj wpisy do regułek `udev`: 

	```shell
	$ cat ts4500_drives.csv |sed 's/F\(.\),C\(.\),R\(.\),\(.*\)/KERNEL=="IBMtape\*\", ATTR{serial_num}=="\4", OWNER="spinst1", SYMLINK="lin_tape\/drv-f\1c\2r\3"/' > 98-ibm-lin_tape.rules
	$ cat 98-ibm-lin_tape.rules
	KERNEL=="IBMtape*", ATTR{serial_num}=="00000786ED2A", OWNER="spinst1", SYMLINK="lin_tape/drv-f2c4r1"
	KERNEL=="IBMtape*", ATTR{serial_num}=="00000786ED9A", OWNER="spinst1", SYMLINK="lin_tape/drv-f7c4r4"
	KERNEL=="IBMtape*", ATTR{serial_num}=="00000787319A", OWNER="spinst1", SYMLINK="lin_tape/drv-f2c1r3"
	KERNEL=="IBMtape*", ATTR{serial_num}=="00000786ED4A", OWNER="spinst1", SYMLINK="lin_tape/drv-f2c4r2"
	KERNEL=="IBMtape*", ATTR{serial_num}=="00000786ECBA", OWNER="spinst1", SYMLINK="lin_tape/drv-f2c4r3"
	KERNEL=="IBMtape*", ATTR{serial_num}=="00000786EDEA", OWNER="spinst1", SYMLINK="lin_tape/drv-f2c4r4"
	KERNEL=="IBMtape*", ATTR{serial_num}=="000007872F2A", OWNER="spinst1", SYMLINK="lin_tape/drv-f7c1r4"
	KERNEL=="IBMtape*", ATTR{serial_num}=="00000786ED0A", OWNER="spinst1", SYMLINK="lin_tape/drv-f7c4r1"
	KERNEL=="IBMtape*", ATTR{serial_num}=="00000786EC2A", OWNER="spinst1", SYMLINK="lin_tape/drv-f7c4r2"
	KERNEL=="IBMtape*", ATTR{serial_num}=="00000786E8EA", OWNER="spinst1", SYMLINK="lin_tape/drv-f7c4r3"
	```

1. Dopisz linijkę dla changera: 

	Chwilowo nie wiem jak wyciągnąć serial przez TS4500CLI, więc wziałem go z GUI "Properies" i pogrpowałem serial z `/proc/scsi/IBMchanger`:

	```shell
		  /dev/lin_tape/by-id ❯ cat /proc/scsi/IBMchanger | grep 78AC006
	0       03584L22    0000078AC0060403         lpfc                      19:0:1:1        Primary   
	4       03584L22    0000078AC0060403         lpfc                      23:0:1:1        Alternate 
	```

	Wygrepowany serial logicznej biblioteki wrzucam do pliku `98-ibm-lin_tape.rules` jak poniżej:

	```
	KERNEL=="IBMchanger*[0-9]", ATTR{serial_num}=="0000078AC0060403", OWNER="spinst1", SYMLINK="lin_tape/TSM_C-0000078AC0060403"
	```

1. Wrzuć plik konfiguracyjny dla CPF/DPF jeśli taka licencja została kupiona:

	```shell
	$ cat /etc/modprobe.d/lin_tape.conf 
	options lin_tape tape_reserve_type=persistent
	options lin_tape alternate_pathing=1
	```

## Instalacja i budowanie drivera

_Lin_tape_ przychodzi w dwóch paczkach: lin_tape (src RPM) do przebudowania za każdym razem gdy zmienisz kernel :man_facepalming:. (1)
{ .annotate }

1. Może kiedyś pokuszę się o zrobienie adkmoda :shrug: ?

Instalacja i kompilacja drivera:

1. Sciągnij najświeższy driver z [IBM Fix Central](https://ibm.com/support/fixcentral).

1. Zainstaluj paczki potrzebne do budowania kernela:

	!!! Warning inline end "Uwaga"
		`dnf` instaluje paczkę `kernel-devel` najnowszą jaką znajdzie, więc jesłi jesteś do tyłu z aktualizacjami, to zainstalowany _devel_ będzie nowszy niż działające jądro i budowa `lin_tape` się nie powiedzie. 

		Zaktualizuj jądro, albo ściągnij `kernel-devel` w wersji pasującej do Twojego jajka.

	- kernel-devel
	- make
	- gcc
	- rpm-build 

	```sh title="Instalacja pakietów do budowania modułów jądra"
	sudo dnf install  rpm-build kernel-devel make gcc
	```

1. Przebuduj pakiet `lin_tape-*src.rpm`:

	```sh title="Budowanie modułu lin_tape"
	rpmbuild --rebuild lin_tape-3.0.72-1.src.rpm
	```

	!!! Note "Zwróć uwagę"
		Komenda `rpmbuild` umieszcza zbudowane pakiety w `$HOME/rpmbuild/RPMS/$ARCH/`.

		Dla porządku, możesz przenieść tam też pakiet `lin_taped-*.rpm`


1. Zainstaluj obie paczki.

	```sh title="Instalacja modułu lin_tape"
	sudo dnf install lin_tape-3.0.72-1.x86_64.rpm lin_taped-3.0.72-rhel9.x86_64.rpm
	```

1. Zweryfikuj, czy moduł się zładował i czy regółki _udev_ połapały się w napędach:

	```sh hl_lines="1" title="Weryfikacja instalacji lin_tape"
	$ ls -l /dev/lin_tape/
	total 0
	drwxr-xr-x. 2 root root 740 Mar 31 21:26 by-id
	lrwxrwxrwx. 1 root root  13 Mar 31 21:26 drv-F2C1R2 -> ../IBMtape25n
	lrwxrwxrwx. 1 root root  12 Mar 31 21:26 drv-F2C3R1 -> ../IBMtape2n
	lrwxrwxrwx. 1 root root  13 Mar 31 21:26 drv-F2C3R2 -> ../IBMtape28n
	lrwxrwxrwx. 1 root root  12 Mar 31 21:26 drv-F2C3R3 -> ../IBMtape3n
	lrwxrwxrwx. 1 root root  13 Mar 31 21:26 drv-F2C3R4 -> ../IBMtape27n
	lrwxrwxrwx. 1 root root  12 Mar 31 21:26 drv-F7C1R1 -> ../IBMtape4n
	lrwxrwxrwx. 1 root root  12 Mar 31 21:26 drv-F7C3R1 -> ../IBMtape1n
	lrwxrwxrwx. 1 root root  13 Mar 31 21:26 drv-F7C3R2 -> ../IBMtape26n
	lrwxrwxrwx. 1 root root  12 Mar 31 21:26 drv-F7C3R3 -> ../IBMtape0n
	lrwxrwxrwx. 1 root root  13 Mar 31 21:26 drv-F7C3R4 -> ../IBMtape24n
	lrwxrwxrwx. 1 root root  14 Mar 31 21:26 TSM_B-0000078AC0060402 -> ../IBMchanger6
	```

## Instalacja w Storage Protect

1. Wygeneruj definicję napędów:

	```shell
	$ cat ts4500_drives.csv | sed 's/F\(.\),C\(.\),R\(.\),\(.*\)/define drive TS45k-C drv-f\1c\2r\3' > def_drives.mac
	$ cat def_drives.mac
	define drive TS45k-C drv-f2c4r1
	define drive TS45k-C drv-f7c4r4
	define drive TS45k-C drv-f2c1r3
	define drive TS45k-C drv-f2c4r2
	define drive TS45k-C drv-f2c4r3
	define drive TS45k-C drv-f2c4r4
	define drive TS45k-C drv-f7c1r4
	define drive TS45k-C drv-f7c4r1
	define drive TS45k-C drv-f7c4r2
	define drive TS45k-C drv-f7c4r3
	```
1. Wygeneruj definicje sćieżek do napędów. Podstaw swoją nazwę serwer i biblioteki:

	```shell
	$ cat ts4500_drives.csv | sed 's/F\(.\),C\(.\),R\(.\),\(.*\)/define path TSM-SERWER-CD-HA  drv-f\1c\2r\3 srct=server destt=drive libr=ts45k-c device=\/dev\/lin_tape\/drv-f\1c\2r\3/'  > def_paths.mac
	```

1. Zdefiniuj bibliotekę:

	Nazwę urządenia w ścieżce wpisujesz taką, jaką jest w regułce `udev'a`

	```
	def libr ts45k-c libt=scsi autolabel=yes
	def path TSM-SERWER-CD-HA ts45k-c srct=server destt=libr device=/dev/lin_tape/TSM_C-0000078AC0060403
	```

1. Puść makro definiowania napędów `def_drives.mac`

	```shell
	$ dsmadmc -se=tsm-c.pcss -id=xxx -pa=S3cr3tP@$$ -itemcommit macro def_drives.mac      
	IBM Storage Protect
	Interfejs administracyjny wiersza poleceń - Wersja 8, Wydanie 1, Poziom 24.0
	(c) Copyright IBM Corp. 1990, 2024.
	(c) Copyright IBM Corp. i inne podmioty 1990, 2024. Wszelkie prawa zastrzeżone.

	Sesja z serwerem uruchomiona TSM-SERWER-CD-HA: Linux/x86_64
	  Wersja serwera: 8, wydanie: 1, poziom: 24.000
	  Data/godzina serwera: 01.12.2024 13:01:56  Ostatni dostęp: 01.12.2024 13:01:51

	ANS8000I Komenda serwera: 'define drive TS45k-C drv-f2c4r1'.
	ANR8404I Drive DRV-F2C4R1 defined in library TS45K-C.
	ANS8000I Komenda serwera: 'define drive TS45k-C drv-f7c4r4'.
	ANR8404I Drive DRV-F7C4R4 defined in library TS45K-C.
	ANS8000I Komenda serwera: 'define drive TS45k-C drv-f2c1r3'.
	ANR8404I Drive DRV-F2C1R3 defined in library TS45K-C.
	ANS8000I Komenda serwera: 'define drive TS45k-C drv-f2c4r2'.
	ANR8404I Drive DRV-F2C4R2 defined in library TS45K-C.
	ANS8000I Komenda serwera: 'define drive TS45k-C drv-f2c4r3'.
	ANR8404I Drive DRV-F2C4R3 defined in library TS45K-C.
	ANS8000I Komenda serwera: 'define drive TS45k-C drv-f2c4r4'.
	ANR8404I Drive DRV-F2C4R4 defined in library TS45K-C.
	ANS8000I Komenda serwera: 'define drive TS45k-C drv-f7c1r4'.
	ANR8404I Drive DRV-F7C1R4 defined in library TS45K-C.
	ANS8000I Komenda serwera: 'define drive TS45k-C drv-f7c4r1'.
	ANR8404I Drive DRV-F7C4R1 defined in library TS45K-C.
	ANS8000I Komenda serwera: 'define drive TS45k-C drv-f7c4r2'.
	ANR8404I Drive DRV-F7C4R2 defined in library TS45K-C.
	ANS8000I Komenda serwera: 'define drive TS45k-C drv-f7c4r3'.
	ANR8404I Drive DRV-F7C4R3 defined in library TS45K-C.

	```

1. Puść makro od śćieżek:

	```shell
	dsmadmc -se=tsm-c.pcss -id=xxx -pa=S3cr3tP@$$ -itemcommit macro def_paths.mac                                                                        ✔  13:07:55  ▓▒░
	IBM Storage Protect
	Interfejs administracyjny wiersza poleceń - Wersja 8, Wydanie 1, Poziom 24.0
	(c) Copyright IBM Corp. 1990, 2024.
	(c) Copyright IBM Corp. i inne podmioty 1990, 2024. Wszelkie prawa zastrzeżone.

	Sesja z serwerem uruchomiona TSM-SERWER-CD-HA: Linux/x86_64
	  Wersja serwera: 8, wydanie: 1, poziom: 24.000
	  Data/godzina serwera: 01.12.2024 13:09:09  Ostatni dostęp: 01.12.2024 13:01:56

	ANS8000I Komenda serwera: 'define path TSM-SERWER-CD-HA  drv-f2c4r1 srct=server destt=drive libr=ts45k-c device=/dev/lin_tape/drv-f2c4r1'.
	ANR1720I A path from TSM-SERWER-CD-HA to TS45K-C DRV-F2C4R1 has been defined.
	ANS8000I Komenda serwera: 'define path TSM-SERWER-CD-HA  drv-f7c4r4 srct=server destt=drive libr=ts45k-c device=/dev/lin_tape/drv-f7c4r4'.
	ANR1720I A path from TSM-SERWER-CD-HA to TS45K-C DRV-F7C4R4 has been defined.
	ANS8000I Komenda serwera: 'define path TSM-SERWER-CD-HA  drv-f2c1r3 srct=server destt=drive libr=ts45k-c device=/dev/lin_tape/drv-f2c1r3'.
	ANR1720I A path from TSM-SERWER-CD-HA to TS45K-C DRV-F2C1R3 has been defined.
	ANS8000I Komenda serwera: 'define path TSM-SERWER-CD-HA  drv-f2c4r2 srct=server destt=drive libr=ts45k-c device=/dev/lin_tape/drv-f2c4r2'.
	ANR1720I A path from TSM-SERWER-CD-HA to TS45K-C DRV-F2C4R2 has been defined.
	ANS8000I Komenda serwera: 'define path TSM-SERWER-CD-HA  drv-f2c4r3 srct=server destt=drive libr=ts45k-c device=/dev/lin_tape/drv-f2c4r3'.
	ANR1720I A path from TSM-SERWER-CD-HA to TS45K-C DRV-F2C4R3 has been defined.
	ANS8000I Komenda serwera: 'define path TSM-SERWER-CD-HA  drv-f2c4r4 srct=server destt=drive libr=ts45k-c device=/dev/lin_tape/drv-f2c4r4'.
	ANR1720I A path from TSM-SERWER-CD-HA to TS45K-C DRV-F2C4R4 has been defined.
	ANS8000I Komenda serwera: 'define path TSM-SERWER-CD-HA  drv-f7c1r4 srct=server destt=drive libr=ts45k-c device=/dev/lin_tape/drv-f7c1r4'.
	ANR1720I A path from TSM-SERWER-CD-HA to TS45K-C DRV-F7C1R4 has been defined.
	ANS8000I Komenda serwera: 'define path TSM-SERWER-CD-HA  drv-f7c4r1 srct=server destt=drive libr=ts45k-c device=/dev/lin_tape/drv-f7c4r1'.
	ANR1720I A path from TSM-SERWER-CD-HA to TS45K-C DRV-F7C4R1 has been defined.
	ANS8000I Komenda serwera: 'define path TSM-SERWER-CD-HA  drv-f7c4r2 srct=server destt=drive libr=ts45k-c device=/dev/lin_tape/drv-f7c4r2'.
	ANR1720I A path from TSM-SERWER-CD-HA to TS45K-C DRV-F7C4R2 has been defined.
	ANS8000I Komenda serwera: 'define path TSM-SERWER-CD-HA  drv-f7c4r3 srct=server destt=drive libr=ts45k-c device=/dev/lin_tape/drv-f7c4r3'.
	ANR1720I A path from TSM-SERWER-CD-HA to TS45K-C DRV-F7C4R3 has been defined.

	ANS8002I Najwyższy kod powrotu wynosił 0.
	```
