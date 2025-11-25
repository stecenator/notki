# Backup i restore DB2

Z założenia będę tu używać Protecta, ale cał ideologia backupu DB2 jest praktycznie niezależna od nośnika, dlateg ten rozdział leży w kategorii *DB2* a nie *[Storage Protect](../ISP/index.md*.

## Offline backup bez logów

!!! Info inline end
	Bazy nie można używać podczas tego typu backupu. Plusem jest to, że backup jest aktualzny na czas tworzenia (nie gromadzą się logi).

Najprostszy. Chyba zbyt prosty, bo offline i na dodatek bez logów.
Sprowadza się do nastęþujących kroków:

1. Deaktywacja bazy.
1. Backup *offline*.
1. Aktywacja bazy.


### Deaktywacja bazy

Na początek, trzeba wyciszyć bazę. W shellu użytkownika instancji (1) wykonaj poniższą komendę:
{ .annotate }

1. Albo innego uprawnionego do wykonywania backupów.


```shell title="Wyciszanie bazy do backupu"
db2 => connect to pilsisko

   Database Connection Information

 Database server        = DB2/LINUXX8664 12.1.3.0
 SQL authorization ID   = DB2INST1
 Local database alias   = PILSISKO

db2 => quiesce database immediate force connections
DB20000I  The QUIESCE DATABASE command completed successfully.
db2 => unquiesce database
DB20000I  The UNQUIESCE DATABASE command completed successfully.
db2 => terminate
DB20000I  The TERMINATE command completed successfully.
[db2inst1@dibitu ~]$ db2 deactivate database pilsisko
DB20000I  The DEACTIVATE DATABASE command completed successfully.
```

!!! Quote "Skrypt"
	Zamiast klepać te poleceania, można to wrzucic do pliku np.: `db_prep.txt`:

	```
	CONNECT TO pilsisko
	QUIESCE DATABASE IMMEDIATE FORCE CONNECTIONS;
	UNQUIESCE DATABASE;
	TERMINATE;
	DEACTIVATE DATABASE database-alias
	```

	I zapuścić komendą `db2 -tf db_prep,txt`

### Backup *offline*

Po deaktywacji bazy można puścić backup:

```shell title="Offline backup, bez logów"
[db2inst1@dibitu ~]$ db2 backup db pilsisko  use tsm

Backup successful. The timestamp for this backup image is : 20251123132004
```
Na serwerze Protect pojawi się `filespace` z nazwą bazy:

``` title="Filespace węzła DIBITU_DB2"
Protect: SP1>q files dibitu_db2

Node Name           Filespace           FSID     Platform     Filespac-     Is Filesp-        Capacity      Pct 
                    Name                                      e Type        ace Unico-                      Util
                                                                               de?                         
---------------     -----------     --------     --------     ---------     ----------     -----------     -----
DIBITU_DB2          /PILSISKO              1     DB2/LIN-     API:DB2/-         No              201 MB     100,0
                                                  UXX8664      LINUXX8-                                         
                                                               664  
```

### Reaktywacja bazy

Reaktywacja bazy odbywa się komendą:

```shell title="Reaktywacja bazy po backupie"
db2 => activate database pilsisko
```

!!! Note "Do rozkminy"
	Nie wiem dlaczego to działa, ale nie musiałem aktywować bazy po backupie. TRzeba spytać jakiegoś inkwizytora od DB2.