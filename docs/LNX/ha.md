---
icon: cluster
---

# Pacemaker

Pacemaker jest standardowym oporgramowaniem HA na Linuxa. Tutaj opisuję procedurę stawiania dwuwęzłowego klastra według nastęujących założeń:

<div class="grid cards" markdown>

-   :simple-qemu:{ .lg .middle } [__QEMU/KVM/Libvirt__](../virt/libvirt.md)

    ---

    Klaster stawiam na wirtualizwtorze Libvirt z KVM/QEMU.

-   :simple-redhat:{ .lg .middle } [__OS: Red Hat 9__](#os)

    ---

    Sklonowany z jednego źródła według [:fontawesome-regular-hand-point-right: tego artykułu](../virt/qemu-img.md#konwersja-zlinkowanego-klona-do-niezaleznej-kopii).

-   :material-ip-network:{ .lg .middle } [__Sieć__](#siec)

    ---

    Składa się z 3 adresów: 2 na węzły i 1 na VIP usługi.


-   :material-harddisk:{ .lg .middle } [__Dyski__](#dyski)

    ---

    OS na QCOW2, wpółny storage na RAW

-   :fontawesome-solid-hands-holding-circle:{ .lg .middle } [__Aplikacja__](#aplikacja)

    ---

    W klastrze będzie działać :IBM-bw: Storage Protect.

</div>

## OS

Klaster składa się z dwóch węzłów, które są zlinkowanymi klonami maszyny "Golden image". Cały proces tworzenia klonów opisałem [tu](../virt/libvirt.md#klonowanie-maszyny). 
Każdy z klonów dostał [swoją](#siec) konfigurację sieci i został też dostosowany do wymogów [aplikacji](../ISP/setup_os.md). 


## Sieć

| IP         | FQDN             | Opis                |
| :---       | :---             | :---                |
| 10.13.0.12 | sp-n1.host-only  | IP 1 węzła klastra  |
| 10.13.0.13 | sp-n2.host-only  | IP 2 węzła klastra  |
| 10.13.0.14 | sp.host-only     | VIP usługi          |

## Dyski

Każdy OS ma swój systemowy w formacie QCOW2. Libvirt nie pozwala na współdzielenie takich dysów przez dwie maszyny, więc wspólne dyski są w formacie RAW, i jest ich tyle, żeby było poprawnie dla usługi. ponieżej znajduej się zestawianie dysków utworzonych dysków wirtualnych. W "dorosłych" instalacjch, to oczywiście bedą LUNy z macierzy. 

| Dysk             | sp-n1            | sp-n2             | Opis |
| :---             | :---:            | :---:             | :--- |
| sp-n1-os.qcow2   | :material-check: |                   | Dysk systemowy |
| sp-n2-os.qcow2   |                  | :material-check:  | Dysk systemowy |
| pcmk-actlog.raw  | :material-check: | :material-check:  | Active log |
| pcmk-archlog.raw | :material-check: | :material-check:  | Archive log |
| pcmk-db01.raw    | :material-check: | :material-check:  | DB01 |
| pcmk-db02.raw    | :material-check: | :material-check:  | DB02 |
| pcmk-dbb.raw     | :material-check: | :material-check:  | Backup bazy |
| pcmk-inst.raw    | :material-check: | :material-check:  | Instancja |

## Aplikacja

Wysokodostępną aplikacją jest IBM Storage Protect. 