# Widmowo-obronne Kury SQLowe 

## Gmeranie przy taśmach bibliotecznych

### Napędy i urządzenia "by server"

Lista wszystkich napędów, takżę typu `FILE`

- serwer
- napęd
- serial
- device


Jednolinijkowiec do kopiowania:

```sql
select cast(source_name as char(15)) src, cast(pt.LIBRARY_NAME as char(15)) lib, cast(dr.DRIVE_NAME as char(15)) drv, cast(pt.device as char(20)) dev,  cast(dr.drive_serial as char(20)) serial, cast(pt.online as char(8)) online from drives dr, paths pt  where dr.drive_name = pt.destination_name order by src, lib, drv
```

Ładnie:

```sql
select cast(source_name as char(15)) src, -
		cast(pt.LIBRARY_NAME as char(15)) lib, -
		cast(dr.DRIVE_NAME as char(15)) drv, -
		cast(pt.device as char(20)) dev, -
		cast(dr.drive_serial as char(20)) serial, -
		cast(pt.online as char(8)) online -
	from drives dr, paths pt -
	where dr.drive_name = pt.destination_name -
	order by src, lib, drv
```

Lista napędów **innych** niż `FILE`, jednolinijkowiec:

```sql 
select cast(source_name as char(15)) src, cast(pt.LIBRARY_NAME as char(15)) lib, cast(dr.DRIVE_NAME as char(15)) drv, cast(pt.device as char(20)) dev,  cast(dr.drive_serial as char(20)) serial, cast(pt.online as char(8)) online from drives dr, paths pt  where pt.device <> 'FILE' and dr.drive_name = pt.destination_name order by src, lib, drv
```

Ładnie:

```sql
select cast(source_name as char(15)) src, - 
		cast(pt.LIBRARY_NAME as char(15)) lib, -
		cast(dr.DRIVE_NAME as char(15)) drv, -
		cast(pt.device as char(20)) dev, -
		cast(dr.drive_serial as char(20)) serial, -
		cast(pt.online as char(8)) online -
	from drives dr,paths pt -
	where pt.device <> 'FILE' and dr.drive_name = pt.destination_name -
	order by src, lib, drv
```

1. Generator komendy `del vol` dla pustych taśm w puli:

	```sql
	select 'del vol ' as qra, cast(volume_name as char(8)) VN, ' w=y' WAIT from volumes where volume_name  in ( select volume_name from libvolumes where library_name='TS4500KON' and volume_name like '%L5' and status='Private') and status='EMPTY' and stgpool_name='ORACLECOPY'
	```

1. Kadydaci do reclaimu dla puli:

	```sql
	select volume_name from volumes where status='FULL' and PCT_UTILIZED<50 and stgpool_name='I500POOLCP'
	```

1. Puste wolumeny pulowe w bibliotece:

	```sql
	select cast(volume_name as char(12)) VN, cast(stgpool_name as char(15)) PN, cast(access as char(10)) acc, status  from volumes where volume_name in ( select volume_name from libvolumes where library_name='TS4500KON' and volume_name like '%L5' and status='Private') and status='EMPTY'
	```
1. **Nieaktualne. Lepiej użyć `perform libaction`** Generator makra masowego podnoszenia ścieżek:

	```sql
	select 'upd path ' as upd, cast(SOURCE_NAME as char(15)) as  ,cast(DESTINATION_NAME as char(12)) as dest, 'srct=server destt=drive' as types, concat('libr=',cast(LIBRARY_name as char(20))) as libr, 'onlin=yes' as onl  from paths where online='NO' and destination_type='DRIVE'
	```

	Przykładowy output:

	```tsm
	Protect: WAW5-TSM-SRV01>run PADLINA_PATH_UP
	UPD            AS                   DEST              TYPES                        LIBR                           ONL       
	----------     ----------------     -------------     ------------------------     --------------------------     ----------
	upd path       WAW5-TSM-SRV01       WAW5-PTDRV13      srct=server destt=drive      libr=WAW5-TSM01-LIB            onlin=yes 
	upd path       WAW5-TSM-SRV01       WAW5-PTDRV14      srct=server destt=drive      libr=WAW5-TSM01-LIB            onlin=yes 
	upd path       WAW5-TSM-SRV01       WAW5-PTDRV15      srct=server destt=drive      libr=WAW5-TSM01-LIB            onlin=yes 
	upd path       WAW5-TSM-SRV01       WAW5-PTDRV16      srct=server destt=drive      libr=WAW5-TSM01-LIB            onlin=yes
	```

 	Definicja skryptu:

	```
	def scr paths_up -
	"select 'upd path ' as upd, -
		cast(SOURCE_NAME as char(15)) as src, -
		cast(DESTINATION_NAME as char(12)) as dest, -
		'srct=server destt=drive' as types, -
		concat('libr=',cast(LIBRARY_name as char(20))) as libr, -
		'onlin=yes' as onl -
	from paths -
	where online='NO' and destination_type='DRIVE'" -
	desc="Makro do podnoszeni sciezek"
	```

1. Scieżki OFFLINE (trochę ładniej niż `q path`:

	```sql
	select cast(SOURCE_NAME as char(15)) src, -
	 cast(DESTINATION_NAME as char(15)) dst, - 
	 cast(p.LIBRARY_NAME as char(15)) libr, - 
	 cast(DEVICE as char(40)) as dev, - 
	 cast(drive_serial as char(15)) as serial, -
	 WWN -
	from paths p, drives d -
	where p.online<>'YES' and d.drive_name=p.destination_name
	```

	Definicja skryptu w SP:

	```
	def scr offline_paths "select cast(SOURCE_NAME as char(15)) src, cast(DESTINATION_NAME as char(15)) dst, cast(p.LIBRARY_NAME as char(15)) libr, cast(DEVICE as char(20)) as dev,  cast(drive_serial as char(15)) as serial, WWN from paths p, drives d where p.online <> 'YES' and d.drive_name = p.destination_name" -
		desc="Lista sciezek OFFLINE"
	```

## Klasy urządzeń

1. DevClass (raczej sekwencyjne)

	```sql
	select DEVCLASS_NAME,ACCESS_STRATEGY,DEVTYPE,FORMAT,CAPACITY /1024 as GIB, MOUNTLIMIT, cast(DIRECTORY as char(50)) dir from devclasses
	```

## Statystyki i zbieranie użytecznych danych (storage)

Tu są skrypty, które przydają się w porannej kawie i ogólnej ocenie stanu zdrowia TSMa od strony pamięci: bilioteki, woluminy, pule

1. Taśmy o ostatnim odczycie starszym niż 90 dni:

	```sql
	select VOLUME_NAME, LAST_WRITE_DATE 
	from volumes 
	where days(current date) - days(LAST_READ_DATE) > 90 
	order by LAST_WRITE_DATE
	```


1. Policzenie taśm w rożnych statusach we wszystkich bibliotekach:

	```sql
	select cast(library_name as char(15)) Libr, status, count(volume_name) as tape -
	from libvolumes -
	group by library_name, status
	```

	Wersja jednolinijkowa:
  
	```sql
	select cast(library_name as char(15)) Libr, status, count(volume_name) as tape from libvolumes group by library_name, status
	```
   
   Definicja skryptu **`tape_stats`**:

   ```
   def scr tape_stats "select cast(library_name as char(15)) Libr, status, count(volume_name) as tape from libvolumes group by library_name, status"
   ```

1. Statystyki woluminów w pulach z rozbiciem na reclaimowalne. **`vol_stats`** i nie:

	Zlicza wolimuny w stanach `Filing`, `Full<50` (jako `Recl`), `Full` i `Pending`

	```sql
	select STGPOOL_NAME, 
		cast(case -
			when Status='FULL' and PCT_UTILIZED>=50 then 'FULL' -
			when Status='FULL' and PCT_UTILIZED<49 then 'RECLAIM' -
			else STATUS -
			END as char(10)) as stat, -
		count(volume_name) as vols -
	from volumes -
	group by STGPOOL_NAME, 
		case -
			when Status='FULL' and PCT_UTILIZED>=50 then 'FULL' -
			when Status='FULL' and PCT_UTILIZED<49 then 'RECLAIM' -
			else STATUS END - 
	order by stgpool_name, stat
	```

	Definicja jako skrypt **`vol_stats`** (można kopiować i wklejać w całości bo są `-` na końcach linii):

	```
	define script vol_stats -
	"select STGPOOL_NAME, cast(case when Status='FULL' and PCT_UTILIZED>=50 then 'FULL' when Status='FULL' and PCT_UTILIZED<49 then 'RECLAIM' else STATUS END as char(10)) as stat, count(volume_name) as vols from volumes group by STGPOOL_NAME, case when Status='FULL' and PCT_UTILIZED>=50 then 'FULL' when Status='FULL' and PCT_UTILIZED<49 then 'RECLAIM' else STATUS END order by stgpool_name, stat" -
	desc="Statusy tasm w pulach"
	```

1. Statystyki pul. Teki trochę ładniejsze `q stg` ;-)


	```sql
	select cast(stgpool_name as char(20)) as STG, -
		PCT_UTILIZED, -
		RECLAIM, -
		RECLAIMPROCESS, -
		MIGPROCESS, -
		lpad((NUMSCRATCHUSED || '/' || MAXSCRATCH),10,' ') as Scr,  -
		dec(dec(NUMSCRATCHUSED,6,2)/dec(MAXSCRATCH,6,2)*100, 5,1) as ScrPct  -
	from stgpools -
	where maxscratch>0 -
	order by ScrPct
	```

	Definicja skryptu **`stg_stats`**:

	```
	define script stg_stats "select cast(stgpool_name as char(20)) as STG, PCT_UTILIZED, RECLAIM, RECLAIMPROCESS, MIGPROCESS, lpad((NUMSCRATCHUSED || '/' || MAXSCRATCH),10,' ') as Scr, dec(dec(NUMSCRATCHUSED,6,2)/dec(MAXSCRATCH,6,2)*100, 5,1) as ScrPct from stgpools where maxscratch>0 order by ScrPct" -
	desc="Statystyki pul"
	```

## Pliki, filespace i zawartość wolumenów

1. Filespace na taśmie:

	```sql
	select distinct NODE_NAME NN,FILESPACE_NAME FN, volume_name VN  from contents where volume_name in ('180AABL5', '181AABL5')
	```

## Nody i filespace

1. Ogólny raport o klinetach. Wersje, IP, sortowany według ostatniego dostępu (najstarsi, czyli trupy z szafy, na górze):

	```sql
	select cast(node_name as char(15)) Node,cast(DOMAIN_NAME as char(20)) Domain, -
	 cast(CLIENT_VERSION || '.' || CLIENT_RELEASE || '.' || CLIENT_LEVEL || '.' || CLIENT_SUBLEVEL as char(12)) as ver, -
	 cast(APPLICATION_VERSION || '.' || APPLICATION_RELEASE || '.' || APPLICATION_LEVEL || '.' || APPLICATION_SUBLEVEL as char(15)) as app, -
	 PLATFORM_NAME, -
	 cast(CLIENT_OS_LEVEL as char(15)) as os_ver, -
	 cast(TCP_NAME as char(25)) as hostname, -
	 cast(TCP_ADDRESS as char(16)) as ip, -
	 days(current date) - days(LASTACC_TIME) as LAST_ACC -
	from nodes -
	order by LAST_ACC desc, NODE_NAME asc
	```

	Definicja skryptu:
  
	```
	define script node_stats -
	"select cast(node_name as char(15)) Node,cast(DOMAIN_NAME as char(20)) Domain, cast(CLIENT_VERSION || '.' || CLIENT_RELEASE || '.' || CLIENT_LEVEL || '.' || CLIENT_SUBLEVEL as char(12)) as ver, cast(APPLICATION_VERSION || '.' || APPLICATION_RELEASE || '.' || APPLICATION_LEVEL || '.' || APPLICATION_SUBLEVEL as char(15)) as app, PLATFORM_NAME, cast(CLIENT_OS_LEVEL as char(15)) as os_ver, cast(TCP_NAME as char(25)) as hostname, cast(TCP_ADDRESS as char(16)) as ip, days(current date) - days(LASTACC_TIME) as LAST_ACC from nodes order by LAST_ACC desc, NODE_NAME asc" -
	desc="Trupy w szafie"

	```

1. Węzły, które się nie kontaktowały od 30 dni:

	```sql
	select cast(node_name as char(25)) NN, cast(domain_name as char(12)) DN, (days(current date) - days(LASTACC_TIME))  days_ina 
	from nodes 
	where  (days(current date) - days(LASTACC_TIME))>30 
	order by domain_name,  days_ina
	```

	Jednolinijkowiec: 

	```sql
	select cast(node_name as char(25)) NN, cast(domain_name as char(12)) DN, (days(current date) - days(LASTACC_TIME))  days_ina from nodes where  (days(current date) - days(LASTACC_TIME))>30 order by domain_name,  days_ina
	```

1. Filespacee z zakończonym backupem wcześniej niż 30 fdni temu:

	Ładne:

	```sql
	select cast(node_name as char(15)) node, -
		cast(FILESPACE_NAME as char(35)) FS, -
		(days(current date) - days(BACKUP_END)) LAST_FS_BKP -
	from filespaces -
	where  (days(current date) - days(BACKUP_END))>30 -
	order by LAST_FS_BKP desc
	```

	Do kopiowania:

	```sql
	select cast(node_name as char(15)) node, cast(FILESPACE_NAME as char(35)) FS, (days(current date) - days(BACKUP_END))  LAST_FS_BKP from filespaces where  (days(current date) - days(BACKUP_END))>30 order by LAST_FS_BKP desc
	```

1. MB backupu z dzisiaj:

	```sql
	select cast(entity as char(20)) kto , sum(seconds_between(end_time, start_time))as sekundy, sum(bytes)/1024/1024 MiB -
	from summary -
	where activity='BACKUP' and  date(current date) = date(start_time) -
	group by entity
	```

	Do kopiowania:

	```sql
	select cast(entity as char(20)) kto , sum(seconds_between(end_time, start_time))as sekundy, sum(bytes)/1024/1024 MiB from summary where activity='BACKUP' and  date(current date) = date(start_time)group by entity
	```

1. Dzienny workload w MiB z ostatnich 30 dni (bo tyle ma tabela `summary_extended`)

	```sql
	select cast(entity as char(20)) kto, cast(activity as char(15)) as co, dec(dec(sum(bytes), 30,0)/1048576, 10, 2) as MiBs, date(start_time) as day from summary_extended where activity in ('BACKUP', 'ARCHIVE') group by entity, date(start_time), activity having sum(bytes)>0 order by day, MiBs desc
	```

	**Uwaga:** - to jest do poprawki. Warto by posumować BACKUP + ARCHIVE + HSM. 
	**Pomysł:** - można zrobić podobną qrę na ruchy wewnętrzne.

1. Ile MB zajmują nody, które nie kontaktowały się z serwerem dłużej niź 30 dni:

	```sql
	select a.node_name, sum(LOGICAL_MB) from occupancy a  where a.node_name in ( select node_name from  nodes where  (days(current date) - days(LASTACC_TIME))>30 ) group by a.node_name
	```

1. Auditoccupancy by domain:

	```sql
	select n.domain_name, -
		sum(o.total_mb) tot_mb -
	from nodes n , auditocc o -
	where n.node_name=o.node_name -
	group by n.domain_name -
	order by n.domain_name
	```

	Skrypt `dom_auditocc`:

	```
	select n.domain_name, sum(o.total_mb) tot_mb from nodes n , auditocc o where n.node_name=o.node_name group by n.domain_name by n.domain_name
	```

1. Wszystkie nody, które skończyły harmonogramy z niezerowym rezultatem w ciągu ostatnich 24h:

	```sql
	select node_name, result, date(actual_start)  from events where result>0 and days(ACTUAL_START) = days(current date)
	```

## Dirpoole 
 
1. Generator `move container` dla kontenerów z zadaną ilością wolnego miejsca:

	```sql
	SELECT 'move container '|| SUBSTR(CONTAINER_NAME,1,50) AS CONTAINER_NAME, 'defrag=yes '|| CAST(FREE_SPACE_MB AS DECIMAL(8,0)) as "FREE_SPACE_MB", SUBSTR(TOTAL_SPACE_MB,1,5) AS TOTAL_SPACE_MB from containers where FREE_SPACE_MB>10 and STATE='AVAILABLE' and CONTAINER_NAME not like '%N:\%' order by FREE_SPACE_MB desc
	``` 

## Polityki

1. Polityki backupu wraz z destination:

	**Uwaga:** Niektóre kolumny są castowane na krótsze `char'y`, żeby ładnie wyglądały, więc coś możę być ucięte!
	
	```sql
	select cast(DOMAIN_NAME as char(20)) Dom, -
  		cast(set_name as char(20)) Set, -
  		cast(CLASS_NAME as char(20)) Mgmt, - 
  		VEREXISTS VerE, VERDELETED VerD, RETEXTRA RetE, RETONLY RetO, -
  		cast(DESTINATION as char(20)) as Dest - 
  	from bu_copygroups -
  	order by DOMAIN_NAME, SET_NAME, CLASS_NAME
	```

1. Polityki archiwizacji wraz z destination:

	**Uwaga:** Niektóre kolumny są castowane na krótsze `char'y`, żeby ładnie wyglądały, więc coś możę być ucięte!

	```sql
	select cast(DOMAIN_NAME as char(20)) Dom, -
  		cast(CLASS_NAME as char(20)) Mgmt, -
  		RETVER RetV, -
  		cast(DESTINATION as char(20)) as Dest -  
	from ar_copygroups order by DOMAIN_NAME, SET_NAME, CLASS_NAME
	```

1. Kopiowanie polityk archiwalnych. 

	Generuje `define copyg` z istniejących polityk:

	```sql
	select 'def copyg SAP ',SET_NAME,CLASS_NAME, 't=a', concat('retver=',RETVER), concat('dest=',DESTINATION) from ar_copygroups where domain_name='SAP' and set_name <> 'ACTIVE'
	```

1. Kopiowanie polityk backupowych.

	Generuje `define copyg` z istniejących polityk backupu:

	```sql
	select 'def copyg ',
	DOMAIN_NAME, 
	SET_NAME, 
	class_name, 
	concat('vere=',VEREXISTS), 
	concat('verd=',VERDELETED), 
	concat('rete=',RETEXTRA), 
	concat('reto=',RETONLY),
	concat('dest=',destination)  
	from bu_copygroups 
	where SET_NAME <> 'ACTIVE'
	```

	Wersja do skopiowania do terminala **Uwaga podstaw ID i hasło:**

	```shell
	$ dsmadmc -se=ztsm.kg -id=XXX -pa=XXX -dataonly=yes "select 'def copyg ',DOMAIN_NAME, SET_NAME, class_name, concat('vere=',VEREXISTS), concat('verd=',VERDELETED), concat('rete=',RETEXTRA), concat('reto=',RETONLY) ,concat('dest=',destination)  from bu_copygroups where SET_NAME <> 'ACTIVE' " | tr -s ' '
	```
