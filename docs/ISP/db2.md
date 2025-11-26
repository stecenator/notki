# Konfiguracja DB2 jako klienta IBM Storage Protect

Wsparcie dla DB2 jest na poziomie API klienta BA - wystarczy mieć to skonfigurowane i gitara. Ale diabeł oczywiście tkwi w sczegółach, zatem... szczegóły poniżej.
[Oficjalna dokumentacja](https://www.ibm.com/docs/pl/db2/11.5.x?topic=tsm-configuring-client) też jest bardzo fajna.

## Serwer ISP

Serwer nie zajmuje się retencją backupów w imieniu DB2. Za to jest odpowiedzialna sama baza. Daltego wystarczy założyć prostą politykę:

- `VERE` = 1 
- `VERD` = 0
- `RETE` = 0
- `RETO` = 0

!!! Danger "Ważne"
	O ile TSM za retencję backupu DB2 nie odpowiada, o tyle za expirowanie archiwów już tak. A baza używająć`LOGARCHMETH1` , zwala logi do TSMa właśnie jako obiekty archiwalne.  Dlatego warto uzodnić czas retencji logów z DBA bazy.

### Domena, policy set, managment classa i copy grupa

Zakładam, że jest już pula `dc01`, która u mnie zwykle jest kontenerowa. Oczywioście można tu użyć dowolnej puli, jak komu pasuje. Przy LANFree to będzie pewnie taśma, albo `FILE` na jakimś GPFSie.

``` title="Polityki dla DB2"
def dom db2 descr="Klienci db2"
def pol db2 prd desc="Polityka dla DB2"
def mgmt db2 prd dbb migdest=dc01
def copyg db2 prd dbb t=b vere=1 verd=0 rete=0 reto=0 dest=dc01
def copyg db2 prd dbb t=a retver=30 dest=dc01
def mgmt db2 prd logs migdest=dc01 descr="DB2 archlogs"
def copyg db2 prd logs t=a retver=30 dest=dc01
assign defmgmt db2 prd dbb
val pol db2 prd
act pol db2 prd
```

!!! note "Uwaga:"
	W powyższej liście jest "zbędna rzecz": `migdest=dc01`. To dla porządku, bo nie lubię mieć ostrzeżeń podczas validacji policysetu. 


!!! danger "Ważne:"
	Jeśli planujesz archiwizację logów (1) potrzebujesz conajmniej copygrupy archiwalnej w domyślnej managment class. A pewnie lepszym pomysłem jest zrobienie dedykowanej managment classy pod logi. 
	{ .annotate }
	
	1. prawdopodobnie planujesz, bo bez tego życie jest smutne :cry:.

	W powyższym przykładzie jest zdefiniowana klasa `LOGS` z copygrupą archiwalną, której planuję użyć do archiwizacji logów. 

	!!! Tip "Ciekawostka"
		Ponieważ copygrupy backupowa i archiwalna mogą mieć innne `destination` możliwe jest rozdzielenie backupu od logów. Można np skierować backupy na :material-tape-drive: a logi na deduplikowane :material-harddisk:.

### Klient

Klientów będzie tak naprawdę dwóch: dla bazy (API) i dla OSa (BA).

Założenia:

- Hostname i nodename klienta db2: `dibitu`
- Nodename dla klienta API: `dibitu_db2`
- klientów API rejestruję w odpowiednich dla nich domenach.
- Klientów OS rejestruję w domenie np `OS` albo jak w poniżej w `LNX` jeśli akurat lubię mieć OSy porozdzielane. 
- Adres mojego serwera Protect: `sp-1.iic`


#### Klient dla bazy

Klient dla bazy będzie służył wyłącznie do połączeń API wykonych przez silnik bazy danych.

!!! Note "Uwaga:"
	Ważne jest, żeby klient miał prawo kasowania swoich backupów. W przeciwnym wypadku one nigdy nie wygasną! 

```
reg node dibitu_db2 tajne_hasło dom=DB2 backdel=yes sessionsec=trans
```

#### Klient dla OS i harmonogramów


Na tym kliencie będzie robiony backup plików z tego hosta, oraz będzie on słuchał harmonogramów, które np będą wywoływać skrypty backupujące bazę. 

```
reg node dibitu tajne_hasło dom=LNX sessionsec=trans
```

## Serwer DB2

Na hoście DB2 potrzebny jest pałeny klientw *Backup Archive*. [Stąd](https://www3.software.ibm.com/storage/tivoli-storage-management/maintenance/client/v8r1/Linux/LinuxX86/BA/) (1) można sciągnąć względnie świeżego. 
{ .annotate }

1.	Z pewnych źródeł wiem, że niedługo będzie wersja 8.2 zarówno serwera jak i klienta więc traktuj ten link ze zrozumieniem :wink:.

### Instalacja klienta BA

Z punktu widzenia DB2 potrzebna jest tylko paczka API, ale ze względu na możliwość uruchamiania hamrmonogramóœ jak i przeszukiwania bazy Protecta, ja zawze instalauję pełnego klienta.
Proces instalacji klietna ba jest opisany [tutaj](ba.md).

### Konfiguracja klienta BA

Kluczowy jest plik `dsm.sys`, który musi zawierać dwoe stanze: jedną dla klienta BA a drugą do DB2. podstawowoą konfigurację klietna BA  opisuję [tutaj](ba.md), alt to jest ogólne. Teraz podstawię sobie zmienne pod moją przykładową konfigurację:

!!! Note inline end "Uwaga"
	Stanza `SP-1-DB2` dla DB2 jest trochę inna:

	1. Ma inny `nodename` - to jest konto dla BAZY.
	1. Ma zdefiniowany `passworddir`. Ważne żeby ten katalog był dostępny do zapisu dla właściciela instancji.
	1. Ma inne ścieżki do logów backupowych `errorlogname` i `schedlogname`. Te katalogi też powinny być "pisalne" dla `db2inst1`. 

``` title="Plik /opt/tivoli/tsm/client/ba/bin/dsm.sys"
servername SP-1         * Alias dla klienta BA (OS)
        tcpserveraddress        sp-1.iic
        errorlogn               /var/log/tsm/dsmerror.log
        errorlogret             10 d
        schedlogn               /var/log/tsm/dsmsched.log
        schedlogret             10 d
        passwordaccess          generate
        nodename                dibitu
        * inclexcl                /etc/inclexcl.txt
        resourceutilization     6
        deduplication           yes
        dedupcachepath          /var/spdedup
        ENABLEDEDUPCache        yes
        virtualmount            /etc
        managedservices         schedule webclient
        httpport                1581

servername SP-1-DB2     * Alias dla klienta BA (OS)
        tcpserveraddress        sp-1.iic
        errorlogn               /pils/pilsisko/tsm/logs/dsmerror-db2.log
        errorlogret             10 d
        schedlogn               /pils/pilsisko/tsm/logs/dsmsched-db2.log
        schedlogret             10 d
        passwordaccess          generate
        passworddir				/pils/pilsisko/tsm/pwd
        nodename                dibitu_db2
        * inclexcl                /etc/inclexcl.txt
        resourceutilization     6
        deduplication           yes
        dedupcachepath          /var/spdedup-db2
        ENABLEDEDUPCache        yes
        virtualmount            /etc
        managedservices         schedule webclient
        httpport                1582
```

Plik `dsm.sys` ma dwie stanze. Ta o nazwie `SP-1-DB2` jest przeznaczona dla bazy DB2.
Plik `dsm.opt` wskazuje na domyślną stanze `dsm.sys`, także to od niego zależy która konfiguracja będzie użyta.

``` title="Plik /opt/tivoli/tsm/client/ba/bin/dsm.opt"
servername SP-1
```

Dla DB2 zostanie utworzony dodatkowy plik `opt`, który pozwoli mu skorzystać z drugiej stanzy. Na razie przetestuj połączenie klienta BA:

```shell title="Pierwsze połączenie klienta dsmc"
[root@dibitu ba-8.1.27]# dsmc
IBM Storage Protect
Command Line Backup-Archive Client Interface
  Client Version 8, Release 1, Level 27.0 
  Client date/time: 11/23/2025 00:57:46
(c) Copyright IBM Corp. 1990, 2025. All Rights Reserved. 

Node Name: DIBITU
ANS1051I Invalid user id or password
Please enter your user id <DIBITU>: 

Please enter password for user id "DIBITU": 

Session established with server SP1: Linux/ppc64le
  Server Version 8, Release 1, Level 27.000
  Server date/time: 11/23/2025 00:58:00  Last access: 11/22/2025 20:49:19
Protect> 

```

### Konfiguracja API TSM w DB2

Odpowiednią stanzę w `dsm.sys` już mam. DB2 używa TIVSm-API, dlatego plików konfiguracyjnych domyślnie szuka w `/opt/tivoli/tsm/client/api/bin64` (1). O ile `dsm.sys` może i nawet lepiej, żeby był wspólny o tyle `dsm.opt` warto mieć swój. Odnośnie `dsm.opt` są dwie szkoły:
{ .annotate }

1. Na AIXie to będzie `/usr/tivoli/tsm/client/api/bin64`.

=== "Elegancka"

	Plik `dsm.opt` tworzy się w jakimś ładnym miejscu, np na współdzielnym filesystemie i podaje się go albo przez parametr `-optfile=/scieżka/do/dsm.opt` albo przez zmienną środowiskową DSMI_CONFIG wskazującą konkretny na plik `dsm.opt` (1). 
	{ .annotate }

	1. :exclamation: Może mieć zupełnie inną nazwę :exclamation:

	Na przykład plik sobie leży we współdzielnym katalogu: `/pils/pilsisko/tsm/dsm-db2.opt` i wskazuje sobie na odpowiednią stanzę w `dsm.sys`:

	```
	SErvername SP-1-DB2
	```

	W dalszych przykładach posługuję się wersją "elegancką" :smile:.

=== "Prosta"

	Tworzy się plik `/opt/tivoli/tsm/client/api/bin64/dsm.opt` wskazujący na odpowiedni wpis w `dsm.sys`:

	```
	SErvername SP-1-DB2
	```

	Ta metoda ma sens przy prostych bazach, które nie są w klastrze, ani nie są spartycjonowane.

!!! Tip "Wskazówka:"
	Zmienne środwiskowe TSM ustawia się w `~db2inst1/sqllib/userprofile` i zwykle są to:

	- `DSMI_DIR` - Określa zdefiniowaną przez użytkownika ścieżkę do katalogu, w którym znajduje się zaufany plik agenta API (dsmtca)
	- `DSMI_CONFIG` - Identyfikuje ścieżkę katalogu zdefiniowaną przez użytkownika dla pliku `dsm.opt`, który zawiera opcje użytkownika TSM. W przeciwieństwie do pozostałych dwóch zmiennych, ta zmienna powinna zawierać pełną ścieżkę i nazwę pliku.
	- `DSMI_LOG` - Określa zdefiniowaną przez użytkownika ścieżkę do katalogu, w którym zostanie utworzony dziennik błędów (dsierror.log).

### Wspólny `dsm.sys`

Można dyskutować, czy to jest dobre. Ja tak lubię. Jako `root` podlinkuj, jak na poniższym przykładzie:

```shell
[root@dibitu bin64]# pwd
/opt/tivoli/tsm/client/api/bin64
[root@dibitu bin64]# ln -s ../../ba/bin/dsm.sys .
[root@dibitu bin64]# ls -la dsm.sys
lrwxrwxrwx. 1 root root 20 Nov 23 11:40 dsm.sys -> ../../ba/bin/dsm.sys
```

### Indywidialny `dsm-db2.opt`


Robię metodą "elegancką", czyli każda instancja będzie miała swój własny plik `dsm.opt`. U mnie to:

!!! Info inline end
	Jeśli nie napisałem inaczej, to konfigurację trzeba robić jako włąściciel instancji

```shell title="Lokalizacja dsm.opt dla DB2"
[db2inst1@dibitu cfg]$ pwd
/pils/pilsisko/tsm/cfg
[db2inst1@dibitu cfg]$ cat dsm.opt 
SErvername SP-1-DB2
```

### Zmienne środowiskowe Storage Protect API

!!! Warning inline "Uwaga:"
	Częstym błędem jest robienie wskazanych tu katalogów jako `root`. Ważne jest, żeby te katalogi były dostępne dla użytkownika instancji. W szczególności `DSMI_LOG` musi być dostępny do zapisu.

Ponieważ chcę to mieć zrobione elegancko, muszę wskazać instancji gdzie są jej  pliki konfiguracyjne API TSM. W tym celu, trzeba dodać następujace wpisy do `~db2inst1/sqllib/userprofile`:


```sh title="Zmienne środowiskowe Storage Protect"
DSMI_DIR=/opt/tivoli/tsm/client/api/bin64
DSMI_CONFIG=/pils/pilsisko/tsm/cfg/dsm-db2.opt
DSMI_LOG=/pils/pilsisko/tsm/logs
export DSMI_DIR DSMI_CONFIG DSMI_LOG
```

#### Weryfikacja środowiska

Przeloguj się, i sprawdź czy zmienne się załadowały i wskazują na poprawne katalogi. Pomyłka w tym miejscu jest upierdliwa w późniejszym wyłapaniu.

```shell title="Weryfikacja zmiennych"
[db2inst1@dibitu ~]$ echo $DSMI_DIR
/opt/tivoli/tsm/client/api/bin64
[db2inst1@dibitu ~]$ ls -la $DSMI_CONFIG
-rw-r--r--. 1 db2inst1 db2inst1 20 Nov 23 11:31 /pils/pilsisko/tsm/cfg/dsm-db2.opt
[db2inst1@dibitu ~]$ ls -lad $DSMI_LOG
drwxr-xr-x. 2 db2inst1 db2inst1 6 Nov 23 12:13 /pils/pilsisko/tsm/logs
```

!!! Warning "Ważne!"
	Po każdej zmianie w zmiennych środowiskowych, trzeba przeładować *database managera*, co oznacza chwilowy brak dostępu do baz :exclamation: W sesji z "nowymi" zmiennymi `DSMI*` Można zrobić to tak:

	```shell
	[db2inst1@dibitu ~]$ set | grep DSMI
	DSMI_CONFIG=/pils/pilsisko/tsm/cfg/dsm-db2.opt
	DSMI_DIR=/opt/tivoli/tsm/client/api/bin64
	DSMI_LOG=/pils/pilsisko/tsm/logs
	[db2inst1@dibitu ~]$ db2stop
	11/23/2025 12:36:20     0   0   SQL1064N  DB2STOP processing was successful.
	SQL1064N  DB2STOP processing was successful.
	[db2inst1@dibitu ~]$ db2start
	11/23/2025 12:36:34     0   0   SQL1063N  DB2START processing was successful.
	SQL1063N  DB2START processing was successful.
	```


#### LOGARCHMETH1

Ustawienie archiwizacji logów na cokolwiek jest kluczowe. Bez tego możliwe będa tylko backupy offline. Archwizację logów do Protecta ustawaia się komendą:

```shell title="Ustawianie archiwizacji logów"
db2 update db cfg for <moja_baza> using logarchmeth1 tsm:<klasa_dla_logów>
```

!!! Example "Przykład"
	```shell
	[db2inst1@dibitu ~]$ db2 update db cfg for pilsisko using logarchmeth1 tsm:logs
	DB20000I  The UPDATE DATABASE CONFIGURATION command completed successfully.
	SQL1363W  One or more of the parameters submitted for immediate modification 
	were not changed dynamically. For these configuration parameters, the database 
	must be shutdown and reactivated before the configuration parameter changes 
	become effective.
	```

### Połączenie DB2 i Storage Protect

Wywołaj polecenie `~/sqllib/adsm/dsmapipw`:

```sh title="Zmiana hasła i test komunikacji z TSM dla noda DB2"
[db2inst1@dibitu ~]$ ./sqllib/adsm/dsmapipw 

*************************************************************
* Tivoli Storage Manager                                    *
* API Version = 8.1.27                                       *
*************************************************************
Enter your current password:
Enter your new password:
Enter your new password again:

Your new password has been accepted and updated.
```

Jednocześnie w ACTLOGu TSMa powinno być widać coś takiego:

``` title="ACTLOG z nawiązania sesji przez noda DB2"
ANR0839I Session 42075 started for node DIBITU_DB2 (Linux x86-64) (SSL 10.10.3.93:35244) on sp-1:1500.
ANR0403I Session 42075 ended for node DIBITU_DB2 (Linux x86-64).
ANR8592I Session 42076 connection is using protocol TLSV13, cipher specification TLS_AES_256_GCM_SHA384, certificate TSM Self-Signed 
Certificate. 
ANR0839I Session 42076 started for node DIBITU_DB2 (Linux x86-64) (SSL 10.10.3.93:35254) on sp-1:1500.
ANR0403I Session 42076 ended for node DIBITU_DB2 (Linux x86-64).
ANR8592I Session 42077 connection is using protocol TLSV13, cipher specification TLS_AES_256_GCM_SHA384, certificate TSM Self-Signed 
Certificate. 
ANR0839I Session 42077 started for node DIBITU_DB2 (Linux x86-64) (SSL 10.10.3.93:47422) on sp-1:1500.
ANR0403I Session 42077 ended for node DIBITU_DB2 (Linux x86-64).
```

We właściwiościach noda `DIBITU_DB2` na TSMie będzie też widać zmianę atrybutu `Platform` przed i po nawiązaniu komunikacji:

=== "Przed"

	```
	Protect: SP1>q node dom=db2

	Node Name                     Platform     Policy Domain      Days Sinc-     Days Sinc-     Locked?
	                                           Name                  e Last      e Passwor-     
	                                                                  Access          d Set     
	-------------------------     --------     --------------     ----------     ----------     -------
	DIBITU_DB2                    (?)          DB2                         1              1       No 
	```

=== "Po"

	```
	Protect: SP1>q node dom=db2

	Node Name                     Platform     Policy Domain      Days Sinc-     Days Sinc-     Locked?
	                                           Name                  e Last      e Passwor-     
	                                                                  Access          d Set     
	-------------------------     --------     --------------     ----------     ----------     -------
	DIBITU_DB2                    Linux        DB2                        <1             <1       No   
	                               x86-64
	```

## Backup do Storage Protect

Jeżeli nie ma potrzeby używania *proxy nodów*, czyli nie ma klastrów, ani środowiska PureScale, to właściwie wszystko jest gotowe do backupu i... odtwarzania.
DB2 o dorosła baza, więc ma pierdyliony możliwości backupu i odtwarzania. Nietkóre będa wymagały dodatkowych ustawień i/lub licencji. Na początek robię prosy backup `offline`.

### Backup offline bazy `pilsisko`

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

## Co dalej?

[Dalej](../db2/back_n_rest.md) jest backup i restore we wszystkich możliwych smakach.