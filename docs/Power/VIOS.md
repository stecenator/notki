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

## Shared Ethernet Adapter

!!! Note "Ważne"
    Adres IP można dodać do SEA, ale bezpieczniej jest dodać go do karty obok, która jest w domyśnym VLANie. Dzięko temu możliwe będzei np serwisowanie SEA bez utraty dostpu sieciowego do VIOSa 

Kolejność tworznia:

1. LACP na adapterach fizycznych, np `ent0` i `ent1`. 

    ``` hl_lines="9" title="smitty etherchannel"
                        Add An EtherChannel / Link Aggregation

    Type or select values in entry fields.
    Press Enter AFTER making all desired changes.
      
    [MORE...2]                                              [Entry Fields]
      Alternate Address                                  []                      +
      Enable Gigabit Ethernet Jumbo Frames                no                     +
      Mode                                                8023ad                 +
      IEEE 802.3ad Interval                               long                   +
      Hash Mode                                           default                +
      Backup Adapter                                                             +
           Automatically Recover to Main Channel          yes                    +
           Perform Lossless Failover After Ping Failure   yes                    +
      Internet Address to Ping                           []
      Number of Retries                                  []                      +#
      Retry Timeout (sec)                                []                      +#
      MAC swap                                            no                     + 
      LLDP packet processing mode                         none                   + 
    [BOTTOM]

    ```

    Utworzona karta powinna wyglądać mniej więcej tak:

    ``` title="Atrybuty zagregowanej karty Etherchannel"
    # lsattr -El ent2
    adapter_names   ent0,ent1      EtherChannel Adapters                                          True
    alt_addr        0x000000000000 Alternate EtherChannel Address                                 True
    auto_recovery   yes            Enable automatic recovery after failover                       True
    auto_set_mtu    yes            Auto set jumbo mtu if jumbo frames is set                      True
    backup_adapter  NONE           Adapters to use when the primary channel fails                 True
    delay_log       0              Delay error logging (in seconds) during open                   True
    hash_mode       src_dst_port   Determines how outgoing adapter is chosen                      True
    hcn_id          0              Hybrid Converged Network ID                                    True
    interval        long           Determines interval value for IEEE 802.3ad mode                True
    lldp_mode       none           LLDP packet special processing                                 True
    mac_swap        no             Enable MAC address swap between primary and backup on failover True
    mode            8023ad         EtherChannel mode of operation                                 True
    netaddr         0              Address to ping                                                True
    noloss_failover yes            Enable lossless failover after ping failure                    True
    num_retries     3              Times to retry ping before failing                             True
    retry_time      1              Wait time (in seconds) between pings                           True
    use_alt_addr    no             Enable Alternate EtherChannel Address                          True
    use_jumbo_frame no             Enable Gigabit Ethernet Jumbo Frames                           True
    ```

1. Upewnij się, że masz jakieś karty wirtualne, które będą "trunking" czyli przeznaczone do rozwowy z SEA. Musisz mieć co najmniej po jednej dla każego VLANu trunkowanego do SEA. 

1. Utwórz adapter SEA na utworzonym LACPie (karta `ent2`) :

    === "Bez HA"
        ```sh title="Tworzenie karty SEA"
        $ mkvdev -sea ent2 -vadapter ent3  -default ent3 -defaultid 12 
        ent5 Available
        en5
        et5
        ```

    === "`ha_mode=auto`"
        ```sh title="Tworzenie karty SEA"
        $ mkvdev -sea ent2 -vadapter ent3  -default ent3 -defaultid 12 -attr ha_mode=auto ctl_chan=ent5
        ent5 Available
        en5
        et5
        ```        

    === "`ha_mode=sharing`"
        ```sh title="Tworzenie karty SEA w trybie sharing"
        $ mkvdev -sea ent2 -vadapter ent3,ent7,ent8  -default ent3 -defaultid 12 -attr ha_mode=sharing ctl_chan=ent5
        ent5 Available
        en5
        et5
        ```  

        !!! Important "Ważne"
            Jako `-vadapter` musi być podane co najmniej 2 adaptery!

### Dodanie nowych kart vETH do SEA

Czasem trzeba dodać nowy VLAN. Wtedy nowy tag musi być na _trunku_ do fizycznej karty, która jest pod SEA. A od strony Powera są dwa podejśćia:

=== "Dodanie taga do istniejącej vETH"
    Mając SEA wirtualizujące jedną kartę vETH, po prostu dodajesz nowego taga do niej. Będzie gadać ze wszystkim LPARami, które mają PVID=tag w obrębie vSwitcha.

=== "Dodanie nowej vETH"
    To pozwili na zmianę trybu `ha_mode` na `sharing`. Nowa karta musi mieć PVID pewnie z dupy, b i tak go nie przenosi, ale __musi__ być tagowana VLANem który ma przenosić.

!!! Warning "Ważne"
    Jeśli planujesz SEA w trybie `sharing`, nadaj wszystkim kartom na jednym viosie __trunk priority__ `1` a na drugin `2`. Same się dogadają, kto ma ktory obsługiwać. 

1. Sprawdź atrybuty dodawanych kart po obu stronach. Dla kążdej karty wykonaj:

    ``` sh title="WEryfikacja trunk i PVID"
    entstat -d entX | grep -i -E 'trunk|port vlan'
    ```

    I upewnij się, że `trunk_priority` jest ustawione ok, i zgadzają się `PVID`.

1. Wylistuj obecne adaptery wirtualne przypisane do karty SEA. Założenie: SEA to `ent6`

    ``` sh title="Lista adapterów i tryb ha w SEA"
    lsdev -dev ent6 -attr | grep -E "virt_adapters|ha_mode"
    ```

    ??? Example "Przykład"
        ```
        $ lsdev -dev ent6 -attr | grep -E "virt_adapters|ha_mode"
        ha_mode         auto     High Availability Mode                                                             True
        virt_adapters   ent3     List of virtual adapters associated with the SEA (comma separated)                 True
        ```

1. Dodaj brakujące adaptery. __na liście muszą być też te już wcześniej umieszczone__.

    ``` sh title="Dodanie kart vET do SEA"
    chdev -dev <sea_name> -attr virt_adapters=<adapter1>,<adapter2>,<adapter3>
    ```

    ??? Example "Przykład"
        ```sh
        $ chdev -dev ent6 -attr virt_adapters=ent3,ent7,ent8,ent9
        ent6 changed
        ```

1. Zweryfikuj czy wszystko jest ok:

    ``` sh title="Sprawdzenie"
    entstat -d ent6 | grep -i -E 'port vlan|trunk'
    ```

    ??? Example "Przykład"
        ```
        [root@bo-vios1:/]# entstat -d ent6 | grep -i -E 'port vlan|trunk'


        Trunk Adapter: True
        Port VLAN ID:    12
        Trunk Adapter: True
        Port VLAN ID:   230
        Trunk Adapter: True
        Port VLAN ID:   229
        Trunk Adapter: True
        Port VLAN ID:    13
        Trunk Adapter: False
        Port VLAN ID:    99
        ```

### Zmiana trybu ha_mode na `sharing`

Jest możliwa tylko, gdy  bridgowany jest wiecej niż jeden adapter wirtualny, co w sumie jest logiczne. 

!!! Bug "Do rozkminy"
    Żeby chodziły tagi 802.3, trzeba je wieszać na adapterze _default_ jako... tagi. A jeśli chcę miec wiecej kart, do _load sharing_ to jaki PVID im dawać? Z dupy, czy jakiś istniejący? 

### TCPIP w VIOS

1. Dodaj IP do wirtualnej karty Ethernet z tego samego VLANu co domyślny VLAN dla SEA, ale nie oznaczone jako _bridge_ w progilu partycji. W typ przypadku to będzie karta `en4` ze slotu `V11`:

    ```sh title="Konfigurowanie ip w VIOS"
    $ mktcpip -hostname di-vios1 -inetaddr 10.0.12.83 -netmask 255.255.255.0 -interface en4 -start -gateway 10.0.12.254
    ```

## NPIV

### Listing mapowań NPIV

```sh title="Mapowania w CSV"
ioscli lsmap -all -npiv -field name clntid clntname vfcclient fc vfcclientdrc -fmt ,
```

??? Example "Przykład" 
    ```sh
    # ioscli lsmap -all -npiv -field name clntid clntname vfcclient fc vfcclientdrc -fmt ,
    vfchost0,3,di-ora-prd,fcs0,fcs0,U9824.42A.78EBBA1-V3-C4
    vfchost1,3,di-ora-prd,fcs1,fcs1,U9824.42A.78EBBA1-V3-C5
    vfchost2,4, , ,fcs0, 
    vfchost3,4, , ,fcs1, 
    vfchost4,5, , ,fcs0, 
    vfchost5,5, , ,fcs1, 
    vfchost6,6, , ,fcs0, 
    vfchost7,6, , ,fcs1, 
    vfchost8,7, , ,fcs0, 
    vfchost9,7, , ,fcs1, 
    vfchost10,8, , ,fcs0, 
    vfchost11,8, , ,fcs1,
    ```
