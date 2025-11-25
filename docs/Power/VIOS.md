# VIOS

!!! Tip "Wskazówka"
    Choć support IBM tego nie lubi, do VIOSów zwykle loguję się na `root`. Warto w takim wypadku warto dodać `/usr/ios/cli/` do `$PATH`. Albo użyć mojego ulubionego pliku `.kshrc` :smile:.

``` sh title="Mój ulubiony profil `.kshrc` dla VIOSów"
--8<-- "Power/template/kshrc_template.sh"
```


## Mapowania w formacie CSV

Do celów skryptowania, standardowy output z `lsmap` jest upierdliwy. Czasem lepiej jest mieć to od razu w formacie *CSV*. 

``` sh title="vFC w formacie CSV"
# ioscli lsmap -all -npiv -field name clntid clntname vfcclient fc vfcclientdrc -fmt ,
```

``` sh title="vSCSI/vOPT w formacie CSV"
# ioscli lsmap -all -field svsa physloc vtd clientid backing -fmt ,
```

## Aktualizowanie VIOSów

Trzeba robić delikatnie. Najlepiej jest zacząć od klonowania na zapasowy dysk, jak by coś się miało spierdolić.

!!! Danger "Uwaga"
    Jeśli pracujesz zdalnie, warto mieć tam jump-hosta z `tmux` lub `screen`, bo VPNy mają tendencję do zrywania połączeń podczas kluczowych momentów :smile:.

Założenia:

- VIOSy mają zapasowe dyski do klonowania. Być możę istnieją wcześniejsze kopie VIOSa na tych dyskach, więc trzeba będzie je usunąć.
- Poprawki są wgrane do katalogu `/home/padmin/vios_4.1.1.10`

### Klonowanie na zapas

Na początek krótka weryfikacja:

```sh title="Komendy weryfikacyjne"
bootinfo -s                     # (1)
lspv                            # (2)
alt_disk_install -X old_rootvg  # (3)
```

1.  Podaje dysk, z którego system wstał.
2.  Pokazuje listę dyskóœ w OSie. W tym np z `old_root_vg`, którą trzeba **odpowiednio** usunąć: 
    ```sh
    hdisk0          00c7a2e8122f3857                    old_rootvg                    
    hdisk1          00c7a2e852fc9e03                    None                        
    hdisk2          00c7a2e8bab60f8b                    rootvg          active 
    ```
3.  **Odpowiednio** usuwa grupę `old_root_vg`.

Po usunięciu `old_root_vg` sytuacja powinna wygądać tak:

```sh
root@e1080m1viost2:/# lspv 
hdisk0          00c7a2e8122f3857                    None                        
hdisk1          00c7a2e852fc9e03                    None                        
hdisk2          00c7a2e8bab60f8b                    rootvg          active 
```

### Wgrwanie poprawek na VIOS

!!! Note "Uwaga"
    Tę cześć robić jako `padmin`.

```sh
e1080m1viost2> ls
cfgbackups      config          ioscli.log      rules           vios_4.1.1.10   viosupg_backup
e1080m1viost2> updateios -dev /home/padmin/vios_4.1.1.10 -install -accept
```

### Ustawianie **przed rebootem**

Jak system pokaże żę skończył wgrywać poprawki:

``` title="Koniec poprawek"
installp:  * * *  A T T E N T I O N ! ! ! 
        Software changes processed during this session require this system 
        and any of its diskless/dataless clients to be rebooted in order 
        for the changes to be made effective.
```

Wgraj najnowsze ustawienia a potem ostrzegawczy strzał w tył głowy.

```sh title="Deply ustawień i restart"
e1080m1viost2> rules -o deploy -d

bosboot: Boot image is 69660 512 byte blocks.
A manual post-operation is required for the changes to take effect, please reboot the system.
e1080m1viost2> shutdown -restart 
Shutting down the VIO Server could affect Client Partitions. Continue [y|n]?

y
```

!!! Danger "Uwaga:"
    Raczej poczekaj z aktulizacją następnego VIOSa, aż ten wstanie i go sprawdzisz :smile:. 