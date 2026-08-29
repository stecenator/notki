---
icon: octicons/container-24
---

# Pule kontenerowe

Jak z nimi żyć? 

Pojawiły się wraz z 7.1.3, czyli są już na rynku od 2017 roku, a nadal dostarczają sporo radośći. Ty jest zbiór moich doświaczeń z pulami kontenerowymi. 

## Zasady użycia

- [x] Pule konetenerowe nie nadają się do składowania danych zaszyfrowanych przezd zapisem (np szyfrowanych RMANem)
- [x] Dane wcześniej skompresowane też nie bardzo nadają się do składowania w kontenerach, choć dają się _deduplikować_. 
- [x] Migracja pomiędzy pulami zwykłymi i kontenerowymi jest [nietrywialna](../adm/dcp.md#migracja-i-kopiowanie-pomiedzy-pulami).
- [x] Disaster recovery lepiej oprzeć na replikacji
- [x] [Utrzymanie](../adm/dcp.md#utrzymanie) puli kontnerowej oznacza replkację, backup i regularne [audyty](../adm/dcp.md#audyt).

Najważniejszą zasadą, opisywaną także w Blueprintach, jest zasada 1:1. czyli jeden dysk = 1 LV = 1 filesystem= 1 katalog. Striping jest ro biony na przez Protecta.

```mermaid
flowchart TD
    POOL(Pula kontenerowa\nDP01)
    FS1(/sp/dc01/dir1)
    FS2(/sp/dc02/dir1)
    FS3(/sp/dc03/dir1)
    FS4(/sp/dc04/dir1)

    POOL <--- FS1
    POOL <--- FS2
    POOL <--- FS3
    POOL <--- FS4

    LV1(LV: dp01vg/dir01lv)
    LV2(LV: dp01vg/dir02lv)
    LV3(LV: dp01vg/dir03lv)
    LV4(LV: dp01vg/dir04lv)

    FS1 <--- LV1
    FS2 <--- LV2
    FS3 <--- LV3
    FS4 <--- LV4

    PV1(PV: sp1-dir1)
    PV2(PV: sp1-dir2)
    PV3(PV: sp1-dir3)
    PV4(PV: sp1-dir4)

    LV1 <--- PV1
    LV2 <--- PV2
    LV3 <--- PV3
    LV4 <--- PV4

    VG(VG: dp01vg)

    PV1 <--- VG
    PV2 <--- VG
    PV3 <--- VG
    PV4 <--- VG
```

## Tworzenie puli kontenerowej


1. Załóż filesystemy według powyższego schematu.

    === ":simple-linux: Linux"

        Założenia:

        - Moje dyski/urządzenia mpath nazywają się `cinek-sp1-dir*`. 
        - grupa będzie nazywać się `dirpoolvg`.
        - Całość będzie zmontowana do `/sp/dp01/dir*`.


        Procedura:


        1. Wyciagnij listę dysków. Zrobiłeś je według [tego](../../LNX/san/MPIO_and_SAN.md) przepisu?

            ```bash
            sudo multipath -ll | grep cinek-sp1-dir | cut -f 1 -d " "
            ```

            Na przykład tak:

            ```bash title="Przykład"
            sudo multipath -ll | grep cinek-sp1-dir | cut -f 1 -d " "
            cinek-sp1-dir1
            cinek-sp1-dir2
            cinek-sp1-dir3
            cinek-sp1-dir4
            ```
        
        1. Założ na nich PV.
        1. Dodaj do grupy `dirpoolvg`
        1. Na każdym z PV załóź LV tak, żeby zeżarł dokładnie jednen cały dysk:

            ```bash
            lvcreate -n dir01lv -l 100%free dirpoolvg /dev/mapper/cinek-sp1-dir1
            ```
        
            Powtórz ten krok dla wszyskich PV.

        1. Załóź filesystem na utworzonych woluminach logicznych. Np. XFS.
        1. Dodaj montowanie do `/etc/fstab`:

            ```bash
            cat >> /etc/fstab << EOF
            /dev/mapper/dirpoolvg-dir01lv				/sp/dp01/dir1	xfs	defaults	0 0
            /dev/mapper/dirpoolvg-dir02lv				/sp/dp01/dir2	xfs	defaults	0 0
            /dev/mapper/dirpoolvg-dir03lv				/sp/dp01/dir3	xfs	defaults	0 0
            /dev/mapper/dirpoolvg-dir04lv				/sp/dp01/dir4	xfs	defaults	0 0
            EOF
            ```

            !!! Warning "Uwaga na klaster"

                Oczywiście jeśli TSM będzie w klastrze, to do opcji trzeba dodać `noauto` :shrug:.

        1. Walnij `systemd` w łeb i zmontuj filesytemy:

            ```bash
            sudo systemctl daemon-reload
            sudo mount -a 
            ```


    === ":AIX-old: AIX"

        !!! Bug

            Wygrzebać notatki z ostatnigo wdrożenia.

    === ":material-microsoft-windows-classic: WinDOS"

        :simple-redragon: Tu żyją smoki. Nie idź tą drogą.


1. Załóż putą pulę: 
    
    ``` title="Definiowanie puli kontenerowej"
    define stgpool dp01 stgtype=directory 
    ```

1. Dodaj filesystemy do puli

    ```
    define stgpooldir dp01 /sp/dp01/dir1
    define stgpooldir dp01 /sp/dp01/dir2
    define stgpooldir dp01 /sp/dp01/dir3
    define stgpooldir dp01 /sp/dp01/dir4
    ```