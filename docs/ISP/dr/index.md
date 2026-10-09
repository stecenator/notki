---
icon: fontawesome/solid/explosion
---

# Disaster recovery

Czyli szeroko rozumiane zbieranie TSMa z podłogi. 

## Odtwarznie bazy

!!! Info "Założenia"

    - Odtwarzanie bazy odbywa się na tej samej maszynie.
    - ARCHLOG nie został utracony

## Odtwarzanie bazy do punktu w czasie

## Odtwarzanie bazy bez `volhist` 

Siłą rzeczy też do punktu w czasie. Podstawą tej proceury jest [ten dokument](https://www.ibm.com/support/pages/rebuild-missing-volume-history-file-file-database-restore).


Dlaczego w ogóle może zejść potrzeba takiego odtwarzania? Ano przydarzyło mi się, że przez nieuwagę usunąłem sobie katalog instancji _Protecta_ przy próbie reinstalacji OSa. Myślałem, że wzystko jest w oddzielnych volume grupach, i że po ponownym zainstalowaniu OSa zrobię [ponowny import instancji](#import-istniejacej-instancji), z grupy `spvg` ale nie zauważyłem, że katalog instancji nie jest filesystemem tylko katalogiem w `/` fiesystemu :facepalm:.

### Stan początkowy

Mam właściwie wszystkie filesystemy i pewnie gdybym pamiętał jak były pomontowane i miał katalog instancji (`DFTDBPATH`) to mógłbym go skatalogować i po prostu działać. Ale nie mam :shrug:. Mam za to taką strukturę filesystemów/katalogów:

``` title="Struktura montowania /sp"
/sp/
├── actlog
├── archlog
├── db01
├── db02
├── db03
├── db04
├── dbb
│   └── upd
├── dp01
│   ├── 00
│   ├── 01
│   ├── 02
│   └── 03
└── spinst1
```

Tak jak wspomniałem, nie mam pomysłu jak dobrać się do bazy rozłożonej w tatalogach `/sp/db*` więc sformatowałem te filesytemy (i przy okazji zmieniłem ext4 na XFS). Podobonie z `/sp/a*log`. Zatem jedyna  pozostałość "starego" TSMa jaką mam, to backup bazy w `/sp/dbb` i pamięc, że _devclass_ nazywała się `DBB`. Resztę muszę zrobić od nowa.

### Nowa instancja

Żeby odtwozyć bazę, potrzebna jest nowa instancja. Można ją zrobić tekstowo, np. przy pomocy [tej procedury](../setup/setup_instance.md), albo pójś na łatwiznę i jesli masz X11, to odpalić :material-wizard-hat: wizarda `/opt/tivoli/tsm/server/bin/dsmicfgx` jako `root`.

### Plik `devconf.dat` 

Jeśli go nie ma, trzeba go stworzyć. Wystarczy minimalny, to jest taki, który wskazuje na devclassę plikową przechowującą bazę. Mój tworzę tak (jako użytkownik instancji):

```bash
cat > /sp/spinst1/devconf.dat << EOF
DEFINE DEVCLASS DBB DEVT=FILE FORMAT=DRIVE SHARE=NO MAXCAP=1048576K MOUNTL=2 DIR=/sp/dbb
EOF
```

### Plik `volhist.dat`

Utworzenie tego pliku jest torchę trudniejsze, bo parę rzeczy trzeba zgadnąć. Np czas utworzenia backupu i numery sekwencyjne woluminów. 

``` title="Szablon volhost.dat"
 Operation Date/Time:   2026/09/04 05:00:10
 
 Volume Type:  BACKUPFULL
 Volume Name:  "/sp/dbb/88490810.DBV"
 Backup Series:        1622
 Backup Op:               0
 Volume Seq:         100001
 Device Class Name:  DBB
************************************************** 
```

Istotne pola:

- `Operation Date/Time` - To trzeba zgadnąć, np na podstawie daty utorzenia pliku.
- `Volume Type` - Pewie będzie `BACKUPFULL`. Czasem `SNAPSHOT`.
- `Volume Name` - ścieżka do pliku. __Uwaga:__ Protect wpisuje tu nazwy plikó wwielkimi literami, ale w filesystemie to są małe litery.
- `Backup Series` - Może być ustawione na cokolwiek. Byle wspólne dla woluminów należących do tej samej serii.
- `Backup Op` - `0` dla pełnego backupu.
- `Volume Seq` - To trzeba zgadnąć. Np z rożnic w datach modyfikacji plików w `/sp/dbb`. Najstarszy numerujemy od `100001`, inkrementacja co `1`.

#### Odtwarzanie bazy

1. Sprawdź daty plików backupu bazy:

    ```bash hl_lines="5-6"
    [spinst1@sp-1 spinst1]$ ls -la /sp/dbb/
    total 7047436
    drwxr-xr-x.  3 spinst1 spinst1         57 Jun 28 06:02 .
    drwxr-xr-x. 10 spinst1 spinst1        109 Jul 13 12:36 ..
    -rw-------.  1 spinst1 spinst1 3574595823 Jun 28 06:01 82619209.dbv
    -rw-------.  1 spinst1 spinst1 3641968469 Jun 28 06:01 82619210.dbv
    ```

    Jak widać, data modyfikacji jest taka sama. Ale nazwy plików mają kolejne numerki, co sugeruje backup idący dwoma wątkami. 
    Mam zatem kolejność i datę... zakończenia backupu. Potrzebna jest jednak data jego rozpoczęcia, ale o tym później :smile:. 

1. Utwórz pierszą wersjię `volhist.dat`:

    ``` hl_lines="1 4 7 10 13 16"
     Operation Date/Time:   2026/06/28 06:01:00
    
    Volume Type:  BACKUPFULL
    Volume Name:  "/sp/dbb/82619209.DBV"
    Backup Series:        1622
    Backup Op:               0
    Volume Seq:         100001
    Device Class Name:  DBB
    ************************************************** 
    Operation Date/Time:   2026/06/28 06:01:00
    
    Volume Type:  BACKUPFULL
    Volume Name:  "/sp/dbb/82619210.DBV"
    Backup Series:        1622
    Backup Op:               0
    Volume Seq:         100002
    Device Class Name:  DBB
    ************************************************** 
    ```

1. Podłóż święte pliki do `dsmserv.opt`

``` hl_lines="7-8" title="dsmserv.opt po dopisani świętych plików"
COMMmethod TCPIP
TCPPort 1500

ACTIVELOGSize               65536 
ACTIVELOGDirectory          /sp/actlog 
ARCHLOGDirectory            /sp/archlog 
DEVCONFIG                   /sp/spinst1/devconf.dat
VOLUMEHISTORY               /sp/spinst1/volhist.dat
```

1. Pierwsza próba odtwarzania, która się wyłoży, ale pokaże czego brakuje do rzeczywistego odtworzenia. Jako user instancji, w katalogu instancji:

    ```bash
    dsmserv -i /sp/spinst1 restore db todate=06/28/2026
    ```

    Output, który jaki `Backup Series` należy ustalić. Szukam błędu __ANR4606E__:

    ```bash hl_lines="1 24 34"
    [spinst1@sp-1 spinst1]$ dsmserv -i /sp/spinst1 restore db todate=06/28/2026
    ANR7800I DSMSERV generated at 10:53:50 on Mar 19 2026.

    IBM Storage Protect for Linux/ppc64le
    Version 8, Release 2, Level 1.000

    Licensed Materials - Property of IBM

    (C) Copyright IBM Corporation 1990, 2026.
    All rights reserved.
    U.S. Government Users Restricted Rights - Use, duplication or disclosure
    restricted by GSA ADP Schedule Contract with IBM Corporation.

    ANR7801I Subsystem process ID is 2570443.
    ANR0900I Processing options file /sp/spinst1/dsmserv.opt.
    ANR0010W Unable to open message catalog for language en_US.UTF-8. The default language message catalog will be used.
    ANR7814I Using instance directory /sp/spinst1.
    ANR3339I Default Label in key data base is TSM Server SelfSigned SHA Key. 
    ANR4726I The ICC support module has been loaded.
    ANR1637W Error (Write error) occurred initializing the server machine GUID.
    ANR8598I Outbound SSL Services were loaded.
    ANR8230I TCP/IP Version 6 driver ready for connection with clients on port 1500.
    ANR8200I TCP/IP Version 4 driver ready for connection with clients on port 1500.
    Enter the password to restore the master encryption key (or press Enter to skip): 
    ANR4634I Starting point-in-time database restore to date 06/28/2026 11:59:59 PM.
    ANR4591I Selected backup series 1622 from 06/28/2026 and 06:01:00 AM as best candidate available for restore database processing.
    ANR4592I Restore database backup series 1622 includes eligible operation 0 with volume /sp/dbb/82619209.DBV having sequence 100001 and
    using device class DBB.
    ANR4592I Restore database backup series 1622 includes eligible operation 0 with volume /sp/dbb/82619210.DBV having sequence 100002 and
    using device class DBB.
    ANR4598I Validating database backup information for selected backup series 1622 and operation 0 using volume /sp/dbb/82619210.DBV.
    ANR8340I FILE volume /sp/dbb/82619210.DBV mounted.
    ANR1363I Input volume /sp/dbb/82619210.DBV opened (sequence number 1).
    ANR4606E Restore database volume header backup series number 1015 does not match the expected backup series number of 1622. This volume
    cannot be used to restore the database.
    ANR1364I Input volume /sp/dbb/82619210.DBV closed.
    ANR4602E No volumes found for TODATE 06/28/2026 11:59:59 PM.
    ```

1. Zmień `Backup Series` na wskzaną wartość, w tym wypadku `1015` i ponów próbę odtwarznia. Ta próba też się wywali, tym razem szukaj komunikatu __ANR4614E__.

    ```bash hl_lines="34-35" title="Odtwarzanie z serii 1015"
    [spinst1@sp-1 spinst1]$ dsmserv -i /sp/spinst1 restore db todate=06/28/2026
    ANR7800I DSMSERV generated at 10:53:50 on Mar 19 2026.

    IBM Storage Protect for Linux/ppc64le
    Version 8, Release 2, Level 1.000

    Licensed Materials - Property of IBM

    (C) Copyright IBM Corporation 1990, 2026.
    All rights reserved.
    U.S. Government Users Restricted Rights - Use, duplication or disclosure
    restricted by GSA ADP Schedule Contract with IBM Corporation.

    ANR7801I Subsystem process ID is 2587622.
    ANR0900I Processing options file /sp/spinst1/dsmserv.opt.
    ANR0010W Unable to open message catalog for language en_US.UTF-8. The default language message catalog will be used.
    ANR7814I Using instance directory /sp/spinst1.
    ANR3339I Default Label in key data base is TSM Server SelfSigned SHA Key. 
    ANR4726I The ICC support module has been loaded.
    ANR1637W Error (Write error) occurred initializing the server machine GUID.
    ANR8598I Outbound SSL Services were loaded.
    ANR8230I TCP/IP Version 6 driver ready for connection with clients on port 1500.
    ANR8200I TCP/IP Version 4 driver ready for connection with clients on port 1500.
    Enter the password to restore the master encryption key (or press Enter to skip): 
    ANR4634I Starting point-in-time database restore to date 06/28/2026 11:59:59 PM.
    ANR4591I Selected backup series 1015 from 06/28/2026 and 06:01:00 AM as best candidate available for restore database processing.
    ANR4592I Restore database backup series 1015 includes eligible operation 0 with volume /sp/dbb/82619209.DBV having sequence 100001 and
    using device class DBB.
    ANR4592I Restore database backup series 1015 includes eligible operation 0 with volume /sp/dbb/82619210.DBV having sequence 100002 and
    using device class DBB.
    ANR4598I Validating database backup information for selected backup series 1015 and operation 0 using volume /sp/dbb/82619210.DBV.
    ANR8340I FILE volume /sp/dbb/82619210.DBV mounted.
    ANR1363I Input volume /sp/dbb/82619210.DBV opened (sequence number 1).
    ANR4614E The database backup timestamp of 20260628060010 on database backup media with backup type FULL does not match the backup timestamp
    20260628060100 from the volume history file. This volume cannot be used to restore the database.
    ANR1364I Input volume /sp/dbb/82619210.DBV closed.
    ANR4602E No volumes found for TODATE 06/28/2026 11:59:59 PM.
    ```

    __Taa-daam!__ Jest timestamp: `20260628060010` co przekłada się na datę: `2026/06/28 06:00:10`. 

1. Popraw `volhist.dat`.

    ``` title="Finalna wersja volhist.dat"
    Operation Date/Time:   2026/06/28 06:00:10

    Volume Type:  BACKUPFULL
    Volume Name:  "/sp/dbb/82619209.DBV"
    Backup Series:        1015
    Backup Op:               0
    Volume Seq:         100001
    Device Class Name:  DBB
    **************************************************
    Operation Date/Time:   2026/06/28 06:00:10

    Volume Type:  BACKUPFULL
    Volume Name:  "/sp/dbb/82619210.DBV"
    Backup Series:        1015
    Backup Op:               0
    Volume Seq:         100002
    Device Class Name:  DBB
    **************************************************
    ```

1. Odtwórz bazę do wskazanego timestampu. 

    !!! Notice

        W mojej komendzie pojawił się parametr `on=dbdirs.txt`. To dlatego, że odtwarzam do innej struktury katalogów niż miał oryginał. 


    ```bash title="Finalne zaklęcie odtwarzania bazy"
    dsmserv -i /sp/spinst1 restore db todate=06/28/2026 totime=06:00:10 on=dbdirs.txt
    ```

    ??? Example "Przykład (przydługi)"

        ```bash
        [spinst1@sp-1 spinst1]$ dsmserv -i /sp/spinst1 restore db todate=06/28/2026 totime=06:00:10 on=dbdirs.txt 
        ANR7800I DSMSERV generated at 10:53:50 on Mar 19 2026.

        IBM Storage Protect for Linux/ppc64le
        Version 8, Release 2, Level 1.000

        Licensed Materials - Property of IBM

        (C) Copyright IBM Corporation 1990, 2026.
        All rights reserved.
        U.S. Government Users Restricted Rights - Use, duplication or disclosure
        restricted by GSA ADP Schedule Contract with IBM Corporation.

        ANR7801I Subsystem process ID is 2611058.
        ANR0900I Processing options file /sp/spinst1/dsmserv.opt.
        ANR0010W Unable to open message catalog for language en_US.UTF-8. The default language message catalog will be used.
        ANR7814I Using instance directory /sp/spinst1.
        ANR3339I Default Label in key data base is TSM Server SelfSigned SHA Key. 
        ANR4726I The ICC support module has been loaded.
        ANR8598I Outbound SSL Services were loaded.
        ANR8230I TCP/IP Version 6 driver ready for connection with clients on port 1500.
        ANR8200I TCP/IP Version 4 driver ready for connection with clients on port 1500.
        Enter the password to restore the master encryption key (or press Enter to skip): 
        ANR4634I Starting point-in-time database restore to date 06/28/2026 06:00:10 AM.
        ANR4591I Selected backup series 1015 from 06/28/2026 and 06:00:10 AM as best candidate available for restore database processing.
        ANR4592I Restore database backup series 1015 includes eligible operation 0 with volume /sp/dbb/82619209.DBV having sequence 100001 and
        using device class DBB.
        ANR4592I Restore database backup series 1015 includes eligible operation 0 with volume /sp/dbb/82619210.DBV having sequence 100002 and
        using device class DBB.
        ANR4598I Validating database backup information for selected backup series 1015 and operation 0 using volume /sp/dbb/82619210.DBV.
        ANR8340I FILE volume /sp/dbb/82619210.DBV mounted.
        ANR1363I Input volume /sp/dbb/82619210.DBV opened (sequence number 1).
        ANR4609I Restore database process found FULL database backup timestamp 20260628060010 from database backup media.
        ANR4609I Restore database process found FULL database backup timestamp 20260628060010 from database backup media.
        ANR1364I Input volume /sp/dbb/82619210.DBV closed.
        ANR3008I Database backup was written using client API: 8.1.23.0.
        ANR4638I Restore of backup series 1015 operation 0 in progress.
        ANR4897I Database restore of operation 0 will use device class DBB and attempt to use 2 streams.
        ANR8592I Session 1 connection is using protocol TLSV13, cipher specification TLS_AES_128_GCM_SHA256, certificate sp-1. 
        ANR0839I Session 1 started for node $$_TSMDBMGR_$$ (DB2/LINUXPPC64LE) (SSL localhost[127.0.0.1]:35332) on localhost:1500.
        ANR8340I FILE volume /sp/dbb/82619209.DBV mounted.
        ANR0510I Session 1 opened input volume /sp/dbb/82619209.DBV.
        ANR1363I Input volume /sp/dbb/82619209.DBV opened (sequence number 1).
        ANR8592I Session 2 connection is using protocol TLSV13, cipher specification TLS_AES_128_GCM_SHA256, certificate sp-1. 
        ANR0839I Session 2 started for node $$_TSMDBMGR_$$ (DB2/LINUXPPC64LE) (SSL localhost[127.0.0.1]:35344) on localhost:1500.
        ANR8340I FILE volume /sp/dbb/82619210.DBV mounted.
        ANR0510I Session 2 opened input volume /sp/dbb/82619210.DBV.
        ANR1363I Input volume /sp/dbb/82619210.DBV opened (sequence number 1).
        ANR4912I Database restore is in progress. A total of 1,073,741,824 bytes have been transferred.
        ANR4912I Database restore is in progress. A total of 2,147,483,648 bytes have been transferred.
        ANR4912I Database restore is in progress. A total of 3,221,225,472 bytes have been transferred.
        ANR4912I Database restore is in progress. A total of 4,294,967,296 bytes have been transferred.
        ANR4912I Database restore is in progress. A total of 5,368,709,120 bytes have been transferred.
        ANR4912I Database restore is in progress. A total of 6,442,450,944 bytes have been transferred.
        ANR1364I Input volume /sp/dbb/82619209.DBV closed.
        ANR0514I Session 1 closed volume /sp/dbb/82619209.DBV.
        ANR0403I Session 1 ended for node $$_TSMDBMGR_$$ (DB2/LINUXPPC64LE).
        ANR0403I Session 2 ended for node $$_TSMDBMGR_$$ (DB2/LINUXPPC64LE).
        ANR8592I Session 3 connection is using protocol TLSV13, cipher specification TLS_AES_128_GCM_SHA256, certificate sp-1. 
        ANR0839I Session 3 started for node $$_TSMDBMGR_$$ (DB2/LINUXPPC64LE) (SSL localhost[127.0.0.1]:40490) on localhost:1500.
        ANR1364I Input volume /sp/dbb/82619210.DBV closed.
        ANR0514I Session 3 closed volume /sp/dbb/82619210.DBV.
        ANR0403I Session 3 ended for node $$_TSMDBMGR_$$ (DB2/LINUXPPC64LE).
        ANR8592I Session 4 connection is using protocol TLSV13, cipher specification TLS_AES_128_GCM_SHA256, certificate sp-1. 
        ANR0839I Session 4 started for node $$_TSMDBMGR_$$ (DB2/LINUXPPC64LE) (SSL localhost[127.0.0.1]:40496) on localhost:1500.
        ANR0403I Session 4 ended for node $$_TSMDBMGR_$$ (DB2/LINUXPPC64LE).
        ANR8592I Session 5 connection is using protocol TLSV13, cipher specification TLS_AES_128_GCM_SHA256, certificate sp-1. 
        ANR0839I Session 5 started for node $$_TSMDBMGR_$$ (DB2/LINUXPPC64LE) (SSL localhost[127.0.0.1]:40504) on localhost:1500.
        ANR0403I Session 5 ended for node $$_TSMDBMGR_$$ (DB2/LINUXPPC64LE).
        ANR1628I The database manager is using port 51500 for server connections.
        ANR4635I Point-in-time database restore complete, restore date 06/28/2026 06:00:10 AM.
        ANR3096I The volumes used to perform this restore operation were successfully recorded in the server volume history.
        ANR0369I Stopping the database manager because of a server shutdown.

        ```
        
## Import istniejącej instancji 


