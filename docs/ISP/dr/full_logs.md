---
icon: octicons/log-16
---

# Przepełniony ACTLOG i ARCHLOG

Może  to nie jest _disaster_ ale _recovery_ bywa upierdliwe, bo serwer stoi. I nie chce wstać. Dzieje się tak np wtedy, gdzy wwznowi się replikację po dłuższej przerwie i ma dużo do roboty na tablicach "chuknów". Jest to o tyle słabe, że nie widać tych działań jako procesu. Przykładowy objaw:

```sh hl_lines="15-16"
# df -h
Filesystem                    Size  Used Avail Use% Mounted on
devtmpfs                      4.0M     0  4.0M   0% /dev
tmpfs                         126G  4.0K  126G   1% /dev/shm
tmpfs                          51G  105M   51G   1% /run
efivarfs                      256K   90K  162K  36% /sys/firmware/efi/efivars
/dev/mapper/rhel-root          70G   18G   53G  25% /
/dev/sdb2                     960M  360M  601M  38% /boot
/dev/mapper/rhel-home         500G   21G  479G   5% /home
/dev/sdb1                     599M  7.1M  592M   2% /boot/efi
tmpfs                          26G   12K   26G   1% /run/user/0
/dev/mapper/instvg-inst1lv     30G  507M   30G   2% /tsm/tsminst1
/dev/mapper/instvg-db01lv      64G   31G   34G  48% /tsm/db/01
/dev/mapper/instvg-db02lv      64G   31G   34G  48% /tsm/db/02
/dev/mapper/instvg-actlv      160G  160G  339M 100% /tsm/actlog
/dev/mapper/datavg-archlv     256G  256G  337M 100% /tsm/archlog
/dev/mapper/datavg-dc01lv     1.0T  702G  323G  69% /tsm/dc01/01
/dev/mapper/datavg-dc02lv     1.0T  691G  334G  68% /tsm/dc01/02
/dev/mapper/datavg-dbblv      256G  120G  137G  47% /tsm/dbb
/dev/mapper/instvg-db03lv      64G   31G   34G  48% /tsm/db/03
/dev/mapper/instvg-db04lv      64G   31G   34G  48% /tsm/db/04
```

W zależności od warunków jest kilka wyjść. Zaczynam od najprostszego:

## Powiększenie ARCHLOG

Wystarczy powiększyć filesystem wskazany w `dsmserv.opt` jako `ARCHLOGDIR`. 

!!! Note "Dlaczenie nie `ARCHFAILOVERLOGDIRECTORY`?"

    To zależy. W przypadku crashu z powodu porządków w tablicach deduplikacji, serwer będzie crashował szybciej niż zdąży przewalć logi na failover. Przynajmniej na werjis 8.2.2, gdzie mnie to ugryzło.
    Jeżeli przepełnienie było spowodowane czymś innym, to moźe się udać :man_shrugging:.

W przypadku powyżej trzeba:

1. Powiekszyć filesystem `/dev/mapper/datavg-archlv` tak, żeby mógł zarchwizować zalegające logi z `/tsm/actlog`.

    ```bash title="Dodanie 100 GiB do Archloga"
    lvresize -L +100G /dev/instvg/archlv  -r
    ```

1. Żeby Uruchomić serwer w trybie `maintenance`, trzeba znać usera instancji i katalog instancji. Stań się właścicielem instancji:

    ```
    su - tsminst1
    ```
2. Wystartuj w trybie `maintenance`:

    ```bash title="Start w trybie maintnenance"
    dsmserv -i /katalog/instancji maintenance
    ```



## Backup z poziomu DB2

Czasem nie ma jak powiększyć `ARCHLOG`. Wtedy można podłączyć np nowy dysk, udział NFSowy, albo na chwilę użyć jakigoś istniejącego, wystarczająco dużego filesystemu, żeby zrobić full backup bazy DB2 z poziomu samej bazy. Oczywiście jest na to oficjalna [procedura](https://www.ibm.com/support/pages/archive-log-directories-are-full-and-server-will-not-start).

1. Znajdź sobie jakieś tymczasowe miejsce na backup bazy. U mnie to `/tsm/DB2_Arch/crash_rec`: 

    ```bash
    mkdir /tsm/DB2_Arch/crash_rec
    chown tsminst1:tsmsrvrs /tsm/DB2_Arch/crash_rec/
    ```

1. Upewnij się, że serwer leży i kwiczy. Stań się userem instancji (w tym przykładzie `tsminst1`) wystartuj database managera:

    ```bash
    su - tsminst1
    db2start
    ```

1. Zrób backup bazy do tymczasowego katalogu:

    ```bash
     db2 backup db tsmdb1 to /tsm/DB2_Arch/crash_rec
    ```

    !!! Note "Podwójna ścieżka"

        Jak się poda kilka katalogów, albo np ten sam, tylko kilka razy, wtedy DB2 użyje tylu wątków w backupie ile dostanie katalogów.

        ```bash
        db2 backup db tsmdb1 to /tsm/DB2_Arch/crash_rec,/tsm/DB2_Arch/crash_rec
        ```

        W przypadku gdzy filesystemy logów są "pod korek" nie polecam jednak tego podejścia. Do wielowątkowego zapisu, DB2 wydaje się potrzebować... przestrzeni LOGów :man_facepalming:.

1. Po skończonym backupie, który powinien wyglądać tak:

    ```bash
    $ db2 backup db tsmdb1 to /tsm/DB2_Arch/crash_rec

    Backup successful. The timestamp for this backup image is : 20261005202930
    ```

    Sprawdź zajętość filesystemów:

    ```bash hl_lines="15-16"
    # df -h
    Filesystem                    Size  Used Avail Use% Mounted on
    devtmpfs                      4.0M     0  4.0M   0% /dev
    tmpfs                         126G   16K  126G   1% /dev/shm
    tmpfs                          51G  105M   51G   1% /run
    efivarfs                      256K   90K  162K  36% /sys/firmware/efi/efivars
    /dev/mapper/rhel-root          70G   18G   53G  25% /
    /dev/sdb2                     960M  360M  601M  38% /boot
    /dev/mapper/rhel-home         500G   21G  479G   5% /home
    /dev/sdb1                     599M  7.1M  592M   2% /boot/efi
    tmpfs                          26G   12K   26G   1% /run/user/0
    /dev/mapper/instvg-inst1lv     30G  505M   30G   2% /tsm/tsminst1
    /dev/mapper/instvg-db01lv      64G   31G   34G  48% /tsm/db/01
    /dev/mapper/instvg-db02lv      64G   31G   34G  48% /tsm/db/02
    /dev/mapper/instvg-actlv      165G  151G   15G  92% /tsm/actlog
    /dev/mapper/datavg-archlv     266G  2.9G  264G   2% /tsm/archlog
    /dev/mapper/datavg-dc01lv     1.0T  702G  323G  69% /tsm/dc01/01
    /dev/mapper/datavg-dc02lv     1.0T  691G  334G  68% /tsm/dc01/02
    /dev/mapper/datavg-dbblv      256G  120G  137G  47% /tsm/dbb
    /dev/mapper/instvg-db03lv      64G   31G   34G  48% /tsm/db/03
    /dev/mapper/instvg-db04lv      64G   31G   34G  48% /tsm/db/04
    /dev/mapper/datavg-db2archlv 1000G  128G  872G  13% /tsm/DB2_Arch
    ```

    Jest prawie dobrze. `ARCHLOG` jest orpóżniony, ale w  `ACTLOG` są śmieci. Skąd to wiadomo, skoro `ACTLOG` jest pre-alokowany?
    Bo dobrze postawiony TSM na zawsze około 20% powietrz w tym filesystemie. 

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

    !!! Danger "Ważne"

        Warto poczekać kilka|naście|dziesiąt minut, bo DB2 coś tam sobie jeszcze sprawdza we wcześniejszych logach i potrafi je na chwilę otwirać. 
        Na poniższym wydruku `First active log` to `S0007669.LOG` a widać, że otworzył na chwilę (jak się prare razy wykona to polecenie, to widać, żę wcześniejsze logi się zmieniają) wcześniejszy log. 
        Z kasowaniem trzeba zaczekać aż skończy.

        ```bash hl_lines="2"
        [tsminst1@spbg01 LOGSTREAM0000]$ ls -l | grep LOG | head -312 | tr -s " "  | cut -f 9 -d " " | while read d; do fuser -f $d; done
        /tsm/actlog/NODE0000/LOGSTREAM0000/S0007666.LOG: 4072163
        /tsm/actlog/NODE0000/LOGSTREAM0000/S0007669.LOG: 4072163
        /tsm/actlog/NODE0000/LOGSTREAM0000/S0007670.LOG: 4072163
        ```

1. Jak jest pusto, można ciąć :fingers_crossed: :

	```bash
	ls -l | grep LOG | head -187 | tr -s " "  | cut -f 9 -d " " | while read d; do rm $d; done
	```

1. Odlącz się od bazy:

	```bash
	db2 disconnect TSMDB1
	```