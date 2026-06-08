---
# icon: material/package-variant-closed-plus
icon: ha-rg
---

# Zasoby klastra

Do klastra zostaną dodane następujące zasoby:

- Filesystemy ze współdzoielnonych dysków,
- VIP usługi `sp`,
- Instancja IBM Storage Protect `spinst1`.

Zasoby zostaną zgrupowane do jednej do dwóch grup zasobów:

!!! Note inline end "Zwróć uwagę"
    Ponieważ nie ma jeszcze grupy zasobów `spinst1-rg`, zostanie ona utworzona przy pierwszym dodaniu zasobu do grupy:smile:.

- `spinst1-rg`, która będzie zawierać następujące zasoby:
    - Grupę LVM: `spvg`
    - Grupę LVM: `dpvg`
    - Adres IP: `sp.host-only`
    - Usługę systemd: `spinst1` startującą instancję.
- `oc-rg`, która bęie zawierać:
    - Usługę systemd: `opscenter` startującą _Operations Center_.
    - Adres IP: `oc.host-only`


## Dodawanie IP

1. Dodaj IP klastra do grupy zasobów `spinst1-rg`:

    ```sh title="dodawanie IP do spinst1-rg"
    pcs resource create VIP_SAN ocf:heartbeat:IPaddr2 ip=192.168.1.31 --group sp01
    ```

## Dodawanie istniejącej grupy woluminów

!!! Danger "Uwaga"
    Upewnij się, że podłaćzana do pozostałych węzłów klastra grupa jest zdeaktywowana na węźle, który ją utworzył!
    Proces deaktywacji jest opisany [tutaj](os-setup.md).

1. Upewnij się, że oba węzły klastra widzą wpólne dyski. Ogólna metoda dodawania dysków do maszyn KVM jest opisana [tutaj](../../virt/libvirt.md#odaczanie-dysku-od-dziaajacej-vmki). W moim przykładzie jest tak, że dyski u grupa woluminów są na maszynie `sp-n1` i dodaję je do węzła `sp-n1`. Poniższe komendy wykonuj na hoście KVM:

    ```sh hl_lines="1" title="Przejżyj podpięte do źsódłowego noda dyski"
    $ sudo virsh domblklist sp-n1
     Target   Source
    -------------------------------------------------------------
     vda      /home/marcinek/media/Szajsung/vm/sp-n1-os.qcow2
     sda      -
     sdb      /home/marcinek/media/Szajsung/vm/pcmk-inst.raw
     sdc      /home/marcinek/media/Szajsung/vm/pcmk-actlog.raw
     sdd      /home/marcinek/media/Szajsung/vm/pcmk-archlog.raw
     sde      /home/marcinek/media/Szajsung/vm/pcmk-db01.raw
     sdf      /home/marcinek/media/Szajsung/vm/pcmk-db02.raw
     sdg      /home/marcinek/media/Szajsung/vm/pcmk-dbb.raw
    ```

1. Podpnij je w tej samej kolejnonści do noda `sp-n2`:

    ```sh title="Dodwanie dysków do drugiego węzła klastra"
    sudo virsh attach-disk sp-n2 /home/marcinek/media/Szajsung/vm/pcmk-inst.raw sdb --driver qemu --type disk --config --live --subdriver raw --targetbus scsi --shareable
    sudo virsh attach-disk sp-n2 /home/marcinek/media/Szajsung/vm/pcmk-actlog.raw sdc --driver qemu --type disk --config --live --subdriver raw --targetbus scsi --shareable
    sudo virsh attach-disk sp-n2 /home/marcinek/media/Szajsung/vm/pcmk-archlog.raw sdd --driver qemu --type disk --config --live --subdriver raw --targetbus scsi --shareable
    sudo virsh attach-disk sp-n2 /home/marcinek/media/Szajsung/vm/pcmk-db01.raw sde --driver qemu --type disk --config --live --subdriver raw --targetbus scsi --shareable
    sudo virsh attach-disk sp-n2 /home/marcinek/media/Szajsung/vm/pcmk-db02.raw sdf --driver qemu --type disk --config --live --subdriver raw --targetbus scsi --shareable
    sudo virsh attach-disk sp-n2 /home/marcinek/media/Szajsung/vm/pcmk-dbb.raw sdg --driver qemu --type disk --config --live --subdriver raw --targetbus scsi --shareable
    ```

1. W RH domyślnie jest włączone `use_devicesfile =1` w `lvm.conf`, dlatego trzeba dodać te dyski do LVM komendą `sudo lvmdevices --adddev /dev/dbXX`.

    !!! Note inline end
        Pewnie jest na to ładniejszy sposób, ale po dodaniu tych urządzeń do LVM po prostu restatuję, a LVM sobie wykrywa tę grupę.

    ```sh title="Dodawanie nowych dysków do LVM"
    sudo lvmdevices --adddev /dev/sdb
    sudo lvmdevices --adddev /dev/sdc
    sudo lvmdevices --adddev /dev/sdd
    sudo lvmdevices --adddev /dev/sde
    sudo lvmdevices --adddev /dev/sdf 
    ```

1. Dodaj grupę `spvg`

    ```sh title="Towrzenie zasobu spvg w grupie spinst1-rg"
    sudo pcs resource create spvg_lvm ocf:heartbeat:LVM-activate vgname=spvg vg_access_mode=system_id --group spinst1-rg
    ```
1. Dodaj filesystemy do grupy `spinst-rg`:

    ```sh title="Dodawanie filesystemu do grupy zasobów"
    pcs resource create fs_sp_db_db01 ocf:heartbeat:Filesystem device=/dev/spvg/db01lv directory=/sp/db/db01 fstype=xfs --group spinst1-rg
    ```

    Zrób to dla wszytkich filesystemów grupy `spvg`, a jeśli masz też grupę pod storage pulę, to jej fileststemy też dodaj.

## Dodawanie aplikacji do klastra.

Ponieważ dodawanie IBM Storage Protect do klastra wiąże się z __katalogowaniem instancji__ na drugim węźle, przeczytaj [tę dokumentację](https://www.ibm.com/docs/en/storage-protect/8.2.0?topic=components-configuring-secondary-node).

!!! Warning "Uwaga!"

    Isntancja SP powinna już być skonfigurowana na pierwszym węźle klastra, np przy pomocy [tych](https://www.ibm.com/docs/en/storage-protect/8.2.0?topic=is-taking-first-steps-after-you-install-storage-protect) kroków.

1. Upewnij się, że grupa zasobów jest przerzucona na konfigurowany węzeł:

    !!! Tip "Wskazówka"
        Najprościej przerzucić grupę zasobów poprzez postawienie pierwszego węzł klastra w tryb __standby__.

        ```sh title="sp01-n1 do standby"
        pcs node standby sp01-n1
        ```

    ```sh title="Status grupy zasobów"
    pcs status
    ```

    ??? Example "Przykład"
        ```sh
        pcs status 
        Cluster name: sp01
        Cluster Summary:
          * Stack: corosync (Pacemaker is running)
          * Current DC: sp01-n1 (version 2.1.10-1.1.el9_7-5693eaeee) - partition with quorum
          * Last updated: Wed Mar 25 11:24:51 2026 on sp01-n2
          * Last change:  Tue Mar 24 16:09:05 2026 by root via root on sp01-n1
          * 2 nodes configured
          * 16 resource instances configured

        Node List:
          * Node sp01-n1: standby
          * Online: [ sp01-n2 ]

        Full List of Resources:
          * Resource Group: sp01:
            * VIP_SAN   (ocf:heartbeat:IPaddr2):         Started sp01-n2
            * VIP_GPFS  (ocf:heartbeat:IPaddr2):         Started sp01-n2
            * vg_spvg   (ocf:heartbeat:LVM-activate):    Started sp01-n2
            * vg_hddvg  (ocf:heartbeat:LVM-activate):    Started sp01-n2
            * fs_sp_spinst1     (ocf:heartbeat:Filesystem):      Started sp01-n2
            * fs_sp_db_db01     (ocf:heartbeat:Filesystem):      Started sp01-n2
            * fs_sp_db_db02     (ocf:heartbeat:Filesystem):      Started sp01-n2
            * fs_sp_db_db03     (ocf:heartbeat:Filesystem):      Started sp01-n2
            * fs_sp_db_db04     (ocf:heartbeat:Filesystem):      Started sp01-n2
            * fs_sp_actlog      (ocf:heartbeat:Filesystem):      Started sp01-n2
            * fs_sp_archlog     (ocf:heartbeat:Filesystem):      Started sp01-n2
            * fs_sp_dbb (ocf:heartbeat:Filesystem):      Started sp01-n2
            * fs_sp_bkpdp_01    (ocf:heartbeat:Filesystem):      Started sp01-n2
            * fs_sp_bkpdp_02    (ocf:heartbeat:Filesystem):      Started sp01-n2
            * fs_sp_hsmdp_02    (ocf:heartbeat:Filesystem):      Started sp01-n2
            * fs_sp_hsmdp_01    (ocf:heartbeat:Filesystem):      Started sp01-n2

        Daemon Status:
          corosync: active/disabled
          pacemaker: active/disabled
          pcsd: active/enabled
        ```

        Dla pewności, sortwadź też czy OS widzi filesystemy:

        ```
        # df -h
        Filesystem                   Size  Used Avail Use% Mounted on
        devtmpfs                     4.0M     0  4.0M   0% /dev
        tmpfs                         63G   33M   63G   1% /dev/shm
        tmpfs                         26G  9.8M   26G   1% /run
        efivarfs                     512K  116K  392K  23% /sys/firmware/efi/efivars
        /dev/mapper/rhel97e-root     122G   12G  111G  10% /
        /dev/mapper/tsmb2            960M  107M  854M  12% /boot
        /dev/mapper/tsmb1           1022M  7.4M 1015M   1% /boot/efi
        tmpfs                         13G     0   13G   0% /run/user/0
        /dev/mapper/rhel-root         70G   19G   52G  27% /mnt/oldroot
        /dev/mapper/spvg-spinst1lv    20G  271M   20G   2% /sp/spinst1
        /dev/mapper/spvg-db01lv       64G  1.8G   63G   3% /sp/db/db01
        /dev/mapper/spvg-db02lv       64G  1.8G   63G   3% /sp/db/db02
        /dev/mapper/spvg-db03lv       64G  1.8G   63G   3% /sp/db/db03
        /dev/mapper/spvg-db04lv       64G  1.8G   63G   3% /sp/db/db04
        /dev/mapper/spvg-actloglv    148G  129G   20G  88% /sp/actlog
        /dev/mapper/hddvg-archloglv  640G  5.8G  634G   1% /sp/archlog
        /dev/mapper/hddvg-dbblv      640G  4.5G  636G   1% /sp/dbb
        /dev/mapper/hddvg-bkpdp01lv  100G   47G   54G  47% /sp/bkpdp/01
        /dev/mapper/hddvg-bkpdp02lv  100G   55G   46G  55% /sp/bkpdp/02
        /dev/mapper/hddvg-hsmdp02lv  1.5T   11G  1.5T   1% /sp/hsmdp/02
        /dev/mapper/hddvg-hsmdp01lv  1.5T   11G  1.5T   1% /sp/hsmdp/01
        ```

1. Upewnij się, że użytkownik instancji ma ten sam UID na obu maszynach.
1. Sprawdź i ewentualnie popre=raw uprawnienia do plików w katalogu `/sp`. Po zamontowaniu filesystemów, włascicleme punktów montowania możę być `root`, a ma być `spinst`.

    ```sh title="Uprawnienia do punktów montowania"
    # ls -la /sp/
    total 4
    drwxr-xr-x   9 root    root      97 Mar 24 11:38 .
    dr-xr-xr-x. 19 root    root     265 Mar 24 11:38 ..
    drwxr-xr-x   3 spinst1 spinst1   22 Sep 14  2023 actlog
    drwxr-xr-x   3 spinst1 spinst1   21 Sep 14  2023 archlog
    drwxr-xr-x   4 root    root      26 Mar 24 11:38 bkpdp
    drwxr-xr-x   6 root    root      54 Mar 24 11:38 db
    drwxr-xr-x   2 spinst1 spinst1    6 Apr 17  2024 dbb
    drwxr-xr-x   4 root    root      26 Mar 24 11:38 hsmdp
    drwxr-xr-x   5 spinst1 spinst1 4096 Mar 24 12:17 spinst1
    ```

    Jest źle. Popraw to:

    ```sh hl_lines="1 2" title="Leperowanie uprawnień"
    [root@sp01-n2 ~]# chown -R spinst1:spinst1 /sp/*
    [root@sp01-n2 ~]# ls -la /sp/
    total 4
    drwxr-xr-x   9 root    root      97 Mar 24 11:38 .
    dr-xr-xr-x. 19 root    root     265 Mar 24 11:38 ..
    drwxr-xr-x   3 spinst1 spinst1   22 Sep 14  2023 actlog
    drwxr-xr-x   3 spinst1 spinst1   21 Sep 14  2023 archlog
    drwxr-xr-x   4 spinst1 spinst1   26 Mar 24 11:38 bkpdp
    drwxr-xr-x   6 spinst1 spinst1   54 Mar 24 11:38 db
    drwxr-xr-x   2 spinst1 spinst1    6 Apr 17  2024 dbb
    drwxr-xr-x   4 spinst1 spinst1   26 Mar 24 11:38 hsmdp
    drwxr-xr-x   5 spinst1 spinst1 4096 Mar 24 12:17 spinst1
    ```
1. Utwórz instancję DB2 na drugim węźle klastra:

    ```sh title="Tworzenie instancji DB2"
    /opt/tivoli/tsm/db2/instance/db2icrt -a server -u spinst1 spinst1
    ```

    ??? Example "Przykład"

        ```sh title="Tworznie instancji DB2"
        [root@sp01-n2 ~]# /opt/tivoli/tsm/db2/instance/db2icrt -a server -u spinst1 spinst1
        DBI1446I  The db2icrt command is running.


        DB2 installation is being initialized.

         Total number of tasks to be performed: 4 
        Total estimated time for all tasks to be performed: 309 second(s) 

        Task #1 start
        Description: Setting default global profile registry variables 
        Estimated time 1 second(s) 
        Task #1 end 

        Task #2 start
        Description: Initializing instance list 
        Estimated time 5 second(s) 
        Task #2 end 

        Task #3 start
        Description: Configuring DB2 instances 
        Estimated time 300 second(s) 
        Task #3 end 

        Task #4 start
        Description: Updating global profile registry 
        Estimated time 3 second(s) 
        Task #4 end 

        The execution completed successfully.

        For more information see the DB2 installation log at
        "/tmp/db2icrt.log.1572819".
        DBI1070I  Program db2icrt completed successfully.
        ```

1. Zaktualizuj domyslną scieżkę baz danych:

    !!! Warning "Uwaga"
        Wszystkie operacje na database managerze i bazie trzeba zrobić jako właściciel instancji, czylu `spinst1`.

    ```sh title="Aktualizacja DBMGRa"
    db2 update dbm cfg using dftdbpath /sp/spinst1
    ```

    ??? Example "Przykład"
        ```sh hl_lines="1 3"
        [root@sp01-n2 ~]# su - spinst1 
        Last login: Wed Mar 25 11:47:30 CET 2026 on pts/2
        [spinst1@sp01-n2 ~]$ db2 update dbm cfg using dftdbpath /sp/spinst1
        DB20000I  The UPDATE DATABASE MANAGER CONFIGURATION command completed 
        successfully.
        ```

1. Skataloguj bazę `TSMDB1`:

    ```sh title="Katalogowanie bazy TSMDB1"
    db2 catalog db tsmdb1 
    ```

    ??? Example "Przykład"

        ```sh
        [spinst1@sp01-n2 ~]$ db2 list db directory

         System Database Directory

         Number of entries in the directory = 1

        Database 1 entry:

         Database alias                       = TSMDB1
         Database name                        = TSMDB1
         Local database directory             = /sp/spinst1
         Database release level               = 15.00
         Comment                              =
         Directory entry type                 = Indirect
         Catalog database partition number    = 0
         Alternate server hostname            =
         Alternate server port number         =

        ```
1. Sprawdź, czy wszystkie pliki potrzebne do startu są na miejscu. W razie potrzeby skopiuj je z pierwszego węzła

    - `/etc/systemd/system/spinst1.service`
    - `/opt/tivoli/tsm/server/bin/spinst1`
    - `/opt/tivoli/tsm/server/bin/dbbkapi/dsm.sys`

    Jeżeli kopiowałeś `spinst1.service`, to przeładuj systemd:

    ```sh
    systemctl daemon-reload
    ```

1. Dodaj do klastra usługę `spinst1.servce`:

    !!! Warning "Uwaga"
        Po dodaniu zasobu do klastra, Pacemaker natychiast go wystartuje!

    ```sh title="Dodawanie spinst1 do klastra"
    pcs resource create inst_spinst1 systemd:spinst1 --group sp01
    ```

    ??? Example "Przykład"

        ```sh hl_lines="1 3 8 18 20"
        [root@sp01-n2 ~]# pcs resource create inst_spinst1 systemd:spinst1 --group sp01
        Deprecation Warning: Using '--group' is deprecated and will be replaced with 'group' in a future release. Specify --future to switch to the future behavior.
        [root@sp01-n2 ~]# systemctl status spinst1 
        ● spinst1.service - Cluster Controlled spinst1.service
             Loaded: loaded (/etc/systemd/system/spinst1.service; disabled; preset: disabled)
            Drop-In: /run/systemd/system/spinst1.service.d
                     └─50-pacemaker.conf
             Active: active (exited) since Wed 2026-03-25 12:20:39 CET; 5s ago
            Process: 1749375 ExecStart=/opt/tivoli/tsm/server/bin/spinst1 start (code=exited, status=0/SUCCESS)
           Main PID: 1749375 (code=exited, status=0/SUCCESS)
                CPU: 78ms

        Mar 25 12:20:34 sp01-n2 systemd[1]: Starting Cluster Controlled spinst1.service...
        Mar 25 12:20:34 sp01-n2 su[1749378]: (to spinst1) root on none
        Mar 25 12:20:34 sp01-n2 su[1749378]: pam_unix(su-l:session): session opened for user spinst1(uid=1001) by (uid=0)
        Mar 25 12:20:39 sp01-n2 spinst1[1749375]: Starting dsmserv instance spinst1 ... Succeeded
        Mar 25 12:20:39 sp01-n2 systemd[1]: Finished Cluster Controlled spinst1.service.
        [root@sp01-n2 ~]# ps -ef | grep dsmserv 
        root     1749378       1  0 12:20 ?        00:00:00 su - spinst1 -c nohup /opt/tivoli/tsm/server/bin/dsmserv  -i /sp/spinst1 -q
        spinst1  1749463 1749378  0 12:20 ?        00:00:00 /opt/tivoli/tsm/server/bin/dsmserv -i /sp/spinst1 -q
        spinst1  1749753 1749463  0 12:20 ?        00:00:00 /opt/tivoli/tsm/server/bin/servermon/servermon -path=/sp/spinst1/ -dbalias=TSMDB1 -schema=TSMDB1 -instance=spinst1 -optFile=/sp/spinst1/dsmserv.opt -installdir=/opt/tivoli/tsm/server/bin/servermon -dsmservId=1749463
        root     1751455 1407985  0 12:20 pts/2    00:00:00 grep --color=tty -d skip dsmserv
        ```

### Przywrócenie działania na pierwszym weźłe

Jeśli wymuszano przenieszieni zasobów na drugi węzeł przypomocyy `pcas stanby node` to można go teraz odstendbajowć :wink:.

```sh title="Przywrócenie pierwszego noda do klastra"
pcs node unstandby sp01-n1
```