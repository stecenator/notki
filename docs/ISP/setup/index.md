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

-   :simple-redhat:{ .lg .middle } [__OS: Red Hat 9__](#os)

    ---

    W tych przykładach, sklonowany według [tego artykułu](../virt/qemu-img.md#konwersja-zlinkowanego-klona-do-niezaleznej-kopii). Oczywiście w dużych instalacjach, na LPARze lub gołym żelazie. 

-   :material-ip-network:{ .lg .middle } [__Sieć__](#siec)

    ---

    Na statycznych adresach. Warto zainstersować się [bondingiem](../../LNX/bond.md).


-   :material-harddisk:{ .lg .middle } [__Dyski__](#dyski)

    ---

    Zasada: 1 LUN, 1 filesystem. Nawet w LVM. Protect sam sobie dobrze stripuje.

-   :fontawesome-solid-hands-holding-circle:{ .lg .middle } [__Aplikacja__](#aplikacja)

    ---

    :IBM-bw: Storage Protect na oddzielnej grupie woluminów, na dedykowanym użyszkodniku. 

</div>

## Spis treści

1. [Przygotowanie OS pod instalację](setup_os.md)
1. [Kartalogi i filesystemy](setup_os.md#filesystemy)
1. [Instalacja binarek i tworzenie instancji ISP](setup_instance.md)
1. [Aktualizacja](upgrade.md)
1. [Maintenance](setup/maint.md)