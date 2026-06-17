---
icon: fontawesome/solid/gears
---

# Instalacja i konfiguracja instancji :IBM-bw: Storage Protect

!!! Tip inline end "AIX"
	AIXowcy też mają tu czego szukać.

Procedura instalacji ISP na hoscie linuxowym, mądrości zebrane i ciągle zbierane. Mam to ubrane w Ansibla. Opublikuję jak będzie miało ręce i nogi.

## Założenia

Z grubsza pasują do tego co :IBM-bw: opisał w [blueprintach](https://www.ibm.com/support/pages/ibm-storage-protect-blueprints). Podsumowując

<div class="grid cards" markdown>

-   :simple-redhat:{ .lg .middle } __OS: Red Hat 9__

    ---

    W tych przykładach, sklonowany według [tego artykułu](../../virt/qemu-img.md#konwersja-zlinkowanego-klona-do-niezaleznej-kopii). Oczywiście w dużych instalacjach, na LPARze lub gołym żelazie. 

-   :material-ip-network:{ .lg .middle } __Sieć__

    ---

    Na statycznych adresach. Warto zainstersować się [bondingiem](../../LNX/net.md#bonding-na-linuxie).


-   :material-harddisk:{ .lg .middle } __Dyski__

    ---

    Zasada: 1 LUN, 1 filesystem. Nawet w LVM. Protect sam sobie dobrze stripuje.

-   :fontawesome-solid-hands-holding-circle:{ .lg .middle } __[Serwer :IBM-bw: Storage Protect](#szczegoy-zaozen)__

    ---

    :IBM-bw: Storage Protect na oddzielnej grupie woluminów, na dedykowanym użyszkodniku. Takie zapakowanie pozwala na łatwe zapakowanie całości do klastra, albo przenoszenie pomiędzy maszynami.

</div>

## Spis treści

1. [Przygotowanie OS pod instalację](setup_os.md)
1. [Kartalogi i filesystemy](setup_os.md#filesystemy)
1. [Instalacja binarek i tworzenie instancji ISP](setup_instance.md)
1. [Aktualizacja](upgrade.md)
1. [Maintenance](maint.md)


## Szczegóły założeń

Serwer konfiguruję zwykle według pewnego schematu:

- __LVM__ - używam, mimo, że zwykle konfguruję według zasady 1 PV = 1 LV - ISP świetnie sobie radzi ze stripowaniem danych pomiędzy wiele katalogów, które są punktami montowania filesytemów. 
    Dlatego trzymam się zasady, że aplikacja wie lepiej. Dotyczy to w szczegółności:

    - _Dbspaces_ - katalogów bazy danych. 
    - _Dirspaces_ - katalogów _devclassy_ `FILE` zarówno pod pule plikowe jak i pod backup bazy.
    - _Stgpooldir_ - katalogów pul kontenerowych na dla _Dirpools_.

- __Kilka grup woluminów__ - to zależy od tego co dostanę, ale w świecie idealnym, dostaję __dwa__ różne sytemy dyskowe: Coś pod bazę i pule i coś pod backup bazy. Ale nawet na jednej macierzy zwykle robię coś takiego:

    ```bash title="PRzykładowy układ LV na małym ISP"
    [root@sp-1 ~]# lvs
      LV         VG        Attr       LSize    Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
      dir00lv    dirpoolvg -wi-ao---- <200.00g                                                    
      dir01lv    dirpoolvg -wi-ao---- <200.00g                                                    
      dir02lv    dirpoolvg -wi-ao---- <200.00g                                                    
      dir03lv    dirpoolvg -wi-ao---- <200.00g                                                    
      dir04lv    dirpoolvg -wi-ao---- <200.00g                                                    
      dir05lv    dirpoolvg -wi-ao---- <200.00g                                                    
      dir06lv    dirpoolvg -wi-ao---- <200.00g                                                    
      dir07lv    dirpoolvg -wi-ao---- <200.00g                                                    
      home       rhel      -wi-ao----  <18.04g                                                    
      root       rhel      -wi-ao----   36.95g                                                    
      swap       rhel      -wi-ao----    4.00g                                                    
      actlog_lv  spvg      -wi-ao----  <80.00g                                                    
      archlog_lv spvg      -wi-ao----  <80.00g                                                    
      db0_lv     spvg      -wi-ao----  <40.00g                                                    
      db1_lv     spvg      -wi-ao----  <40.00g                                                    
      db2_lv     spvg      -wi-ao----  <40.00g                                                    
      db3_lv     spvg      -wi-ao----  <40.00g                                                    
      dbb_lv     spvg      -wi-ao---- <100.00g
    ```

    - `spvg` - grupa pod bazę: `db?`, `actlog`, instancję, czasem `archlog`.
    - `dirpoolvg` - rzeczy związane z poulami kontenerowymi

- Zwykle zakładam strukturę katalogów mniej więcej zgodną z [Blueprintem](https://www.ibm.com/support/pages/ibm-storage-protect-blueprints).
