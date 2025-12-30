---
icon: material/arrow-up-bold-hexagon-outline
---

# Upgrade serwera 

Upgrade, to zmiana pierwszej lub drugiej cyferki wersji. Zwykle wiąże się z koniecznością posiadania wersji z pakietem licencyjnym. Tutaj, na przykładzie skoku z 8.1.27 do 8.2.0, na :IBM-Power: IBM Power. 

## Wymagania

Pampers, jak zwykle:

- Backup bazy.
- Backup pul.
- Stare binarki (8.1.27), na wypadek konieczności reinstalacji.
- `devconfig.dat`
- `volhost.dat`
- User i hasło instancji. 
- Binakrki wersji docelowej, Takie z licencją. 

## Upgrade instancji stand-alone

!!! Note "Ważne"
    Od tego miejsca, instalację robisz jako `root`.

1. Upewnij się, że masz wszystko co jest podane w wymaganiach.
1. Zatrzymaj instancję tsm. U mnie to `spinst1`:

    ```sh title="Zatrzymanie instancji Protect"
    systemctl stop spinst1
    ```
1. Jeśli na tej maszynie działa też `OpsCenter`, jemu też daj w łeb:

    ```sh title="Zatrzymanie Operations Center"
    systemctl stop opscenter
    ```
1. Rozpakuj binarki serwera. Pamiętaj, że to self-extracting archiwum rozpakowuje się do bieżącego katalogu, więc warto stanąć w jakiśmś pustym. NA poniższym przykładzie jest tak:

    - Katalog roboczy (tu się rozpakują binarki): `/home/ibm/srv-8.2.0`.
    - Binarki leżą sobie na NFS: `sputnik:/data` w pliku `/data/protect/SP_8.2_PLIN_LE_SERSTG_AGT_ML.bin`
    - NFS jeest podmontowany pod lokalny katalog `/toys`

    ```sh hl_lines="4" title="Rozpakowanie binariów serwera"
    [root@sp-1 srv-8.2.0]# mount -o ro sputnik:/data /toys 
    [root@sp-1 srv-8.2.0]# pwd
    /home/ibm/srv-8.2.0
    [root@sp-1 srv-8.2.0]# /toys/protect/SP_8.2_PLIN_LE_SERSTG_AGT_ML.bin
    ```

2. Po rozpakowaniu, uruchom `./install.sh` - W zależności od ustawień, może próbować odaplić grafikę. Ja tu jadę tekstowo.

    ```sh title="Start instalatora IBM Storage Protect"
    ./install.sh
    ```

2. Z głównego menu wybierz `Update` wpisując `2` w prompt na dole:

    ``` hl_lines="5 21" title="Menu główne"
    =====> IBM Installation Manager

    Select:
         1. Install - Install software packages
         2. Update - Find and install updates and fixes to installed software packages
         3. Modify - Change installed software packages
         4. Roll Back - Revert to an earlier version of installed software packages
         5. Uninstall - Remove installed software packages

    Other Options:
         L. View Logs
         S. View Installation History
         V. View Installed Packages
            ------------------------
         P. Preferences
            ------------------------
         A. About IBM Installation Manager
            ------------------------
         X. Exit Installation Manager

    -----> 2
    ```

1. Instaltor powinien znaleźć grupę pakietów `IBM Spectrum Protect` (1)
    { .annotate }

    1. :IBM-bw: sam nie bardzo się orientuje ile razy zmienił nazwę temu produktowi :shrug:. Oczywiście powinno być `IBM Storage Protect`.

    ``` hl_lines="17" title="Wybór grupy pakietów do aktuallizacji"
    =====> IBM Installation Manager> Update

    Select a package group to update:
         1. [X] IBM Spectrum Protect

    Details of package group IBM Spectrum Protect:
      Package Group Name         :  IBM Spectrum Protect
      Shared Resources Directory :  /opt/IBM/IBMIMShared
      Installation Directory     :  /opt/tivoli/tsm
      Translations               :  English

    Other Options:
         U. Update All
         A. Unselect All

         N. Next,      C. Cancel
    -----> [N] 
    ```

    Po prostu trzepnij `Enter`.

1. Instalator pkarze znalezione w systemie pakiety godne aktualizacji.

    !!! Info "Zwróć uwagę"
        1. Aktualizowany jest także pakiet `IBM Spectrum Protect license`.
        1. Na tym przykładzie nie ma niektórych pakietów, np `OSSM`, `Device Driver` czy `Languages`. U Ciebie mogą być.

    ``` hl_lines="18" title="Lista kandydatów do aktualizacji"
    =====> IBM Installation Manager> Update> Packages

    Package group:  IBM Spectrum Protect

    Update packages:
         1-. [X] IBM Storage Protect server 8.1.27.20250611_1345
           2. [X] Version 8.2.0.20251121_0614
         3-. [X] IBM Spectrum Protect license 8.1.10.20200521_1450
           4. [X] Version 8.2.0.20251121_0609
         5-. [X] IBM Storage Protect Operations Center 8.1.27000.20250527_1128
           6. [X] Version 8.2.0.20251111_1045

    Other Options:
         A. Show All
         R. Select Recommended

         B. Back,      N. Next,      C. Cancel
    -----> [N] 
    ```

    Naciśnij `Enter`. Na ekranie z **Features** też. 

1. Ostatnie sprawdzenie, czy wszystko OK, i naciśnij `Enter`, żeby rozpocząć *upgrade*:

    ``` hl_lines="17" title="Podsumowanie"
    =====> IBM Installation Manager> Update> Packages> Features> Summary

    Target Location:
      Shared Resources Directory :  /opt/IBM/IBMIMShared
    Update packages:
         1-. IBM Spectrum Protect (/opt/tivoli/tsm)
           2. IBM Storage Protect server 8.1.27.20250611_1345
           3. IBM Spectrum Protect license 8.1.10.20200521_1450
           4-. IBM Storage Protect Operations Center 8.1.27000.20250527_1128
             5-. Features to install:
               6. Operations Center

    Options:
         G. Generate an Update Response File

         B. Back,      U. Update,      C. Cancel
    -----> [U] 

    ```


    !!! Tip "Podpowiedź"
        Jeśli planujesz aktualizację kliku instancji, być może warto skorzystać z opcji `G. Generate an Update Response File`. Wtedy aktualizację pozostałych instancji możesz oskryptować. 

1. Po zakończonej instalacji możęsz przejrzeć logi, albo po prostu klepnąć  `Enter-X-Enter`, żeby wyjść z instalatora.

    ``` title="Podsomowanie wyników instalacji"
                         25%                50%                75%                100%
    ------------------|------------------|------------------|------------------|
    ............................................................................

    =====> IBM Installation Manager> Update> Packages> Features> Summary> 
      Completion

    The update completed successfully.

    INFORMATION: To learn about best practices for configuring, monitoring, and operating an IBM Storage Protect solution, go to IBM Documentation:
    https://www.ibm.com/docs/en
    Search for IBM Storage Protect data protection solutions.

    Options:
         F. Finish
    -----> [F]
    ```

1. Wystartuj ponownie usługi.

    !!! Warning "Ważne"
        Tym razem nie było grubej aktualizacji bazy, ale czasem, gdy instalator poprosi o kredki właściciela instancji, warto po aktualizacji uruchomić serwer w trybie *maintenance*, bo wtedy że serwer wykonuje dodatkowe, jednorazowe czynności na bazie, a nie wisi :smile:.
        <br>
        Jako user instancji, wystartuj serwer tak:  `dsmserv -i /katalog/instancji/serwera maintenance`.

    ``` sh title="Start zaktualizowanych usług"
    systemctl start spinst1
    systemctl start opscenter
    ```

## Upgrade instancji w klastrze Pacemaker

