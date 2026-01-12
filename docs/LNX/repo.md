---
icon: rpm-repo
---

# Repozytorium YUM/DNF

Czasem potrzebne jest repozytorium paczek RPM dostępne lokalnie, np dla odizolowanych systemów. Sam :simple-redhat: pokazuje jak to zrobić w przypadku instalek/poprawek OS, gdy nie ma możliwości podpięcia się z subskrypcją do `CDN`, i w lokalnym intranecie nie ma Satellite. Ja używam tego mechanizmu do instalacji klientów :IBM-bw: Storage Protect. 

[Źródło](https://www.redhat.com/en/blog/ftp-yum-dnf-repository) podaje, co prawda, sposób na postawiene tego na FTP, ale to praktycznie bez znaczenia. Ja stawiam to na HTTP.

## Zalożenia

<div class="grid cards" markdown>

- :lighttpd: __Lighttpd__ zostanie użyty jako webserwer.
- :octicons-file-directory-16: __Katalog__ dla repozytorium to `/data/ba`
- :rpm-repo: __Pakiety__ w repozytorium to :simple-linux: klient  do :IBM-bw: Storage Protect.
- :simple-curl: __Adres__ repozytorium: `http://mój.server/data/ba`.
- ::octicons-cpu-16:: Będą dwie __Architektury CPU__: :simple-intel:/:simple-amd: x86_64 i :IBM-bw: ppc64le. 

</div>

## Przygotowanie repozytorium

1. Skonfiguruj :lighttpd: Lighttpd.

    Konfiguracja wraz ze sposobem udostępnienia katalogu `/data`, jest opisana [tutaj](lighttpd.md).
    Po prostu zrób tam katalogi:

    ```sh title="Katalogi pod repozytoria"
    sudo mkdir /data/ba/{x86_64,ppc64le}
    ```

1. Ściągnij pakiety (1). Zwykle robi się to [stąd](https://www3.software.ibm.com/storage/tivoli-storage-management/maintenance/client/)
    { .annotate }

    1. W chwili pisania tej procedury, pakiety w wersji 8.2 są doastępne tylko przez PAO. Jak się pojawi poprawka, np 8.2.1 to powinna być tu dostępna

1. Rozpakuj pakiety do `/data/ba`:

    !!! Note "Zwróć uwagę"
        W przykładach posługuję się plikami ściągniętymi z PAO/XL Downloads. Pliki ściągane z IBM Fix Central albo URLa, który podałem wyżej, będą miały nazwy zaczynające się od numeru wersji, np `8.1.27.1-TIV-TSMBAC-LinuxX86.tar(.gz)`. W archiwum będą paczki bez podkatalogów. 

        Ponadto archiwa z PAO mają także wersję pakietów pod :simple-debian:/:simple-ubuntu:, które nie są mi (teraz) potrzebne. 

    ```sh title="Rozpkowanie tara z pakietami do repozytorium"
    # Power:
    tar xzvf SP_CLIENT_8.2_LINPOW_LE_ML.tar.gz -C /data/ba/ppc64le
    # PC-XT:
    tar xzvf SP_CLIENT_8.2_LIN86_ML.tar.gz -C /data/ba/x86_64
    ```

1. __Opcjonalnie__: wyprostuj strukturę katalogów po rozpoakowaniu paczek. Przy archiwach z FixCentral pewnie nie trzeba będzie tego robić. Celem jest umieszczenie wszystkich potrzebnym pakietów `rpm` bezpośrednio w katalogu `/data/ba/${basearch}/`:


    === "Przed:"

        ```
        /data/ba
        ├── ppc64le
        │   └── TSMCLI_LNXPLE
        │       └── tsmcli
        │           ├── linuxPLE
        │           │   ├── bacli
        │           │   ├── content.spsig
        │           │   ├── gskcrypt64-8.0.60.4.linux.ppcle.rpm
        │           │   ├── GSKit.pub4.pgp
        │           │   ├── gskssl64-8.0.60.4.linux.ppcle.rpm
        │           │   ├── PRD0001289key.pub.asc
        │           │   ├── TIVsm-API64.ppc64le.rpm
        │           │   ├── TIVsm-APIcit.ppc64le.rpm
        │           │   ├── TIVsm-BAcit.ppc64le.rpm
        │           │   ├── TIVsm-BA.ppc64le.rpm
        │           │   ├── TIVsm-WEBGUI.ppc64le.rpm
        │           │   └── update.txt
        │           └── linuxPLE_DEB
        │               ├── gskcrypt64_8.0-60.4_ppc64el.deb
        │               ├── gskssl64_8.0-60.4_ppc64el.deb
        │               ├── README_api.htm
        │               ├── README.htm
        │               ├── tivsm-api64.ppc64el.deb
        │               ├── tivsm-apicit.ppc64el.deb
        │               ├── tivsm-bacit.ppc64el.deb
        │               ├── tivsm-ba.ppc64el.deb
        │               ├── TIVsm-filepath-source.tar.gz
        │               └── tivsm-jbb.ppc64el.deb
        └── x86_64
            └── TSMCLI_LNX
                └── tsmcli
                    ├── linux86
                    │   ├── gskcrypt64-8.0.60.4.linux.x86_64_pd.rpm
                    │   ├── gskcrypt64-8.0.60.4.linux.x86_64.rpm
                    │   ├── GSKit.pub4.pgp
                    │   ├── gskssl64-8.0.60.4.linux.x86_64_pd.rpm
                    │   ├── gskssl64-8.0.60.4.linux.x86_64.rpm
                    │   ├── PRD0001289key.pub.asc
                    │   ├── README_api.htm
                    │   ├── README.htm
                    │   ├── RPM-GPG-KEY-ibmpkg
                    │   ├── TIVsm-API64.x86_64.rpm
                    │   ├── TIVsm-APIcit.x86_64.rpm
                    │   ├── TIVsm-BAcit.x86_64.rpm
                    │   ├── TIVsm-BAhdw.x86_64.rpm
                    │   ├── TIVsm-BA.x86_64.rpm
                    │   ├── TIVsm-filepath-source.tar.gz
                    │   ├── TIVsm-JBB.x86_64.rpm
                    │   ├── TIVsm-WEBGUI.x86_64.rpm
                    │   └── update.txt
                    └── linux86_DEB
                        ├── gskcrypt64_8.0-60.4.linux.x86_64.deb
                        ├── gskssl64_8.0-60.4.linux.x86_64.deb
                        ├── README_api.htm
                        ├── README.htm
                        ├── tivsm-api64.amd64.deb
                        ├── tivsm-apicit.amd64.deb
                        ├── tivsm-ba.amd64.deb
                        ├── tivsm-bacit.amd64.deb
                        ├── tivsm-bahdw.amd64.deb
                        ├── tivsm-filepath-source.tar.gz
                        └── tivsm-jbb.amd64.deb

        ```

    === "Po"

        ```
        /data/ba
        ├── ppc64le
        │   ├── bacli
        │   ├── content.spsig
        │   ├── gskcrypt64-8.0.60.4.linux.ppcle.rpm
        │   ├── GSKit.pub4.pgp
        │   ├── gskssl64-8.0.60.4.linux.ppcle.rpm
        │   ├── PRD0001289key.pub.asc
        │   ├── TIVsm-API64.ppc64le.rpm
        │   ├── TIVsm-APIcit.ppc64le.rpm
        │   ├── TIVsm-BAcit.ppc64le.rpm
        │   ├── TIVsm-BA.ppc64le.rpm
        │   ├── TIVsm-WEBGUI.ppc64le.rpm
        │   └── update.txt
        └── x86_64
            ├── gskcrypt64-8.0.60.4.linux.x86_64_pd.rpm
            ├── gskcrypt64-8.0.60.4.linux.x86_64.rpm
            ├── GSKit.pub4.pgp
            ├── gskssl64-8.0.60.4.linux.x86_64_pd.rpm
            ├── gskssl64-8.0.60.4.linux.x86_64.rpm
            ├── PRD0001289key.pub.asc
            ├── README_api.htm
            ├── README.htm
            ├── RPM-GPG-KEY-ibmpkg
            ├── TIVsm-API64.x86_64.rpm
            ├── TIVsm-APIcit.x86_64.rpm
            ├── TIVsm-BAcit.x86_64.rpm
            ├── TIVsm-BAhdw.x86_64.rpm
            ├── TIVsm-BA.x86_64.rpm
            ├── TIVsm-filepath-source.tar.gz
            ├── TIVsm-JBB.x86_64.rpm
            ├── TIVsm-WEBGUI.x86_64.rpm
            └── update.txt
        ```

1. Zainstaluj pakiet dostarczający komendę `createrepo`:

    ```sh title="instalacja createrepo_c"
    sudo dnf install createrepo_c
    ```

1. Utwórz repozytoria w obu podkatalogach `${basearch}`:

    ```sh
    createrepo -v .
    ```

1. Utwórz plik `/data/ba/ba.repo` o następującej zawartośći:

    !!! Warning "Uwaga"
        Podmień zadres w `baseurl` na adres FQDN lub IP konfigurowanego serwera.

    ```ini hl_lines="3"
    [SP-BA]
    name=Spectrum Protect Backup/Archive Client
    baseurl=http://10.10.13.14/data/ba/$basearch/
    enabled=1
    gpgcheck=1
    skip_if_unavailable=1
    gpgkey=http://10.10.13.14/data/ba/$basearch/GSKit.pub4.pgp http://10.10.13.14/data/ba/$basearch/PRD0001289key.pub.asc
    ```

Gotowe!

## Instalacja repozytorium na kliencie

1. Zaloguj się na klienta jako `root`.
1. Do katalogu `/etc/yum.repo.d` sciągnij plik `ba.repo` z przygotowanego serwera:

    ```sh title="Instalacja repozytorium SP-BA"
    cd /etc/yum.repos.d
    wget http://10.10.13.14/data/ba/ba.repo # albo curl -o
    ```

    ??? Example "Przykład:"

        ```sh hl_lines="1-2 13 16"
        [root@sp-ppc ~]# cd /etc/yum.repos.d/
        [root@sp-ppc yum.repos.d]# wget http://10.10.13.14/data/ba/ba.repo
        --2026-01-12 13:47:35--  http://10.10.13.14/data/ba/ba.repo
        Connecting to 10.10.13.14:80... connected.
        HTTP request sent, awaiting response... 200 OK
        Length: 259 [application/octet-stream]
        Saving to: ‘ba.repo’

        ba.repo                               100%[=======================================================================>]     259  --.-KB/s    in 0s      

        2026-01-12 13:47:35 (35.9 MB/s) - ‘ba.repo’ saved [259/259]

        [root@sp-ppc yum.repos.d]# dnf repolist 
        Updating Subscription Management repositories.
        repo id                                                  repo name
        SP-BA                                                    Spectrum Protect Backup/Archive Client
        epel                                                     Extra Packages for Enterprise Linux 8 - ppc64le
        rhel-9-for-ppc64le-appstream-rpms                        Red Hat Enterprise Linux 9 for Power, little endian - AppStream (RPMs)
        rhel-9-for-ppc64le-baseos-rpms                           Red Hat Enterprise Linux 9 for Power, little endian - BaseOS (RPMs)
        ```

1. Zainstaluj pakiety:

    - `TIVsm-BA`
    - `TIVsm-BAcit`
    - `TIVsm-APIcit`

    Jeśli zależności poprawnie zadziałają (1), pownny się zainstalować także pakiety zależne.
    { .annotate }

    1. Od wersji 8.2 powinny, dla 8.1.x pakiety `gsk*` świrują z brakiem polecenia `/bin/ln` :man_facepalming:.

    Lista zależności:

    - `TIVsm-API64`
    - `gskssl64`
    - `gskcrypt64`

    !!! Note
        Przy pierwszym użyciu, `dnf` będzie prosił o zgodę na import kluczy GPG.

    ```sh title="Insalacja klienta BA z nowego repozytorium"
    sudo dnf install TIVsm-BA TIVsm-BAcit TIVsm-APIcit
    ```

    ??? Example "Przykład:"

        ```sh
        [root@sp-ppc ~]# dnf install TIVsm-BA TIVsm-BAcit 
        Updating Subscription Management repositories.
        Spectrum Protect Backup/Archive Client                                                                                 13 MB/s |  55 kB     00:00    
        Last metadata expiration check: 0:00:01 ago on Mon 12 Jan 2026 01:59:17 PM CET.
        Dependencies resolved.
        ======================================================================================================================================================
         Package                                Architecture                       Version                             Repository                        Size
        ======================================================================================================================================================
        Installing:
         TIVsm-BA                               ppc64le                            8.2.0-0                             SP-BA                             57 M
         TIVsm-BAcit                            ppc64le                            8.2.0-0                             SP-BA                            2.2 M
        Upgrading:
         gskcrypt64                             ppc64le                            8.0-60.4                            SP-BA                            2.2 M
         gskssl64                               ppc64le                            8.0-60.4                            SP-BA                            9.8 M
        Installing dependencies:
         TIVsm-API64                            ppc64le                            8.2.0-0                             SP-BA                             52 M

        Transaction Summary
        ======================================================================================================================================================
        Install  3 Packages
        Upgrade  2 Packages

        Total download size: 123 M
        Is this ok [y/N]: y
        Downloading Packages:
        (1/5): TIVsm-BAcit.ppc64le.rpm                                                                                         27 MB/s | 2.2 MB     00:00    
        (2/5): gskcrypt64-8.0.60.4.linux.ppcle.rpm                                                                             30 MB/s | 2.2 MB     00:00    
        (3/5): gskssl64-8.0.60.4.linux.ppcle.rpm                                                                               30 MB/s | 9.8 MB     00:00    
        (4/5): TIVsm-API64.ppc64le.rpm                                                                                         38 MB/s |  52 MB     00:01    
        (5/5): TIVsm-BA.ppc64le.rpm                                                                                            35 MB/s |  57 MB     00:01    
        ------------------------------------------------------------------------------------------------------------------------------------------------------
        Total                                                                                                                  75 MB/s | 123 MB     00:01     
        retrieving repo key for SP-BA unencrypted from http://10.10.13.14/data/ba/ppc64le/GSKit.pub4.pgp
        Spectrum Protect Backup/Archive Client                                                                                1.5 MB/s | 1.6 kB     00:00    
        Importing GPG key 0x96E7C766:
         Userid     : "GSKit Signing Key <psirt@us.ibm.com>"
         Fingerprint: 9FE8 AEAE 5E30 4567 5020 196B 308C C91D 96E7 C766
         From       : http://10.10.13.14/data/ba/ppc64le/GSKit.pub4.pgp
        Is this ok [y/N]: y
        Key imported successfully
        retrieving repo key for SP-BA unencrypted from http://10.10.13.14/data/ba/ppc64le/PRD0001289key.pub.asc
        Spectrum Protect Backup/Archive Client                                                                                1.6 MB/s | 1.6 kB     00:00    
        Importing GPG key 0xE58157A3:
         Userid     : "IBM Spectrum Protect Client <psirt@us.ibm.com>"
         Fingerprint: 701C 601D 5BF7 B238 5059 E068 CE71 1BB6 E581 57A3
         From       : http://10.10.13.14/data/ba/ppc64le/PRD0001289key.pub.asc
        Is this ok [y/N]: y
        Key imported successfully
        Running transaction check
        Transaction check succeeded.
        Running transaction test
        Transaction test succeeded.
        Running transaction
          Preparing        :                                                                                                                              1/1 
          Upgrading        : gskcrypt64-8.0-60.4.ppc64le                                                                                                  1/7 
          Running scriptlet: gskcrypt64-8.0-60.4.ppc64le                                                                                                  1/7 
          Upgrading        : gskssl64-8.0-60.4.ppc64le                                                                                                    2/7 
          Running scriptlet: gskssl64-8.0-60.4.ppc64le                                                                                                    2/7 
          Installing       : TIVsm-API64-8.2.0-0.ppc64le                                                                                                  3/7 
          Running scriptlet: TIVsm-API64-8.2.0-0.ppc64le                                                                                                  3/7 
          Installing       : TIVsm-BA-8.2.0-0.ppc64le                                                                                                     4/7 
          Running scriptlet: TIVsm-BA-8.2.0-0.ppc64le                                                                                                     4/7 
          Installing       : TIVsm-BAcit-8.2.0-0.ppc64le                                                                                                  5/7 
          Running scriptlet: gskssl64-8.0-55.31.ppc64le                                                                                                   6/7 
          Cleanup          : gskssl64-8.0-55.31.ppc64le                                                                                                   6/7 
          Running scriptlet: gskcrypt64-8.0-55.31.ppc64le                                                                                                 7/7 
          Cleanup          : gskcrypt64-8.0-55.31.ppc64le                                                                                                 7/7 
          Running scriptlet: TIVsm-BA-8.2.0-0.ppc64le                                                                                                     7/7 
          Running scriptlet: gskcrypt64-8.0-55.31.ppc64le                                                                                                 7/7 
          Verifying        : TIVsm-API64-8.2.0-0.ppc64le                                                                                                  1/7 
          Verifying        : TIVsm-BA-8.2.0-0.ppc64le                                                                                                     2/7 
          Verifying        : TIVsm-BAcit-8.2.0-0.ppc64le                                                                                                  3/7 
          Verifying        : gskcrypt64-8.0-60.4.ppc64le                                                                                                  4/7 
          Verifying        : gskcrypt64-8.0-55.31.ppc64le                                                                                                 5/7 
          Verifying        : gskssl64-8.0-60.4.ppc64le                                                                                                    6/7 
          Verifying        : gskssl64-8.0-55.31.ppc64le                                                                                                   7/7 
        Installed products updated.
        Last metadata expiration check: 0:00:30 ago on Mon 12 Jan 2026 01:59:17 PM CET.

        Upgraded:
          gskcrypt64-8.0-60.4.ppc64le                                                gskssl64-8.0-60.4.ppc64le                                               
        Installed:
          TIVsm-API64-8.2.0-0.ppc64le                       TIVsm-BA-8.2.0-0.ppc64le                       TIVsm-BAcit-8.2.0-0.ppc64le                      

        Complete!
        ```

Skoro klient BA jest już zainstalowany to może warto poczytać o jego [konfigurowaniu](../ISP/ba.md#konfiguracja-klienta-ba)?

:wink: