---
icon: material/shield
---

# :IBM-bw: Storage Protect 

!!! Tip inline end "Podpowiedź"
    Jak masz jakieś [X11](../LNX/x11.md) to można użyć :material-wizard-hat: wizarda: `dsmicfgx`.

Konfiguracja instancji "z palca". Warto to znać, bo nie wszędzie jest grafika. Ktrok po kroku:

## Instalacja binarek

Instalacja binariów serwera sprowadza się do:

- Rozpakowania gdzieś _self-extracting_ archiwum.
- Odpalenia `install.sh`.

Ale jak zwykle diabeł tkwi w szczegółach.

### Instalki

Instalki występują w dwóch smakach:

- Z licencją - dla klientów którzy kupili. Tu zwykle nazwy pliku zacynają się od `SP_*`, np. `SP_8.2_LIN86_SERSTG_AGT_ML.bin`. Te binarki są dostęþne przez [PAO](https://www.ibm.com/software/passportadvantage/pao-customer)
- Bez licencji, czyli poprawki. Nazwy zwykle zaczynają się od cyferek, np `8.1.27.000-IBM-SPSRV-Linuxx86_64.bin`. Te można sciągać z FixCentral, albo [bezpośrednio](https://www3.software.ibm.com/storage/tivoli-storage-management/).

    !!! Tip 
        Zarówno patch jak i maintenance dają się zainstalować jako produkt. Nie posiadają licencji więc będą działać przez 30 dni. Po donistalowaniu pakietu z licencją stają się pełnowymiarowymi instalacjami.

    - W katalogu `patches` są poprawki podbijające 4 liczbę w wersji. 
    - W katalogu `maintenance` są poprawki podbijajace 3 liczbę w wersji

!!! Warning
    Założenie patcha/maintnenance np 8.2 (1) na instalację 8.1 spowoduje utratę licencji. Trzeba ją będzie zainstalować z legitnej paczki `SP_8.2*`. 
    { .annotate }

    1. Jak już się jakiś pojawi.


### Opcje instalatora

Przydatne przałaćzniki instalatora `install.sh`. Instalator domyślnie będzie próbował wystartować graficznie, ale dzisiejsze Unixy zwykle grafiki nie mają. Wtedy zostaje konsola lub cicha instalacja.

- `-s` - cicha instalacja z użyciem _response file_. Plik odpowiedzi można wygenerować podczas interaktywnej instalacji zarówno w trybie graficznym jak i konsolowym.
- `-c` - wymusza instalację w trybie konsolowym.
- `-vmargs "-DBYPASS_TSM_REQ_CHECKS=true"` - Przy instalacji na CentOS/Rocky/Alma/Oracle, albo na zbyt małej ilośći RAMu, ISP może  odmówić instalacji. Ta pozwala ominąć tę blokadę. Przeczytaj po co to [jest](https://www.ibm.com/support/pages/bypass-server-and-storage-agent-prerequisites-during-installation) !

### Instalacja

1. Rozpakuj gdzieś binarki. Przejdź do katalogu docelowego i uruchom śćignięte archiwum:

    ```sh title="Rozpakowanie binarek"
    $ mkdir -p /toys/srv-8.2.0
    $ cd /toys/srv-8.2.0
    $ /scieżka/do/ściągniętego/pliku/SP_8.2_LIN86_SERSTG_AGT_ML.bin
    ```

1. Uruchom instalator jako `root`:

    ```sh title="Start instalatora"
    ./install.sh
    ```

    W razie potrzeby dodaj odpowiednie opcje. instalator automatycznie przełacza sie na tryb konsolowy, jesli nie uda mu się odpalić grafiki.

1. Wybierz paczki do instalacji. Na poniższym przykładzie jest minimum jakiego potrzebuję:

    ``` hl_lines="4 5 7" title="Wybór pakietów"
    =====> IBM Installation Manager> Install

    Select packages to install:
         1. [X] IBM® Installation Manager 1.9.2.8
         2. [X] IBM Storage Protect server 8.2.0.20251121_0614
         3. [ ] IBM Storage Protect languages 8.2.0.20251121_0609
         4. [X] IBM Storage Protect license 8.2.0.20251121_0609
         5. [ ] IBM Storage Protect storage agent 8.2.0.20251121_0606
         6. [ ] IBM Storage Protect device driver  8.2.0.20251121_0610
         7. [ ] IBM Storage Protect Operations Center 8.2.0.20251111_1045
         8. [ ] Open Snap Store Manager 8.2.0.20251121_0607

         O. Check for Other Versions, Fixes, and Extensions

         N. Next,      C. Cancel
    -----> [N] 
    ```

1. Instalator sprawdza zależności. Ja mój uruchomiłem z ignorowaniem wymagań, bo mam za mało RAMu, dlatego dostałem tylko _Warnning_, ale tę brakującą bibliotekę, to trzeba doinstalować.

    ``` hl_lines="6-7 12" title="Sprawdzenie wymagań"
    =====> IBM Installation Manager> Install> Prerequisites

    Validation results:

    * [WARNING] IBM Storage Protect server 8.2.0.20251121_0614 contains validation warning.
         1. WARNING: The system does not meet the recommended memory requirement of 16 GB.
         2. WARNING: libnss3.so is required and cannot be found.

    Enter the number of the error or warning message above to view more details.

    Options:
         R. Recheck status.

         B. Back,      N. Next,      C. Cancel
    -----> [N] 
    ```

    Jak zainstalujesz brakującą bibliotekę (w następnym kroku) to naciśnij `r` żeby ponownie sprawdzić wymagania.

1. Zaloguj się z boku i doinstaluj brakującą bibliotekę 

    ```sh title="Instalacja pakietu dostarczającego bibliotekę libnss3.so"
    sudo dnf install nss
    ```
1. Ponownie sprawdź wymagania.

    ``` hl_lines="6 13" title="Sprawdzenie wymagań"
    =====> IBM Installation Manager> Install> Prerequisites

    Validation results:

    * [WARNING] IBM Storage Protect server 8.2.0.20251121_0614 contains validation warning.
         1. WARNING: The system does not meet the recommended memory requirement of 16 GB.

    Enter the number of the error or warning message above to view more details.

    Options:
         R. Recheck status.

         B. Back,      N. Next,      C. Cancel
    -----> [N] 
    ```

    Jeśli marudzi tylko na RAM, daj mu _next_.

1. Zaakceptuj licencję instalatora :faceplam::

    ``` title="Licencja instalatora"
    =====> IBM Installation Manager> Install> Prerequisites> Licenses

    Read the following license agreements carefully.
    View a license agreement by entering the number:
         1. IBM Installation Manager - License Agreement

    Options:
         A. [X] I accept the terms in the license agreement
         D. [ ] I do not accept the terms in the license agreement

         B. Back,      N. Next,      C. Cancel
    -----> [N] 
    ```
1. Jakieś pierdoły

    ```title="Jakaś pierdoła"
    ====> IBM Installation Manager> Install> Prerequisites> Licenses> 
      Shared Directory

    Installation Manager installation location:
            /opt/IBM/InstallationManager/eclipse

    Shared Resources Directory:
            /opt/IBM/IBMIMShared

    Options:
         L. Change Installation Manager Installation Location  
         M. Change Shared Resources Directory    

         B. Back,      N. Next,      C. Cancel
    ```

    ```title="Jakaś pierdoła"
    =====> IBM Installation Manager> Install> Prerequisites> Licenses> 
      Shared Directory> Location

    New package group:
         1. [X] IBM Storage Protect

    Selected group id: "IBM Storage Protect" 
    Selected location: "/opt/tivoli/tsm"
    Selected architecture: 64-bit

    Options:
         M. Change Location

         B. Back,      N. Next,      C. Cancel
    ```

1. Wybierz licencję. Przy pojemnościowej wybierz _Extended_:

    ``` hl_lines="6" title="Typ licencji"
    Select the product that you purchased: 
         1. IBM Storage Protect 
         2. IBM Storage Protect Extended Edition 
         3. IBM Storage Protect for Data Retention 

    -----> 1
    ```

    ...i zaakceptuj ją:

    ``` hl_lines="6 9 15 21" title="Akceptacja licencji"
    Read the following license agreements carefully. 
    View a license agreement by entering the number: 
         1. IBM Storage Protect - Software License Agreement 
         2. IBM Storage Protect - Non-IBM Terms 
    Options: 
         A. [ ] I accept the terms in the license agreements.  
         D. [ ] I do not accept the terms in the license agreements. 

    -----> A
    Read the following license agreements carefully. 
    View a license agreement by entering the number: 
         1. IBM Storage Protect - Software License Agreement 
         2. IBM Storage Protect - Non-IBM Terms 
    Options: 
         A. [X] I accept the terms in the license agreements.  
         D. [ ] I do not accept the terms in the license agreements. 



         B. Back,      N. Next,      C. Cancel
    -----> [N] 
    ```

1. Podsumowanie i instalacja:

    ``` hl_lines="23" title="Podsumowanie przed instalacją"
    =====> IBM Installation Manager> Install> Prerequisites> Licenses> 
      Shared Directory> Location> Custom panels> Summary

    Target Location:
      Package Group Name         :  IBM Installation Manager
      Installation Directory     :  /opt/IBM/InstallationManager/eclipse
      Package Group Name         :  IBM Storage Protect
      Installation Directory     :  /opt/tivoli/tsm
      Shared Resources Directory :  /opt/IBM/IBMIMShared

    Translations:
            English

    Packages to be installed:
            IBM® Installation Manager 1.9.2.8
            IBM Storage Protect server 8.2.0.20251121_0614
            IBM Storage Protect license 8.2.0.20251121_0609

    Options:
         G. Generate an Installation Response File

         B. Back,      I. Install,      C. Cancel
    -----> [I] 
    ```

1. Koniec instalacji binariów.

    ``` title="Podsumowanie"
                     25%                50%                75%                100%
    ------------------|------------------|------------------|------------------|
    ............................................................................

    =====> IBM Installation Manager> Install> Prerequisites> Licenses> 
      Shared Directory> Location> Custom panels> Summary> Completion

    There were problems during the installation.
    WARNING: Multiple warnings occurred.

         V. View Message Details

    Options:
         F. Finish
    -----> [F] 
    ```

## Parametry jądra :simple-linux:

[Tu](https://www.ibm.com/docs/en/storage-protect/8.2.0?topic=protect-tuning-kernel-parameters-linux-systems) dla wersji 8.2 (1)
{ .annotate }

1. Mam na to playbooka :simple-ansible:nsible. Pewnie kiedyś go tu opiszę.

Z palca można zrobić to tak:

```sh title="Dopieszczanie DB2"
sudo sysctl -w kernel.randomize_va_space=0
sudo sysctl -w vm.swappiness=5
sudo sysctl -w vm.overcommit_memory=0
```

## Użyszkodnik instancji :IBM-bw: Storage Protect 

Od wersji 6 w górę, TSM/Protect działa na dedykowanym użytkowniku. Ten użytkownik nie wymaga specjalnych praw. 

!!! Note "Ciekawostka"
    Użytkownik instancji Protect jest też użytkownikiem instancji DB2. Członkowie primary grupy tego usera są równi bogom w tej instancji (bazy, nie TSM).

| Atrybut            | Wartość | Opis |
| :---               | :---  | :--- |
| Instance user      | `spinst1` | Właściciel instancji SP i DB2. |
| Home               | `/home/spinst` | Katalog domowy instancji DB2. __Uwaga:__ katalog instancji ISP to zwykle u mnie  `/sp/spinst1`. |
| DB2 Instance setup | `/home/spinst/sqllib/userprofile` | Srodowisko instancji DB2. Także __backup!__ |

!!! Tip inline end "Wskazówka"
    Wrzucam usera instancji do grupy `wheel` bo jestem leniem i czasem muszę zrobić coś z nieg przez `sudo`.

!!! Warning "Uwaga na __klastry__"
    Jeśli instalujesz ISP w klastrze, upwenij się, że: 

    - UID i GID Twojego usera jest taki sam na każdym węźle klastra.
    - Katalog domowy użytkownika jest na lokalnym, a nie współdzielonym filesytemie. Są na to dwie szkoły. Druga zakłada, że `home` jest na klastrowym filesystemie, ale ja tak nie lubię.

1. Załóź użytkownika w systemie operacyjnym. 

    ```sh title="Zakłądanie usera dla instancji"
    sudo useradd spinst1 -G wheel
    ```

1. Ustaw właściciela katalogów instancji na usera `spinst1`:

    !!! Note inline end 
        Upewnij się, że filesystemy są zamontowane!

    ```sh title="Zmiana właściciela"
    sudo chown spinst1:spinst1 -R /sp
    ```

1. Zmień (u)limity dla użytkownika instancji. Zrób _dropin_ z ustawianiemi ulimitów. Zawsze warto je [sprawdzić w :IBM-bw:](https://www.ibm.com/docs/en/storage-protect/8.2.0?topic=instance-verifying-access-rights-user-limits) dla aktualnej wersji. Tu dla 8.2.

    ``` title="/etc/security/limits.d/spinst1.conf"
    spinst1 soft nofile 65536
    spinst1 hard nofile 65536
    ```

    !!! Tip "`ulimit` na AIXie"
        Parę rzeczy w AIXie wyjętym z pudełka trzeba zmienić:

        Do `/etc/security/limits` w sekcji `default` albo dla `spinst1` wpisać:

        ```
        nofiles = 65536
        nproc = 8192
        fsize = -1
        ```

## Tworzenie instancji :IBM-bw: Storage Protect

Jak spelnione są te warunki:

- [x] Host ma statyczny IP,
- [x] Host umie rozwiązać swo=ój `hostname` do swojego IP,
- [x] Zainstalowane binarki,
- [x] Wyłączony (tymczasowo) SELinux,
- [x] Podstrojon jądro pod DB2,
- [x] Założony user,
- [x] Ustawione ulimity,
- [x] `spinst1` jest właścicielem katalogów `/sp/*`,

można przejść do tworzenia instancji ISP. Zaczyna się od instancji... DB2

### Tworzenie instancji :IBM-bw: DB2

1. Jako `root` utwórz instancję DB2:

    ``` title="Tworzenie instancji DB2"
    /opt/tivoli/tsm/db2/instance/db2icrt -a server -u spinst1 spinst1
    ```

    !!! Warning "Ważne"
        Od tego miejsca resztę kroków trzeba robić jako `spinst1`.

1. Ustaw domyślny katalog baz na katalog instancji `/sp/spinst1`:

    ``` title="Ustawianie DFTDBPATH"
    db2 update dbm cfg using dftdbpath /sp/inst1
    ```

1. I jeszcze `DB2NOEXITLIST=ON`

    ```sh title="DB2NOEXITLIST=ON"
    db2set -i tsminst1 DB2NOEXITLIST=ON 
    ```

1. Ustaw `LD_LIBRARY_PPATH` i od razu inne zmienne, któ©e przydadzą się póżniej do potrzeb backupu bazy ISP. Środowisko usera instancji bazy jest w pliku `/home/tsminst/sqllib/userprofile`:

    ``` sh title="Zmodyfikowane środowisko ~/sqllib/userprofile:"
    export DSMI_CONFIG=/sp/spinst1/tsmdbmgr.opt
    export DSMI_DIR=/opt/tivoli/tsm/server/bin/dbbkapi
    export DSMI_LOG=/sp/spinst1
    export LD_LIBRARY_PATH=/opt/tivoli/tsm/server/bin/dbbkapi:/usr/local/ibm/gsk8_64/lib64:$LD_LIBRARY_PATH
    ```

    Plik `userprofile` jest wciągany przez `.profile` właściciela instancji:

    ``` sh title="Instance ~/.profile"
    # The following three lines have been added by IBM DB2 instance utilities.
    if [ -f /home/spinst1/sqllib/db2profile ]; then
        . /home/spinst1/sqllib/db2profile
    fi
    ```

## Tworzenie instancji :IBM-bw: Storage Protect

!!! Important "Ważne"
    Poniższe kroki trzeba robić jako użytkownik `spinst1`.

1. Utwórz plik konfiguracji instancji w *katalogu_instancji* `/sp/inst1` przed formatowaniem, wystarczy żeby zawierał tylko `commmethod`. Po formatowaniu będzie miał resztę bajerów. Ja od siebie dodaję jeszcze rochę:

    === "Przed formatowaniem"

        ``` title="/sp/spinst1/dsmserv.opt"
        COMMmethod TCPIP
        TCPPort 1500
        ```
    === "Po formatowaniu"

        ``` title="/sp/spinst1/dsmserv.opt"
        COMMmethod TCPIP
        TCPPort 1500
        DEVCONFIG     devconf.dat
        VOLUMEHISTORY volhist.dat
        ACTIVELOGSize               32768
        ACTIVELOGDirectory          /sp/actlog
        ARCHLOGDirectory            /sp/archlog
        ```

    === "Po moich ulepszeniach"

        ``` hl_lines="8-10" title="/sp/spinst1/dsmserv.opt"
        COMMmethod TCPIP
        TCPPort 1500
        DEVCONFIG     devconf.dat
        VOLUMEHISTORY volhist.dat
        ACTIVELOGSize               32768
        ACTIVELOGDirectory          /sp/actlog
        ARCHLOGDirectory            /sp/archlog
        REORGDURATION 6 
        REORGBEGINTIME 04:00 
        PREALLOCREDUCTIONRATE 12
        ```

1. Przejdź do `/sp/inst1`.
1. Sformatuj instancję.

    ```sh title="Formatoanie instancji ISP"
    dsmserv format dbdir=/sp/db/01,/sp/db/02 activelogsize=16384 activelogdirectory=/sp/actlog archlogdirectory=/sp/archlog
    ```

1. `tsmdbmgr.opt`
1. usługa systemd
1. Makro z ulubionnymi `set/setopt` i definicją `DBB`


    Additional Instance settings

    Some settings had to be changed to reflect best practices or local conditions. 

    | Setting | Value | Comment |
    | :--- |  :--- | :--- |
    | `MINPWLENGTH` | 8 | To adhere with BG-TIVOLI instance |
    | `PWREUSELIMIT` | 12 | Left untouched since BG-TIVOLI does not have it yet |
    | `PREALLOCREDUCTIONRATE` | 12 | To adhere with BG-TIVOLI instance. Should improve replication performance |
    | `REORGDURATION` | 6 | To adhere with BG-TIVOLI instance. Helps minimizing possible overlap with replication windows |
    | `REORGBEGINTIME` | 04:00 | To adhere with BG-TIVOLI instance. Helps minimizing possible overlap with replication windows |
    | `VolumeHistory` | `/tsm/tsminst1/volhist.dat`| Default volume history backup location |
    | `DevConfig` | `/tsm/tsminst1/devconf.dat`| Default device configuration backup location |


### Filesystem locations

All leaf dirs on the following tree are mountpoints for dedicated filesystems. All filesystems are on LVM so can be on-line extended and migrated.

```sh
[root@spbg01 /]# tree -d /tsm
/tsm
├── actlog
├── archlog
├── db
│	 ├── 01
│	 └── 02
├── dbb
├── dc01
│	 ├── 01
│	 └── 02
└── tsminst1
```

### Service definition

IBM Storage Protect instance is started automatically upon OS startup. The service defined is `tsminst1.service`:

``` ini title="Systemd service unit tsminst1.service definition"
[Unit]
Description=IBM Storage Protect Server instance tsminst1

[Service]
TasksMax=infinity
Type=oneshot
RemainAfterExit=true
ExecStart=/opt/tivoli/tsm/server/bin/tsminst1 start
ExecStop=/opt/tivoli/tsm/server/bin/tsminst1 stop
ExecReload=/opt/tivoli/tsm/server/bin/tsminst1 restart

[Install]
WantedBy=multi-user.target
```

A customized version of instance specific startup script is launched from: `/opt/tivoli/tsm/server/bin/tsminst1`. Template customizations:

- `instance_dir=/tsm/tsminst1`
- `instance_user=tsminst1`

Template scritpt used: `/opt/tivoli/tsm/server/bin/rc.dsmserv`
