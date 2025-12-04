# Przydatne Powershelle
Pewnie każdy windziarz to zna, ale dla mnie to jak odkrycie koła.

## Wyświetlanie **`pipe`** w systemie

Przy uruchamianiu *Journal Engine* klienta Backup-Archive, czasem trzeba sprawdzić jakie `NamedPipe` zostały utworzone:

```PowerShell
Get-ChildItem \\.\pipe\
```

## WWPNy kart FC

Przegrałem flaszkę, bo twierdziłem, że się nie da:

```PowerShell
Get-WmiObject -class MSFC_FCAdapterHBAAttributes -namespace "root\WMI" | ForEach-Object {(($_.NodeWWN) | ForEach-Object {"{0:x}" -f $_}) -join ":"}
```

## `fstrim` dysku

O łindołs wiadomo dwie rzeczy: Po pierwsze, jak sama nazwa skazuje jego miejsce jest w okienku. Najlepiej na jakimś Linuxowym hoscie pod KVM. Po drugie weżmie ile mu dasz. Ale czasem jednak coś skasuje i wtedy warto odzyskać na hoście skasowane miejsce. Oczywiście, żeby to działało, trzeba w konfiguracji VMki ustawić *discardy* i przekonać gościa, żeby to robił. 

Za umożliwienie discardów po stronie hosta KVM jest odpowiedzialny ten kawałek XMLa:

```xml hl_lines="2" title="Włączanie unmap"
<disk type='file' device='disk'>
  <driver name='qemu' type='qcow2' discard='unmap'/>
  <source file='/var/lib/libvirt/images/c4eb-windos.qcow2'/>
  <target dev='vda' bus='virtio'/>
  <address type='pci' domain='0x0000' bus='0x04' slot='0x00' function='0x0'/>
</disk>
```

```PowerShell title="Trymowanie dysku w WinDOS 11"
Optimize-Volume -DriveLetter C -ReTrim -Verbose
```

??? Example "Przykład:"

    ```PowerShell
    PS C:\Users\MarcinStec> Optimize-Volume -DriveLetter C -ReTrim -Verbose
    VERBOSE: Invoking retrim on Windows (C:)...
    VERBOSE: Retrim:  0% complete...
    VERBOSE: Retrim:  100% complete.
    VERBOSE: Performing pass 1:
    VERBOSE: Retrim:  1% complete...
    VERBOSE: Retrim:  2% complete...
    VERBOSE: Retrim:  3% complete...
    VERBOSE: Retrim:  4% complete...
    VERBOSE: Retrim:  5% complete...
    [ ... dużo procentów ...]
    Post Defragmentation Report:
    VERBOSE:
     Volume Information:
    VERBOSE:   Volume size                 = 78.54 GB
    VERBOSE:   Cluster size                = 4 KB
    VERBOSE:   Used space                  = 41.06 GB
    VERBOSE:   Free space                  = 37.48 GB
    VERBOSE:
     Allocation Units:
    VERBOSE:   Slab count                  = 20590511
    VERBOSE:   Slab size                   = 4 KB
    VERBOSE:   Slab alignment              = 0 bytes
    VERBOSE:   In-use slabs                = 9210978
    VERBOSE:
     Retrim:
    VERBOSE:   Backed allocations          = 20590511
    VERBOSE:   Allocations trimmed         = 11379426
    VERBOSE:   Total space trimmed         = 43.40 GB
    ```

Od strony hosta widać to tak:

=== "Przed odchudzaniem"

    ```shell
    $ du -sm /var/lib/libvirt/images/c4eb-windos.qcow2
    38291   /var/lib/libvirt/images/c4eb-windos.qcow2
    ```

=== "Po odchudzeniu"

    ```shell
    $ du -sm /var/lib/libvirt/images/c4eb-windos.qcow2
    36645   /var/lib/libvirt/images/c4eb-windos.qcow2
    ```

Czyli urwał 2GiB. Niby szału nie ma, ale ta maszynka jest świeża i złapała tylko jeden cykl poprawek. Przy dłużej żyjących, albo np takich , gdzie coś odinstalowałem badź skasowałem, uzyski są większe. 