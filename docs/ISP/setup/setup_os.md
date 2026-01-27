---
icon: simple/linux
---

# Przygotowanie Linuxa pod pracę z IBM Spectrum Protect

Procedura instalacji ISP na hoscie linuxowym, mądrości zebrane i ciągle zbierane. Mam to ubrane w Ansibla. Opublikuję jak będzie miało ręce i nogi.

## Wymagania wstępne

Sprawdź [oficjalne wymagania](https://www.ibm.com/support/pages/overview-ibm-spectrum-protect-supported-operating-systems) na stronie IBM. 

Jeżeli plaujesz używać taśm IBM, to jedynymi praktycznymi dystrybucjami są SuSE i Red Hat. Wsparcie `lin_tape` na Ubuntu jest koszmarne. Tutaj skupiam się na Red Hat.

## Hostname i sieć

Host musi umieć rozwiązać swój `hostame` do swojego statycznego adresu. Albo przez DNS, albo przez `/etc/hosts`
W moim przypadku dopusuję takie wpisy do `/etc/hosts` (robię klaster, dlatego dodaję trzy wpisy):

```sh title="Dodawanie wpisów do /etc/hosts"
cat >> /etc/hosts << EOF
10.13.0.12      sp-n1 sp-n1.host-only
10.13.0.13      sp-n2 sp-n2.host-only
10.13.0.14      sp sp.host-only
EOF
```

## SELinux

`Disabled` albo `Permissive`. Po utworzeniu insancji można właczyć na `Enforcing`.

```sh title="Wyłączanie SELinuxa"
sudo setenforce 0       # Na teraz
sudo sed 's/^SELINUX=enforcing/SELINUX=permissive/' -i.bak /etc/sysconfig/selinux   # I na wieki wieków
```

## Pakiety

RHEL może być zainstalowany z profilu *Minimal Server*, ale będzie potrzebować jeszcze:

* `ksh`

Opcjonalne, ułatwiające życie:

* `motif` - daje `mwm`
* `xterm`
* `tigervnc-server` - choć w tej procedurze instaluję "na piechotę" ale jak by ktoś chciał tworzyć instancję przez przez `dsmicfgx`
* `tmux` - bo jest lepszy niż screen 
* `libnsl` - na RHEL8 może tego nie byc w minimalnej instalacji.

Jesli maszyna ma chodzić z taśmami IBM to:

* `kernel-devel` - wciągnie masę przyległości, w tym `gcc`.
* `rpm-build`

## Multipath na :IBM-bw: FlashSystems/SVC

Jeśli konfigurujesz przestrzeń z macierzy FlashSystem zajrzyj [tu](LNX/MPIO_Aand_SAN)

## Filesystemy

!!! Note "Info"
    Tu robię na dyskach qemu. W Dużych instalacjach zamiast `vdb`, `vdc` itd., będą aliasy z LUNów z macierzy. Ale idea jest ta sama: 1 dysk = 1 filesystem.

Układ filesystemówjest w miarę standardowy. W zależności od wielkości, będzie się rożnił liczbą dbspaceów i wielkośćią. W Ekstremalnych przypadkach, zdarza mi się `actlog` i `archlog` zakładać na stripowanych. 

Lista filesystemów i ich punków montowania:

| Urządzenie | VG     | LV        | MP            | Opis |
| :---       | :---   | :---      | :---          | :--- |
| `sdb`      | `spvg` | `instlv`  | `/sp/inst1`   | Katalog instancji |
| `sdc`      | `spvg` | `actlv`   | `/sp/actlog`  | Active log |
| `sdd`      | `spvg` | `archlv`  | `/sp/archlog` | Archive log log |
| `sde`      | `spvg` | `db01lv`  | `/sp/db/01`   | 1 dbspace bazy |
| `sdf`      | `spvg` | `db02lv`  | `/sp/db/02`   | 2 dbspace bazy |
| `sdg`      | `spvg` | `dbblv`   | `/sp/dbb`     | backup bazy |


??? Tip "Komendy podłaczające dyski do maszyny sp-n1"

    ```sh
    sudo virsh attach-disk sp-n1 /home/marcinek/media/Szajsung/vm/pcmk-inst.raw  sdb --driver qemu --type disk --config --live --subdriver raw --targetbus scsi
    sudo virsh attach-disk sp-n1 /home/marcinek/media/Szajsung/vm/pcmk-inst.raw  sda --driver qemu --type disk --config --live --subdriver raw --targetbus scsi
    sudo virsh attach-disk sp-n1 /home/marcinek/media/Szajsung/vm/pcmk-inst.raw  sdb --driver qemu --type disk --config --live --subdriver raw --targetbus scsi
    sudo virsh attach-disk sp-n1 /home/marcinek/media/Szajsung/vm/pcmk-actlog.raw  sdc --driver qemu --type disk --config --live --subdriver raw --targetbus scsi
    sudo virsh attach-disk sp-n1 /home/marcinek/media/Szajsung/vm/pcmk-archlog.raw  sdd --driver qemu --type disk --config --live --subdriver raw --targetbus scsi
    sudo virsh attach-disk sp-n1 /home/marcinek/media/Szajsung/vm/pcmk-db01.raw  sde --driver qemu --type disk --config --live --subdriver raw --targetbus scsi
    sudo virsh attach-disk sp-n1 /home/marcinek/media/Szajsung/vm/pcmk-db02.raw  sdf --driver qemu --type disk --config --live --subdriver raw --targetbus scsi
    sudo virsh attach-disk sp-n1 /home/marcinek/media/Szajsung/vm/pcmk-dbb.raw  sdg --driver qemu --type disk --config --live --subdriver raw --targetbus scsi
    ```

    Weryfikacja:

    ```sh
    sudo virsh domblklist sp-n1                                                                                  20:21:52
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

    !!! Warning "Uwaga"
        `virsh` i :simple-qemu: trochę kłamią. Dyski od strony hosta podłączą się od `sda` a nie od `sdb` - to, co na powyższym wydrukujest podane jako `sda` to CDROM widziany przez hosta jako `sr0`. 

1. Utwórz PVki na podłaczonych dyskach. Dla każdego dysku wykonaj:

    ```sh title="Zakładanie PV na dysku"
    sudo pvcreate /dev/DYSK
    ```

    ??? Example "Przykład"

        ```sh
        $ sudo pvcreate /dev/sda
        Physical volume "/dev/sda" successfully created.
        $ sudo pvcreate /dev/sdb
        Physical volume "/dev/sdb" successfully created.
        $ sudo pvcreate /dev/sdc
        Physical volume "/dev/sdc" successfully created.
        $ sudo pvcreate /dev/sdd
        Physical volume "/dev/sdd" successfully created.
        $ sudo pvcreate /dev/sde
        Physical volume "/dev/sde" successfully created.
        $ sudo pvcreate /dev/sdf
        Physical volume "/dev/sdf" successfully created.
        ```

1. Utwórz grupe `spvg`:

    ```sh title="Tworzenie grupy woluminów spvg"
    sudo vgcreate spvg lista wolumenów PV
    ```

    ??? Example "Przykład"

        ```sh title="Tworzenie grupy woluminów spvg"
        sudo vgcreate spvg /dev/sda /dev/sdb /dev/sdc /dev/sdd /dev/sde /dev/sdf
        ```

1. Utwórz logiczne woluminy według tabelki z początku tego rozdziału:

    ```sh title="Zakładanie LV 1:1 z PV"
    sudo lvcreate -n nazwa_LV -l 100%FREE spvg PV
    ```

    ??? Example "Przykład"

        ```sh
        sudo lvcreate -n instlv -l 100%FREE spvg /dev/sda
        sudo lvcreate -n actlv -l 100%FREE spvg /dev/sdb
        sudo lvcreate -n archlv -l 100%FREE spvg /dev/sdc
        sudo lvcreate -n db01lv -l 100%FREE spvg /dev/sdd
        sudo lvcreate -n db02lv -l 100%FREE spvg /dev/sde
        sudo lvcreate -n dbblv -l 100%FREE spvg /dev/sdf
        ```

1. Weryfikacja LVM:

    ```sh hl_lines="1"
    $ sudo lvs -o+devices 
      LV     VG   Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert Devices        
      home   rhel -wi-ao---- <20.70g                                                     /dev/vda2(1511)
      root   rhel -wi-ao----  42.39g                                                     /dev/vda2(6810)
      swap   rhel -wi-ao----   5.90g                                                     /dev/vda2(0)   
      actlv  spvg -wi-a----- <48.00g                                                     /dev/sdb(0)    
      archlv spvg -wi-a----- <48.00g                                                     /dev/sdc(0)    
      db01lv spvg -wi-a----- <64.00g                                                     /dev/sdd(0)    
      db02lv spvg -wi-a----- <64.00g                                                     /dev/sde(0)    
      dbblv  spvg -wi-a----- <64.00g                                                     /dev/sdf(0)    
      instlv spvg -wi-a----- <20.00g                                                     /dev/sda(0)
    ```

1. Sformatuj te woluminy na `XFS`:

    ```sh title="Formatowanie LV na XFS"
    sudo mks.xfs /dev/mapper/spvg-NAZWA
    ```

    ??? Example "Przykład"

        ```sh
        sudo mkfs.xfs /dev/mapper/spvg-instlv
        sudo mkfs.xfs /dev/mapper/spvg-actlv
        sudo mkfs.xfs /dev/mapper/spvg-archlv
        sudo mkfs.xfs /dev/mapper/spvg-db01lv
        sudo mkfs.xfs /dev/mapper/spvg-db02lv
        sudo mkfs.xfs /dev/mapper/spvg-dbblv
        ```

1. Utwórz punkty montowania:

    ```sh title="Tworzenie mount pointów"
    sudo mkdir -p /sp/{inst1,db/01,db/02,actlog,archlog,dbb}
    ```

1. Dopisz utworzone filesystemy do `/etc/fstab`

    ```sh title="Dodawanie wpisów do /etc/fstab"
    sudo cat >> /etc/fstab << EOF
    /dev/mapper/spvg-instlv     /sp/inst1           xfs     defaults    0 0
    /dev/mapper/spvg-actlv      /sp/actlog          xfs     defaults    0 0
    /dev/mapper/spvg-archlv     /sp/archlog         xfs     defaults    0 0
    /dev/mapper/spvg-db01lv     /sp/db/01           xfs     defaults    0 0
    /dev/mapper/spvg-db02lv     /sp/db/01           xfs     defaults    0 0
    /dev/mapper/spvg-dbblv      /sp/dbb             xfs     defaults    0 0
    EOF
    ```

1. Przeładuj `systemd`:

    ```sh title="Odświeżanie systemd"
    systemctl daemon-reload
    ```

1. Zamontuj utworzone filesystemy:

    ```sh title+"Montowanie wszystkiego co jest w /etc/fstab"
    mount -a 
    ```

1. Zweryfikuj czy wszystkie są:

    ```sh title="Weryfikacja montowań"
    df -h
    ```

    !!! Example "Przykład"
    
        ```sh
        [root@sp-n1 ~]# df -h 
        Filesystem               Size  Used Avail Use% Mounted on
        devtmpfs                 4.0M     0  4.0M   0% /dev
        tmpfs                    5.8G     0  5.8G   0% /dev/shm
        tmpfs                    2.3G  8.8M  2.3G   1% /run
        /dev/mapper/rhel-root     43G   12G   32G  27% /
        /dev/vda1                960M  441M  520M  46% /boot
        /dev/mapper/rhel-home     21G  271M   21G   2% /home
        tmpfs                    1.2G     0  1.2G   0% /run/user/1000
        /dev/mapper/spvg-instlv   20G  175M   20G   1% /sp/inst1
        /dev/mapper/spvg-actlv    48G  375M   48G   1% /sp/actlog
        /dev/mapper/spvg-archlv   48G  375M   48G   1% /sp/archlog
        /dev/mapper/spvg-db02lv   64G  489M   64G   1% /sp/db/01
        /dev/mapper/spvg-dbblv    64G  489M   64G   1% /sp/dbb
        ```

## Podsumowanie

Na tym etapie  maszynka powinna mieć:

- [x] ustawiony hostname i sieć,
- [x] (tymczasowo) wyłączonego SELinuxa,
- [x] zainstalowane dodatkowe pakiety,
- [x] założone filesystemy pod instancję,

    ```
    /sp
    ├── actlog
    ├── archlog
    ├── db
    │    ├── 01
    │    └── 02
    ├── dbb
    └── inst1
    ```
