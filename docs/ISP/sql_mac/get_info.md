---
icon: material/table-search
---

# SQL

Zbiór użytecznych zapytań SQL, definicji skryptów serwera i makr, których używam do zbierania danych do dokumentacji wdrożeniowej i podczas pracy z TSM/ISP. SQLe pomagąjące w codziennnym życiu, oraz odpowiednie definicje skryptów, znajduję się w [tym](macros.md) rozdziale.

!!! Tip "Wskazówka"
    Nie musisz kopiwać skryptów pojedynczo. Wszystkie skrypty z tej strony można zdefiniować makrem, które jest [tutaj](macros.md#makro-definujace-skrypty-operacyjne).

    Wszystkie SQLe z tego rozdziału, zostały też zwarte w jednym [makrze](#raport-ogolny) na końcu tej sekcji.

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

=== "Jednolinijkowiec"

    Do kopiowania:

    ```sql
    --8<-- "scripts/isp-sql/drives_by_server-sl.sql"
    ```

=== "Bez FILE"

    Alternatywnie, z pominięciem napędów typu `FILE`:

    ```sql
    --8<-- "scripts/isp-sql/drives_by_server_no_file.sql"
    ```

=== "Bez FILE, jednolinijkowiec"

    Alternatywnie, z pominięciem napędów typu `FILE`:

    ```sql
    --8<-- "scripts/isp-sql/drives_by_server_no_file-sl.sql"
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

---

## Klasy urządzeń

Alternatywna wesrja `q devc`, pokazująca pojemności, moutlimity. Ponadto katalogi dla klas typu `FILE` i formaty dla taśm.

=== "SQL"

    ```sql
    --8<-- "scripts/isp-sql/q_devc.sql"
    ```

=== "Jednolinijkowiec"

    Do kopiowania:

    ```sql
    --8<-- "scripts/isp-sql/q_devc-sl.sql"
    ```

=== "Skrypt `q_devc`"

    ```
    --8<-- "scripts/isp-sql/q_devc.dsm"
    ```

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

=== "SQL"

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
    --8<-- "scripts/isp-sql/inactive_nodes_occ.dsm"
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

=== "SQL"

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

=== "Skrypt `30d_mibs`"

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

## Harmonogramy
## Raport ogólny

Czasem, zwłaszcza do celów dokumentacyjnych, potrzebuję wykonać to wszystko razem. Tu są wszystkie zapytania z tego rozdziału, zebrane jako jedno makro:

``` title="Jedno makro by wszystkimi rządzić i ciemności złączyć"
/* ------------------------------------------------- */
/* Drives, OS devices, serials */
--8<-- "scripts/isp-sql/drives_by_server.sql"
/* ------------------------------------------------- */
/* Libvolumes statiscics */
--8<-- "scripts/isp-sql/tape_stats.sql"
/* ------------------------------------------------- */
/* Write dates of tapes not read since last 90 days */
--8<-- "scripts/isp-sql/old_tapes.sql"
/* ------------------------------------------------- */
/* Devclassess */
--8<-- "scripts/isp-sql/q_devc.sql"
/* ------------------------------------------------- */
/* Stgpool volume statiscics */
--8<-- "scripts/isp-sql/vol_stats.sql"
/* ------------------------------------------------- */
/* Stgpool pool statiscics */
--8<-- "scripts/isp-sql/stg_stats.sql"
/* ------------------------------------------------- */
/* Filespaces older than 30 days */
--8<-- "scripts/isp-sql/old_fs.sql"
/* ------------------------------------------------- */
/* Node statistics. Oldest first */
--8<-- "scripts/isp-sql/node_stats.sql"
/* ------------------------------------------------- */
/* Nodes inactive for more than 30 days */
--8<-- "scripts/isp-sql/inactive_nodes.sql"
/* ------------------------------------------------- */
/* Inactive for more than 30 days nodes occupancy    */
--8<-- "scripts/isp-sql/inactive_nodes_occ.sql"
/* ------------------------------------------------- */
/* Nodes active within last 30 days */
--8<-- "scripts/isp-sql/active_nodes.sql"
/* ------------------------------------------------- */
/* Todays MiBs */
--8<-- "scripts/isp-sql/today_mib.sql"
/* ------------------------------------------------- */
/* 30 days MiBs */
--8<-- "scripts/isp-sql/30-days_mib.sql"
/* ------------------------------------------------- */
/* Domain auditoccupancy */
--8<-- "scripts/isp-sql/dom_audito.sql"
/* ------------------------------------------------- */
/* Backup copy groups with destination */
--8<-- "scripts/isp-sql/q_bkp_pol.sql"
/* ------------------------------------------------- */
/* Archive copy groups with destination */
--8<-- "scripts/isp-sql/q_arch_pol.sql"
```