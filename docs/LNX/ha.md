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

-   :material-ip-network:{ .lg .middle } [__Sieć__](#sieć)

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

Klaster składa się z dwóch węzłów, skonfigurowanych sieciowo według  [tego](#sieć) opisu. Każda maszyna jest przygotowana do pracy z ISP według [tego](../ISP/setup_os.md) przepisu. 

## Sieć

| IP         | FQDN               | Opis                |
| :---       | :---               | :---                |
| 10.13.0.12 | sp01-n1.host-only  | IP 1 węzła klastra  |
| 10.13.0.13 | sp01-n2.host-only  | IP 2 węzła klastra  |
| 10.13.0.14 | sp01.host-only     | VIP usługi          |

## Dyski

Każdy OS ma swój systemowy w formacie QCOW2. Libvirt nie pozwala na współdzielenie takich dysów przez dwie maszyny, więc wspólne dyski są w formacie RAW, i jest ich tyle, żeby było poprawnie dla usługi.

## Aplikacja

Wysokodostępną aplikacją jest IBM Storage Protect. 