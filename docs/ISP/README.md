---
icon: material/tape-drive
---

# Spis mądrości Widmowo Obronych

* [Kury SQLowe](SQL.md) - rożne przydatne zapytania SQLowe.
* [Setup serwera SP na Linuxie](setup/index.md) - Przygtowanie hosta, instalacja binariów i setup instancji metodą "na piechotę".
* [Przydatne makra](macros/README.md) - głównie do rożnych statystyk 
* [Konfiguracja TDP4VE](clients/TDP4VE.md) - konfiguracja klienta Spectrum Protect for Virtual Environments.
* [Opcje](srv_opts.md), które warto sobie ustawić.
* [Disaster recovery](dr/index.md) - szeroko pojęte kwestie związane z odtwarzaniem bazy.


## Tips & tricks

### Kopiowanie polityk pomiędzy serwerami

Najprościej, mając zapiętą komunikację:

```
export policy * toserver=tsm-a preview=yes
```

To nie kopiuje definicji nodów, dlatego warto to zrobć tak:

```
export node dom=<domena>
```

Oczywiście istnieje mnustwo opcji eksportu od pojedynczych nodów po nody z domeny jak na :arrow_up: przykładzie.

### Czyszczenie `actlog` po przepełnieniu

Jeżeli TSM miał problem z backupem bazy i przepełnił sobie `ARCHLOG` a, co za tym idzie takżę i `ACTLOG`. O ile backup bazy obcina `ARCHLOG` o tyle w `ACTLOG` mogą pozostać śmieciowe logi, o których DB2 zapomina. Wspólnie z [Boberem](https://bob.ibm.com/) wyhalucynowałem takie rozwiązanie:

!!! Danger "Ważne"

	Zrób backup bazy. Nawet jeśli już wcześniej był zrobiony, żeby odsmiecić _archloga_.

1. Podłącz się do bazy `TSMDB1`.

	```bash
	db2 connect to TSMDB1
	```

1. Jako użyszkodnik instancji sprawdź jaki jest ostatni aktywny log bazy.

	```
	db2 get db cfg | grep "First active log"
	```

	!!! Example "Przykład"

		```bash
		$ db2 get db cfg | grep "First active log"
		 First active log file                                   = S0000790.LOG
		```

1. Wszystkie pliki o numerach niższych niż wskazany są du usunięcia. PRzejdź do katalogu z aktywnym strominiem logów, u mnie np.: `/sp/actlog/NODE0000/LOGSTREAM0000` i sprawdź, który w kolejności jest pierwszy aktywny plik:

	```bash
	$ ls -l | grep -n S0000790.LOG 
	189:-rw-------    1 tsminst1 tsminst1  536879104 Jul 12 13:18 S0000790.LOG
	```

1. Wyszło, że 189. ponieważ `ls` sortuje leksykograficznie, wszystkie pliki _powyżej_ są do wywalenia. Ale jak mawiał wujaszek Józef Wisarionowicz Dżugaszwili: "kontrola najwyższą formą zaufania", trzeba to sprawdzić. Piki z tej listy powinny być po prostu nieużywane:

	```bash
	ls -l | grep LOG | head -187 | tr -s " "  | cut -f 9 -d " " | while read d; do fuser -f $d; done
	```

	!!! Example "Przykład"

		Wydruk powinien pokazać, że żaden z plików nie jest w użyciu, to jest nie ma wyświetlonego PIDu procesu po nazwie pliku:

		```bash
		$ ls -l | grep LOG | head -187 | tr -s " "  | cut -f 9 -d " " | while read d; do fuser -f $d; done 
		S0000603.LOG: 
		S0000604.LOG: 
		S0000605.LOG: 
		S0000606.LOG: 
		S0000607.LOG: 
		S0000608.LOG: 
		S0000609.LOG: 
		[ ... ]
		```

1. Jak jest pusto, można ciąć :fingers_crossed: :

	```bash
	ls -l | grep LOG | head -187 | tr -s " "  | cut -f 9 -d " " | while read d; do rm $d; done
	```

1. Odlącz się od bazy:

	```bash
	db2 disconnect TSMDB1
	```
