## Kreowanie bazy

### Założenia

- User instancji to `db2inst1`.
- Baza będzie się nazywać `pilsisko`
- `DBPATH` tej bazy to `/pils/pilsisko`
- Tablespace bazy będzie w `/pils/dir01` i `/pils/dir01`

### Przestrzeń pod tablespace bazy

Przygotuj katalogi, albo jeszcze lepiej oddzielne filesystemy w zamontuj je w:

```sh
# mkdir -p /pils/{dir01,dir02,pilsisko}
# echo tu montujesz filesystemy, dodajesz fstaba itd
# chown -R db2inst1:db2inst1 /pils
```

### Tworzenie bazy

Komenda do tworzenia bazy:

```sql
CREATE DATABASE PILSISKO ON '/pils/dir01','/pils/dir01' DBPATH ON '/pils/pilsisko'
```

Przykładowe wywołanie (oczywiście jako `db2inst1`):

```shell
[db2inst1@dibitu ~]$ db2 CREATE DATABASE PILSISKO ON '/pils/dir01','/pils/dir01' DBPATH ON '/pils/pilsisko'
DB20000I  The CREATE DATABASE command completed successfully.
```

### Podłączenie do bazy

Żeby można było wykonyać operacje na bazie, np utworzyć tableletrzeba mieć do niej otwarte połączenie. Można to zrobić na dwa sposoby: W shellu OS, lub w interpretatorze `db2`:

=== "W shellu OS"
    Jeśli planujesz pracować z powiomu shella OS, podłącenie do bazy wygląda tak:

    ```shell
    [db2inst1@dibitu ~]$ db2 connect to pilsisko

       Database Connection Information

     Database server        = DB2/LINUXX8664 12.1.3.0
     SQL authorization ID   = DB2INST1
     Local database alias   = PILSISKO
    ```

=== "W interpreteze `db2`"
    Jeśli lubisz siedzieć bezpośrednio w SQLu, to uruchom `db2` i podłącz się w środku:

    ```shell
    [db2inst1@dibitu ~]$ db2 
    (c) Copyright IBM Corporation 1993,2007
    Command Line Processor for DB2 Client 12.1.3.0

    You can issue database manager commands and SQL statements from the command 
    prompt. For example:
        db2 => connect to sample
        db2 => bind sample.bnd

    For general help, type: ?.
    For command help, type: ? command, where command can be
    the first few keywords of a database manager command. For example:
     ? CATALOG DATABASE for help on the CATALOG DATABASE command
     ? CATALOG          for help on all of the CATALOG commands.

    To exit db2 interactive mode, type QUIT at the command prompt. Outside 
    interactive mode, all commands must be prefixed with 'db2'.
    To list the current command option settings, type LIST COMMAND OPTIONS.

    For more detailed help, refer to the Online Reference Manual.

    db2 => connect to pilsisko

       Database Connection Information

     Database server        = DB2/LINUXX8664 12.1.3.0
     SQL authorization ID   = DB2INST1
     Local database alias   = PILSISKO
    ```

### Odłączanie od bazy

Kążde połączenie do bazy zżera trochę pamięci, więc nieużywane warto rozłączać komendą `db2 disconnect pilsisko` z OSa. Albo z wnętrza interpretera bazy.

### Tworzenie tabeli

Utwórz tabelę `pifko` następującą komendą:

```sql
CREATE TABLE pifko (
    nr        INT NOT NULL GENERATED ALWAYS AS IDENTITY (START WITH 1, INCREMENT BY 1),
    browar    VARCHAR(30)  NOT NULL,
    nazwa     VARCHAR(30)  NOT NULL,
    alk       DECIMAL(9,2) NOT NULL WITH DEFAULT 5,
    typ       VARCHAR(30) NOT NULL WITH DEFAULT 'Pils'
);
```

!!! Note "Uwaga:"
    Ważne jest, żeby na zakończenie koemndy SQL dać średnik `;`. To w połączeniu z parametrem `-t` do interpretera `db2` pozwoli wkleić wielolinijkowy SQL, który będzie wykonany dopiero po napotkaniu średnika. W przeciwnym wypadku durny intrepreter DB2 będzie próbować wykonać każdą linijkę z osobna :shrug:.

Podłacz się do bazy i Wywołaj z wnętrza shella db2:

```shell
[db2inst1@dibitu ~]$ db2 -t
(c) Copyright IBM Corporation 1993,2007
Command Line Processor for DB2 Client 12.1.3.0

[... pierdu-pierdu ...]

db2 => CREATE TABLE pifko (
    nr INT NOT NULL GENERATED ALWAYS AS IDENTITY (START WITH 1, INCREMENT BY 1),
    browar    VARCHAR(30)  NOT NULL,
    nazwa     VARCHAR(30)  NOT NULL,
    alk       DECIMAL(9,2) NOT NULL WITH DEFAULT 5,
    typ       VARCHAR(30) NOT NULL WITH DEFAULT 'Pils'
);db2 (cont.) => db2 (cont.) => db2 (cont.) => db2 (cont.) => db2 (cont.) => db2 (cont.) => 
DB20000I  The SQL command completed successfully.
```

## Przykładowe dane

Za wpakowanie danych do tabeli odpowiada SQLowa komenda `INSERT`. Poniższe polecenie zapakuje kilka piwek do bazy `pils`:

```sql
insert into pifko (browar, nazwa, alk, typ)
    values  ('Pinta', 'Hazy IPA', 4.5, 'IPA'),
            ('Ursa Major', 'Rzeźnik', 3.5, 'Pils'),
            ('Browar trzech kumpli', 'PanIPAni', 6, 'IPA');
```


## Baza `sample`

!!! Note inline end
    To polecenie powinno być wykonane jako właściciel instancji, np `db2inst1`.

Jak chcesz tylko poćwiczyć SQLa, to IBM dostarcza bazę `sample`, którą można wykreować komendą:


```shell
$ db2sampl
```