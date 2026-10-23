---
icon: fontawesome/solid/gears
---

# Skrypty operacyjne

Czyli surogaty komend, które powinny być w TSM. sporo informacji tutaj zawartych jest powtórzeniem z rozdziału o [SQL](get_info.md) ale treść nie pokrywa się w 100%. Z założenia to jest wszystko, a w rozdziale o SQL tylko to co potrzebne do dokumentacji i przeglądu.

!!! Tip "Wskazówka"
    Nie musisz kopiwać skryptów pojedynczo. Wszystkie skrypty z tej strony można zdefiniować makrem, które jest [tutaj](macros.md#makro-definujace-skrypty-operacyjne).

---

## Urządzania fizyczne

Zapytania związane z:

 - Bibliotekami
 - Napędami
 - Taśmami w bibliotekach
 - Ścieżkami

### Ścieżki, napędy i urządzenia "by server"

Lista wszystkich napędów, także typu `FILE`

- serwer
- napęd
- serial
- device

=== "SQL"

    ```sql
    --8<-- "scripts/isp-sql/drives_by_server.sql"
    ```

=== "Skrypt `q_drive`"

    Do kopiowania:

    ```
    --8<-- "scripts/isp-sql/q_drive.dsm"
    ```

### Statystyki taśm w bibliotekach

Liczenie taśm o różnych statusach, pogrupowane na biblioteki

=== "SQL"

    ```sql
    --8<-- "scripts/isp-sql/tape_stats.sql"
    ```


=== "Skrypt `tape_stats`"

    ```
    --8<-- "scripts/isp-sql/tape_stats.dsm"
    ```

### Taśmy nie ruszane od X dni

Daty zapisu taśm, które nie były czytane od X dni.

!!! Warning "Zwróć uwagę"

    W SQLu horyzont czasowy jest zahardkodowany na 90 dni. W sktypcie to jest parametr.

=== "SQL"

    ```sql
    --8<-- "scripts/isp-sql/old_tapes.sql"
    ```


=== "Skrypt `old_tapes`"

    ```
    --8<-- "scripts/isp-sql/old_tapes.dsm"
    ```

### Scieżki OFFLINE

=== "SQL"

    ```sql
    --8<-- "scripts/isp-sql/q_path.sql"
    ```

=== "Skrypt `q_path`"

    ```
    --8<-- "scripts/isp-sql/q_path.dsm"
    ```

### Kandydaci do reclaim

=== "SQL"

    ```sql
    --8<-- "scripts/isp-sql/q_recl.sql"
    ```

=== "Skrypt `q_recl`"

    ```sql
    --8<-- "scripts/isp-sql/q_recl.dsm"
    ```

---

## Klasy urządzeń

Alternatywna wesrja `q devc`, pokazująca pojemności, moutlimity. Ponadto katalogi dla klas typu `FILE` i formaty dla taśm.

=== "SQL"

    ```sql
    --8<-- "scripts/isp-sql/q_devc.sql"
    ```

=== "Skrypt `q_devc`"

    ```
    --8<- "scripts/isp-sql/q_devc.dsm"
    ```

---

## Pule i woluminy

### Statystyki woluminów w pulach

Statystyki woluminów w pulach z rozbiciem na reclaimowalne i nie. Zlicza wolimuny w stanach `Filing`, `Full<50` (jako `Recl`), `Full` i `Pending`

=== "SQL"

    ```sql
    --8<-- "scripts/isp-sql/vol_stats.sql"
    ```

=== "Skrypt `vol_stats`"

    ```
    --8<-- "scripts/isp-sql/vol_stats.dsm"
    ```

### Statystyki pul

=== "SQL"

    ```sql
    --8<-- "scripts/isp-sql/stg_stats.sql"
    ```

=== "Skrypt `stg_stats`"

    ```
    --8<-- "scripts/isp-sql/stg_stats.dsm"
    ```

---

## Filespace i pliki

Zapytania związane z filespaces i backupami.

### Filespacee backupowane wcześniej niż 30 dni temu

=== "Ładny"

    ```sql
    --8<-- "scripts/isp-sql/old_fs.sql"
    ```

=== "Skrypt `old_fs`"

    ```
    --8<-- "scripts/isp-sql/old_fs.dsm"
    ```

---

## Klienci i workload

Informacje o klientach, trupach w szafie :zombie: i transferach danych.

### Ogólne statystyki klientów

Takie trochę lepsze `q node`.

=== "SQL"

    ```sql
    --8<-- "scripts/isp-sql/node_stats.sql"
    ```

=== "Skrypt `node_stats`"

    ```
    --8<-- "scripts/isp-sql/node_stats.dsm"
    ```

### Klienci nieaktywni od 30+ dni

!!! Tip "Wskazówka"

    Zamiast 30 dni można wstawić dowolną sensowną biznesowo wartość. 30 w moim wypadku to była njawiększy w środowisku okres dla harmonogramu, więc jesli cezgoś nie widziałem od 30 dni, to źle.


=== "SQL"

    ```sql
    --8<-- "scripts/isp-sql/inactive_nodes.sql"
    ```

=== "Skrypt `ina_nodes`"

    ```
    --8<-- "scripts/isp-sql/inactive_nodes.dsm"
    ```

### Zajętość mijesca klientów nieaktywnych przez 30 dni

!!! Warning "Uwaga"

    Według _developmentu_ IBM, tabele `OCCUPANCY` i `AUDITOCCUPANCY` mogą nie dawać poprawnych danych gdy używane są pule kontenerowe. 

=== "SQL"

    ```sql
    --8<-- "scripts/isp-sql/inactive_nodes_occ.sql"
    ```

=== "Skrypt `ina_nodes_occ`"

    ```
    --8<-- "scripts/isp-sql/inactive_nodes.dsm"
    ```


### Klienci aktywni ciągu ostatnich 30 dni

=== "SQL"

    ```sql
    --8<-- "scripts/isp-sql/active_nodes.sql"
    ```

=== "Skrypt `actv_nodes`"

    ```
    --8<-- "scripts/isp-sql/active_nodes.dsm"
    ```

### Dzienny transfer danych

=== "Ładny"

    ```sql
    --8<-- "scripts/isp-sql/today_mib.sql"
    ```

=== "Skrypt `today_mib`"

    ```
    --8<-- "scripts/isp-sql/today_mib.dsm"
    ```

### Dzienny transfer danych z ostatnich 30 dni

=== "SQL"

    ```sql
    --8<-- "scripts/isp-sql/30-days_mib.sql"
    ```

=== "Skrypt `30d_mib`"

    ```
    --8<-- "scripts/isp-sql/30-days_mib.dsm"
    ```

### Auditoccupancy w domenach

=== "SQL"

    ```sql
    --8<-- "scripts/isp-sql/dom_audito.sql"
    ```

=== "Skrypt `dom_audito`"

    ```
    --8<-- "scripts/isp-sql/dom_audito.dsm"
    ```

--- 

## Polityki

### Polityki backupu wraz z destination

!!! Warning "Uwaga"
	Niektóre kolumny są castowane na krótsze `char'y`, żeby ładnie wyglądały, więc coś może być ucięte!


=== "SQL"

    ```sql
    --8<-- "scripts/isp-sql/q_bkp_pol.sql"
    ```

=== "Skrypt `q_bkp_pol`"

    ```sql
    --8<-- "scripts/isp-sql/q_bkp_pol.dsm"
    ```

### Polityki archiwizacji wraz z destination

!!! Warning "Uwaga"
	Niektóre kolumny są castowane na krótsze `char'y`, żeby ładnie wyglądały, więc coś może być ucięte!


=== "SQL"

    ```sql
    --8<-- "scripts/isp-sql/q_arch_pol.sql"
    ```

=== "Skrypt `q_arch_pol`"

    ```sql
    --8<-- "scripts/isp-sql/q_arch_pol.dsm"
    ```

## Jak to odpalić?

Przed zbieraniem danych trzeba puścić [makro](#makro-definujace-skrypty-operacyjne) definujące te skrypty. Zakładam, że zostało skopiowane do pliku `def-scripts.mac`

```shell
dsmadmc -id=mój_admin -pa=tajne_hasło -itemcommit macro def-scripts.mac
```

## `isp_info.mac` - raport o stanie instancji TSM/Protect

Korzysta ze skryptów definiowanych wyżej, puszczać tak:

```shell
dsmadmc -id=mój_admin -pa=tajne_hasło -itemcommit -outfile=raport.txt macro isp_info.mac
```

**Uwaga:** parametr `-outfile=raport.txt` jest lepszy niż przekierowanie wyjścia `> raport.txt` bo komendy typu `q status` są sformatowane jak na konsoli, a nie w linijkowo.

## Makro definujące skrypty operacyjne

Definicja wszystkich przydatnych skryptów w jednym makrze. Skopiuj tę treść do pliku `.mac` i uruchom w administracyjnym wierszu poleceń.

```
/* Script: q_devc                                    */
--8<-- "scripts/isp-sql/q_devc.dsm"
/* ------------------------------------------------- */
/* Script: q_drive                                   */
--8<-- "scripts/isp-sql/q_drive.dsm"
/* ------------------------------------------------- */
/* Script: q_recl                                    */
--8<-- "scripts/isp-sql/q_recl.dsm"
* -------------------------------------------------- */
/* Script: q_path                                    */
--8<-- "scripts/isp-sql/q_path.dsm"
/* ------------------------------------------------- */
/* Script: tape_stats                                */
--8<-- "scripts/isp-sql/tape_stats.dsm"
/* ------------------------------------------------- */
/* Script: old_tapes                                 */
--8<-- "scripts/isp-sql/old_tapes.dsm"
/* ------------------------------------------------- */
/* Script: vol_stats                                 */
--8<-- "scripts/isp-sql/vol_stats.dsm"
/* ------------------------------------------------- */
/* Script: stg_stats                                 */
--8<-- "scripts/isp-sql/stg_stats.dsm"
/* ------------------------------------------------- */
/* Script: old_fs */
--8<-- "scripts/isp-sql/old_fs.dsm"
/* ------------------------------------------------- */
/* Script: node_stats */
--8<-- "scripts/isp-sql/node_stats.dsm"
/* ------------------------------------------------- */
/* Script: ina_nodes */
--8<-- "scripts/isp-sql/inactive_nodes.dsm"
/* ------------------------------------------------- */
/* Script: actv_nodes */
--8<-- "scripts/isp-sql/active_nodes.dsm"
/* ------------------------------------------------- */
/* Script: ina_nodes_occ */
--8<-- "scripts/isp-sql/inactive_nodes_occ.dsm"
/* ------------------------------------------------- */
/* Script: today_mib */
--8<-- "scripts/isp-sql/today_mib.dsm"
/* ------------------------------------------------- */
/* Script: 30-days_mib */
--8<-- "scripts/isp-sql/30-days_mib.dsm"
/* ------------------------------------------------- */
/* Script: dom_audito */
--8<-- "scripts/isp-sql/dom_audito.dsm"
/* ------------------------------------------------- */
/* Script: q_bkp_pol */
--8<-- "scripts/isp-sql/q_bkp_pol.dsm"
/* ------------------------------------------------- */
/* Script: q_arch_pol */
--8<-- "scripts/isp-sql/q_arch_pol.dsm"
/* ------------------------------------------------- */
```