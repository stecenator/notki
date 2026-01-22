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
- Bez licencji, czyli poprawki. Nazwy zwykle zaczynając się od cyferek, np `8.1.27.000-IBM-SPSRV-Linuxx86_64.bin`. Te można sciągać z FixCentral, albo [bezpośrednio](https://www3.software.ibm.com/storage/tivoli-storage-management/).

    !!! Tip 
        Zarówno patch jak i maintenance dają się zainstalować jako produkt. Nie posiadają licencji więc będą działać przez 30 dni. Po donistalowaniu pakietu z licencją stają się pełnowymiarowymi instalacjami.

    - W katalogu `patches` są poprawki podbijające 4 liczbę w wersji. 
    - W katalogu `maintenance` są poprawki podbijajace 3 liczbę w wersji

!!! Warning
    Założenie patcha/maintnenance np 8.2 (1) na instalację 8.1 spowoduje utratę licencji. Trzeba ją będzie zainstalować z legitnej paczki `SP_8.2*`. 
    { .annotate }

    1. Jak już się jakiś pojawi.


### Opcje instalatora

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

```sh title="Zakłądanie usera dla instancji"
sudo useradd spinst1 -G wheel
```

## Tworzenie instancji :IBM-bw: DB2



### Środowisko

Zmodyfikowane do potrzeb backupu bazy ISP środowisko usera instancji bazy jest w pliku `/home/tsminst/sqllib/userprofile`:

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

### (u)Limity `/etc/security/limits.d/spinst1.conf`

Jak wtytule, zwykle robię _dropin_ z ustawianiemi ulimitów. Zawsze warto je [sprawdzić w :IBM-bw:](https://www.ibm.com/docs/en/storage-protect/8.2.0?topic=instance-verifying-access-rights-user-limits) dla aktualnej wersji. Tu dla 8.2.

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

## Konfiguracja instancji

Plik konfiguracji instancji w *katalogu_instancji* `/tsm/tsminst1` przed formatowaniem, wystarczy, że zawiera tylko `commmethod`. Po formatowaniu będzie miał resztę bajerów. Ja od siebie dodaję jeszcze rochę:

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

## Formatowanie instancji

Upewnij się, że masz:

- [x] Zainstalowane binarki ISP.
- [x] Utworzonego usera `spinst`.
- [x] Skonfigurowane ulimity `spinst`.
- [x] Skonfigurowane sysctl'e w jądrze.
- [x] Skonfigurowane środowisko usera `spinst1`.
- [x] Utworzoną hierarchię katalogów/filesystemów. Upewnij się, że `spinst1` może po nich pisać.


### Additional Instance settings

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
