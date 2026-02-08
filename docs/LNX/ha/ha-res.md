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

## Dodawanie istniejącej grupy woluminów

!!! Danger "Uwaga"
    Upewnij się, że podłaćzana do pozostałych węzłów klastra grupa jest zdeaktywowana na węźle, który ją utworzył!
    Proces deaktywacji jest opisany [tutaj](os-setup.md).

1. Upewnij się, że oba węzły klastra widzą wpólne dyski. Ogólna metoda dodawania dysków do maszyn KVM jest opisana [tutaj](/virt/libvirt.md#odaczanie-dysku-od-dziaajacej-vmki). W moim przykładzie jest tak, że dyski u grupa woluminów są na maszynie `sp-n1` i dodaję je do węzła `sp-n1`. Poniższe komendy wykonuj na hoście KVM:

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

 