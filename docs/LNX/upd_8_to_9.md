---
icon: simple/redhat
---

# Aktualizacja RHEL 8.10 do 9.7

!!! Tip "Wskazówka"
    Źródłem mądrości jest ten [link](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/upgrading_from_rhel_8_to_rhel_9/assembly_preparing-for-the-upgrade_upgrading-from-rhel-8-to-rhel-9)

1. Sprawdź status rejestracji:
    
    ```sh title="Status rejestracji"
    sudo subscription-manager status
    ```
1. Sprawdź jakie pridukty RH są zainstalowane:

    ```sh title="Lista zainstalowanch pruduktów RH"
    sudo subscription-manager list --installed
    ```

    ??? Example "Przykład"
        ```sh

        ```
1. Zaktualizuj system do 8.10. W razie czego _reboot_ is always good.
1. Zabolkuj wersję OS na 8.10:

    ```sh title="Blokada na 8.10"
    sudo subscription-manager release --set 8.10
    ```

1. Zainstaluj narzędzie `leapp`:

    ```sh title="Instalacja leapp"
    sudo dnf install leapp-upgrade
    ```

    ??? Example "Przykład"
        ```sh
        $ sudo dnf install leapp-upgrade
        Updating Subscription Management repositories.
        Red Hat Enterprise Linux 8 for x86_64 - BaseOS (RPMs)                                           36 MB/s | 125 MB     00:03
        Red Hat Enterprise Linux 8 for x86_64 - AppStream (RPMs)                                        23 MB/s |  81 MB     00:03
        Red Hat Enterprise Linux 8 for x86_64 - High Availability (RPMs)                               4.2 MB/s | 7.2 MB     00:01
        Dependencies resolved.
        ===============================================================================================================================
         Package                              Architecture    Version                  Repository                                 Size
        ===============================================================================================================================
        Installing:
         leapp-upgrade-el8toel9               noarch          0.23.0-1.el8_10          rhel-8-for-x86_64-appstream-rpms          1.4 M
        Installing dependencies:
         leapp                                noarch          0.20.0-1.el8_10          rhel-8-for-x86_64-appstream-rpms           35 k
         leapp-deps                           noarch          0.20.0-1.el8_10          rhel-8-for-x86_64-appstream-rpms           17 k
         leapp-upgrade-el8toel9-deps          noarch          0.23.0-1.el8_10          rhel-8-for-x86_64-appstream-rpms           46 k
         python3-leapp                          Updating Subscription Management repositories.
        Red Hat Enterprise Linux 8 for x86_64 - BaseOS (RPMs)                                           36 MB/s | 125 MB     00:03
        Red Hat Enterprise Linux 8 for x86_64 - AppStream (RPMs)                                        23 MB/s |  81 MB     00:03
        Red Hat Enterprise Linux 8 for x86_64 - High Availability (RPMs)                               4.2 MB/s | 7.2 MB     00:01
        Dependencies resolved.
        ===============================================================================================================================
         Package                              Architecture    Version                  Repository                                 Size
        ===============================================================================================================================
        Installing:
         leapp-upgrade-el8toel9               noarch          0.23.0-1.el8_10          rhel-8-for-x86_64-appstream-rpms          1.4 M
        Installing dependencies:
         leapp                                noarch          0.20.0-1.el8_10          rhel-8-for-x86_64-appstream-rpms           35 k
         leapp-deps                           noarch          0.20.0-1.el8_10          rhel-8-for-x86_64-appstream-rpms           17 k
         leapp-upgrade-el8toel9-deps          noarch          0.23.0-1.el8_10          rhel-8-for-x86_64-appstream-rpms           46 k
         python3-leapp                        noarch          0.20.0-1.el8_10          rhel-8-for-x86_64-appstream-rpms          202 k

        Transaction Summary
        ===============================================================================================================================
        Install  5 Packages

        Total download size: 1.7 M
        Installed size: 13 M
        Is this ok [y/N]: y
        noarch          0.20.0-1.el8_10          rhel-8-for-x86_64-appstream-rpms          202 k

        Transaction Summary
        ===============================================================================================================================
        Install  5 Packages

        Total download size: 1.7 M
        Installed size: 13 M
        Is this ok [y/N]: y
        ```

1. Sprawdź czy są jakieś pliki `.rpmnew` i `rpmsave`. I jakoś się ich pozbądź. Jeśli nie są istotne to je por prostu wywal.
    
    ```sh hl_lines="1 3" title="Pliki rpmsave i rpmnew"
    $ sudo find / -name \*rpmnew
    /etc/pam.d/smartcard-auth.rpmnew
    $ sudo find / -name \*rpmsave
    /etc/cups/cups-browsed.conf.rpmsave
    ```

1. Uruchom raport weryfikujący czy można się podnieść:

    ```sh title="Preupgrade"
    sudo leapp preupgrade --target 9.7
    ```

1. Przejrzyj raport i rozwiąż ewentualne problemy:

    ```sh title="Przegląd raportu"
    sudo less /var/log/leapp/leapp-report.txt
    ```

    Typowe problemy to:

    - Paczki podpisane SHA-1
    - Obce paczki (zwykle mało ważne)
    - Paczki "deprecated"

        Paczki zwykle można usunąć. Klienta TSM można zostawić, Będzie działać na nowwym OSie.

    - Konfiguracja [firewalla](https://access.redhat.com/articles/4855631)

        ```sh title="Weryfikacja"
        cat /etc/firewalld/firewalld.conf | grep -i AllowZoneDrifting
        ```

        Jak wyskoczy, że `yes`, to:

        ```sh title="Wyłączenie zonedriftingu"
        sudo sed -i "s/^AllowZoneDrifting=.*/AllowZoneDrifting=no/" /etc/firewalld/firewalld.conf
        ```

    - Konfiguracja [ssh](https://access.redhat.com/solutions/7003083) 

        Dodaj komentarz za `PermitRootLogin yes`, to leapp się odpierdoli. 

1. Puść upgrade:

    ```sh title="Upgrade!"
    leapp upgrade
    ```

!!! Danger "Ważne"
    Jeśli na upgradowanej maszynie był zainstalowany IBM Storage Protect, to jego wewnętrzne DB2 może po aktualizacji się nie podnieść. Zwykle robi to z niewiele mówiącym komunikatem:

    ```sh hl_lines="22 23" title="Wyjebka TSM"
    [tsminst1@tsm-b2 ~]$ dsmserv  -i /tsm/tsminst1 maintenance                                                                                                                                                           
    ANR7800I DSMSERV generated at 19:53:21 on Oct 15 2025.                                                                                                                                                               
                                                                                                                                                                                                                         
    IBM Storage Protect for Linux/x86_64                                                                                                                                                                                 
    Version 8, Release 1, Level 27.100                                                                                                                                                                                   
                                                                                                                                                                                                                         
    Licensed Materials - Property of IBM                                                                                                                                                                                 
                                                                                                                                                                                                                         
    (C) Copyright IBM Corporation 1990, 2025.                                                                                                                                                                            
    All rights reserved.                                                                                                                                                                                                 
    U.S. Government Users Restricted Rights - Use, duplication or disclosure                                                                                                                                             
    restricted by GSA ADP Schedule Contract with IBM Corporation.                                                                                                                                                        
                                                                                                                                                                                                                         
    ANR7801I Subsystem process ID is 787152.                                                                                                                                                                             
    ANR0900I Processing options file /tsm/tsminst1/dsmserv.opt.                                                                                                                                                          
    ANR0010W Unable to open message catalog for language en_US.UTF-8. The default language message catalog will be used.                                                                                                 
    ANR7814I Using instance directory /tsm/tsminst1.                                                                                                                                                                     
    ANR3339I Default Label in key data base is TSM Server SelfSigned SHA Key.                                                                                                                                            
    ANR4726I The ICC support module has been loaded.                                                                                                                                                                     
    ANR0990I Server restart-recovery in progress.                                                                                                                                                                        
    ANR0302W Server monitoring has been disabled by option.                                                                                                                                                              
    ANR0236E Fail to start the database manager due to an I/0 error. Check for filesystem full conditions, file permissions, and operating system errors.                                                                
    ANR0162W Supplemental database diagnostic information:  -1:08001:-1032 ([IBM][CLI Driver] SQL1032N  No start database manager command was issued.  SQLSTATE=57019 
    ```

    W takiej sytuacji sprawdź czy nie zgubiła się biblioteka `compat-openssl11`

    ```sh title="Instalacja brakującej biblioteki"
    dnf install compat-openssl11
    ```