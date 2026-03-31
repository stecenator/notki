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
    leapp preupgrade --target <_target_os_version_>
    ```

1. Przejrzyj raport i rozwiąż ewentualne problemy:

    ```sh title="PRzegląd raportu"
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
