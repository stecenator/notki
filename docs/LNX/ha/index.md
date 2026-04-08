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

    Sklonowany z jednego źródła według [:fontawesome-regular-hand-point-right: tego opisu](../virt/qemu-img.md#konwersja-zlinkowanego-klona-do-niezaleznej-kopii).

-   :material-ip-network:{ .lg .middle } [__Sieć__](#siec)

    ---

    Składa się z 3 adresów: 2 na węzły i 1 na VIP usługi.

    !!! Danger "Uwaga"
        Jedna sieć na dwuwęzłowym klastrze to za mało. Jej wyłączenie może utuchomić STONITH!.


-   :material-harddisk:{ .lg .middle } [__Dyski__](#dyski)

    ---

    OS na QCOW2, wpółny storage na RAW

-   :fontawesome-solid-hands-holding-circle:{ .lg .middle } [__Aplikacja__](#aplikacja)

    ---

    W klastrze będzie działać :IBM-bw: Storage Protect.

-   :material-source-commit-start:{ .lg .middle } [__Start__](#aplikacja)

    ---

    Zaczynam od [konfiguracji stand-alone ISP na jednym nodzie](../ISP/setup_instance.md). W ramach procedury przenoszę ISP przenoszę do klastra.

</div>

## Architektura klastra

``` mermaid
flowchart LR
    %% Węzły klastra
    subgraph sp-cluster [Pacemaker cluster]
        direction LR

        subgraph sp-n1 [sp-n1]
            spinst1[(spinst1)]
        end

        subgraph sp-n2 [sp-n2]
            oc[(oc)]
        end
    end

    %% Aktywne przypisanie (linią ciągłą)
    spinst1 --> sp-n1
    oc --> sp-n2

    %% Możliwość przełączenia (linie przerywane)
    spinst1 -. failover .- sp-n2
    oc -. failover .- sp-n1
```

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

| Dysk             | sp-n1                 | sp-n2                  | Opis |
| :---             | :---:                 | :---:                  | :--- |
| sp-n1-os.qcow2   | :material-check:      |                        | Dysk systemowy |
| sp-n2-os.qcow2   |                       | :material-check:       | Dysk systemowy |
| pcmk-actlog.raw  | :material-check-bold: | :material-check-bold:  | Active log |
| pcmk-archlog.raw | :material-check-bold: | :material-check-bold:  | Archive log |
| pcmk-db01.raw    | :material-check-bold: | :material-check-bold:  | DB01 |
| pcmk-db02.raw    | :material-check-bold: | :material-check-bold:  | DB02 |
| pcmk-dbb.raw     | :material-check-bold: | :material-check-bold:  | Backup bazy |
| pcmk-inst.raw    | :material-check-bold: | :material-check-bold:  | Instancja |

## Aplikacja

Wysokodostępną aplikacją jest IBM Storage Protect. Początkowo skonfigurowany na jednym węźle `sp-n1`. Instancja posadowiona na dyskach, które będa uwspólnione w ramach klastra.