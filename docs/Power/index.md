---
icon: IBM-Power
---

# IBM Power/PowerVM/VIOS/AIX

## HMC


## VIOS

## AIX

### Ulinoxowienie AIXa

Mój ulubiony szablon pliku `.kshrc`. Na VIOSie z resztą też :shrug:.

```sh title=".kshrc"
--8<-- "Power/template/kshrc_template.sh"
```

#### DNF

Dnf na AIXie można instalować na dwa sposoby. Lokalnie z krążka scięgnießego z ESS albo skryptem ze strony IBM. 

##### Instalcja z DVD

1. Zamontuj krążek np z VIOSa. W poniższym przykładzie, to jest `cd1`:

    ```sh title="Montowanie DVD na AIX"
    mount -V cdrfs -o ro /dev/cd1 /mnt
    ```

1. Upewnij się, że `/tmp` i `/opt` jest przynajmniej po 1G wolnego miejsca. W razie potrzeby dodaj. (tutaj dodaję po 2G):

    ```sh title="Rozszerzanie fileystemu pod AIXem"
    chfs -a size=+2G /opt
    chfs -a size=+2G /tmp
    ```

1. Przejdź do `/mnt/ezinstall/ppc` i puść sktypt `dnf_aixtoolbox_local.sh`

    ```sh title="Instlacja DNF z lokalnego nośnika"
    ./dnf_aixtoolbox_local.sh /mnt
    ```

    !!! Note "Ważne"
        Jako prametr nalezy podać punk montowania DVD z Toolboxem.
