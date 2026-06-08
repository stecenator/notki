---
icon: fontawesome/solid/user
---

# Instalacja klienta BA

Na rożnych platformach.

## AIX

## Linux

Względnie świeżego (1) klienta Linuxowego można ściągnac [stąd](https://www3.software.ibm.com/storage/tivoli-storage-management/maintenance/client/v8r1/Linux/LinuxX86/BA/). 
{ .annotate }

1.  Z pewnych źródeł wiem, że niedługo będzie wersja 8.2 zarówno serwera jak i klienta więc traktuj ten link ze zrozumieniem :wink:.

### Instalacja

Jest prosta. Zwłaszcza na dystrybucjach RPMowych. Wystarczy zainstalować następujące RPMy (tu wersja 8.1.27):

- Szyfrowanki-cacanki. Te paczka występuje też w smaku `gsk*_pd.rpm`. Nie wiem po co to jest i nie isntaluję tego.
    - `gskcrypt64-8.0.60.4.linux.x86_64.rpm`
    - `gskssl64-8.0.60.4.linux.x86_64.rpm`
- `TIVsm-API64.x86_64.rpm` - Packza API - jedyna która jest potrzebna np dla DB2. RMAN też z niej korzysta, ale tam potrzebna jest jeszcze sklejka w postaci TDPO.
- Common Inventory Toolki (CIT): dzieki tym paczkom TSM/Protect potrafi policzyć procesory w klientach. Można nie instalować, ale higienicznej jest to mieć.
    - `TIVsm-APIcit.x86_64.rpm`
    - `TIVsm-BAcit.x86_64.rpm`
- `TIVsm-BA.x86_64.rpm` - Klient backupu plikowego. Tu jest też `dsmadmc` i agent `dsmcad`, dlatego zawsze ją instaluję.
- *opcjonalne* `TIVsm-WEBGUI.x86_64.rpm` - Jeśli lubisz GUI webowe to dorzuć.

```sh title="Instalacja na RHEL 9"
[root@dibitu ba-8.1.27]# rpm -Uvh gskcrypt64-8.0.60.4.linux.x86_64.rpm gskssl64-8.0.60.4.linux.x86_64.rpm TIVsm-API64.x86_64.rpm TIVsm-APIcit.x86_64.rpm TIVsm-BAcit.x86_64.rpm TIVsm-BA.x86_64.rpm
warning: gskcrypt64-8.0.60.4.linux.x86_64.rpm: Header V4 RSA/SHA256 Signature, key ID 96e7c766: NOKEY
warning: TIVsm-API64.x86_64.rpm: Header V4 RSA/SHA256 Signature, key ID e58157a3: NOKEY
Verifying...                          ################################# [100%]
Preparing...                          ################################# [100%]
Updating / installing...
   1:gskcrypt64-8.0-60.4              ################################# [ 17%]
   2:gskssl64-8.0-60.4                ################################# [ 33%]
   3:TIVsm-API64-8.1.27-0             ################################# [ 50%]
   4:TIVsm-APIcit-8.1.27-0            ################################# [ 67%]
   5:TIVsm-BA-8.1.27-0                ################################# [ 83%]
   6:TIVsm-BAcit-8.1.27-0             ################################# [100%]
```

#### Automatyzacja instalacji

W [tym](../../LNX/repo.md) rozdziale opisałem jak zrobić sobie lokalne repozytorium z pakietami kllienta BA. Jest to przydatne, gy muszę utrzymać więcej niż jednego klietna i chcę, żeby poprawki na BA wjeżdzały automatycznie wraz z poprawkami na OS. 

### Konfiguracja klienta BA

Za konfigurację odpowiedzialne są dwa pliki: `dsm.sys` i `dsm.opt`.
Poniższe przykłady konfigów wrzucam jako szablon jinja2, bo i tak zwykle używam tego w z:simple-ansible:utomatyzowanych środowiskach.

```jinja title="dsm.sys"
servername {{ mój_protect }}                                * Mój alias. Mogę mieć takich wiele
        tcpserveraddress        {{ fqdn_mojego_protecta }}  * IP lub FQDN serwera Protect
        errorlogn               /var/log/tsm/dsmerror.log
        errorlogret             10 d
        schedlogn               /var/log/tsm/dsmsched.log
        schedlogret             10 d
        passwordaccess          generate
        nodename                {{ mój_nodename }}          * Jak pominę to mój hostname
        inclexcl                /etc/inclexcl.txt
        resourceutilization     6
        deduplication           yes
        dedupcachepath          /var/spdedup
        ENABLEDEDUPCache        yes
        virtualmount            /etc
        * Bo bez tego CMS w WebGUI nie zadziałą
        managedservices         schedule webclient
        httpport                1581
```

```jinja2 title="dsm.opt"
servername {{ mój_protect }}            * alias stanzy z dsm.sys
* tu jeszcze bywa kilka innych opcji
```

Umieść te pliki w `/opt/tivoli/tsm/client/ba/bin/` odpowiednio podstawiając wartości w miejsce `{{ zmiennych }}`.

## Agent `dsmcad` 

Czasem przydaje się dodatkowy agent `dsmcad`. Ty przykłąd utworzenie agenta `dsmcad-local` któ©y będzie używał innego pliku `dsm.opt` niż domyślny.

1. Skopiuj istniejący plik usługi `dsmcad.service` na `dsmcad-local.servie`.
1. Dodaj zaznaczoną linijkę do tej usługi:

    ```ini hl_lines="12" title="Zmodyfikowany serive unit"
    [Unit]
    Description="Agent SP"
    After=local-fs.target network-online.target

    [Service]
    Type=forking
    GuessMainPID=no
    Environment="DSM_LOG=/opt/tivoli/tsm/client/ba/bin"
    Environment="JAVA_HOME=/opt/tivoli/tsm/tdpvmware/common/jre/jre"
    Environment="LD_LIBRARY_PATH=/opt/tivoli/tsm/client/ba/bin:/opt/tivoli/tsm/tdpvmware/common/jre/jre/bin/classic"
    Environment="PATH=/opt/tivoli/tsm/tdpvmware/common/jre/jre/bin:/sbin:/usr/sbin:/usr/local/sbin:/root/bin:/usr/local/bin:/usr/bin:/bin"
    Environment="DSM_CONFIG=/opt/tivoli/tsm/client/ba/bin/dsm-local.opt"
    EnvironmentFile=/opt/tivoli/tsm/client/ba/bin/dsmcad.lang
    ExecStart=/usr/bin/dsmcad
    ExecStopPost=/bin/bash -c 'let i=0; while [[ (-n "$(ps -eo comm | grep dsmcad)") && ($i -le 10) ]]; do let i++; sleep 1; done'
    Restart=on-failure

    [Install]
    WantedBy=multi-user.target 
    ```

    !!! Warning "Uwaga"

        Zadbaj o to, żeby klient używający stanzy wskazanej w nowym pliku konfiguracyjnym nie pogryzł się o porty i logi z innymi

1. Przeładuj `systemd`:

    ```sh title="Restat systemd"
    sudo systemctl daemonr-reload
    ```

1. Włącz nowego CAD'a.


## Łindołs

Winda jaka jest, kazdy widzi. Tu piszę tricki które się przydają w chodzeniu na skróty ;-)

### Instalacja `CAD` i `schedule`  przy pomocy `dsmcutil.exe`


```
dsmcutil install scheduler /name:"tsmscheduler" /node:dwhb /password:ibm12345 /startnow:no 
dsmcutil install cad /node:dwhb /password:ibm12345 /autostart:yes /startnow:no 
dsmcutil update cad /name:"tsm client acceptor" /cadschedname:"tsmscheduler" 
dsmcutil start /name:"tsm client acceptor"
```