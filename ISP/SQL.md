# Widmowo-obronne Kury SQLowe 

## Gmeranie przy taśmach bibliotecznych

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

1. Policzenie scratchy w wszystkich bibliotekach:

	```sql
	select cast(library_name as char(15)) Libr, status, count(volume_name) as tape 
	from libvolumes 
	group by library_name, status
	```

	Wersja jednolinijkowa:
  
	```sql
	select cast(library_name as char(15)) Libr, status, count(volume_name) as tape from libvolumes group by library_name, status
	```
   

1. Scieżki OFFLINE (trochę ładniej niż `q path`:

	```sql
	select cast(SOURCE_NAME as char(15)) src, -
	 cast(DESTINATION_NAME as char(15)) dst, - 
	 cast(p.LIBRARY_NAME as char(15)) libr, - 
	 cast(DEVICE as char(20)) as dev, - 
	 cast(drive_serial as char(15)) as serial, -
	 WWN -
	from paths p, drives d -
	where p.online <> 'YES' and d.drive_name = p.destination_name
	```

	Definicja skryptu w SP:

	```
	def scr offline_paths "select cast(SOURCE_NAME as char(15)) src, cast(DESTINATION_NAME as char(15)) dst, cast(p.LIBRARY_NAME as char(15)) libr, cast(DEVICE as char(20)) as dev,  cast(drive_serial as char(15)) as serial, WWN from paths p, drives d where p.online <> 'YES' and d.drive_name = p.destination_name" -
		desc="Lista sciezek OFFLINE"
	```

1. **Nieaktualne. Lepiej użyć `perform libaction`**Generator makra masowego podnoszenia ścieżek:

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

1. Taśmy o ostatnim odczycie starszym niż 90 dni:

	```sql
	select VOLUME_NAME, LAST_WRITE_DATE 
	from volumes 
	where days(current date) - days(LAST_READ_DATE) > 90 
	order by LAST_WRITE_DATE
	```

## Klasy urządzeń

1. DevClass (raczej sekwencyjne)

	```sql
	select DEVCLASS_NAME,ACCESS_STRATEGY,DEVTYPE,FORMAT,CAPACITY /1024 as GIB, MOUNTLIMIT, DIRECTORY from devclasses
	```

## Pliki, filespace i zawartość wolumenów

1. Filespace na taśmie:

	```sql
	select distinct NODE_NAME NN,FILESPACE_NAME FN, volume_name VN  from contents where volume_name in ('180AABL5', '181AABL5')
	```

## Nody i filespace

1. Ogólny raport o klinetach. Wersje, IP, sortowany według ostatniego dostępu (najstarsi na górze):

	```sql
	select node_name,DOMAIN_NAME, 
	 CLIENT_VERSION || '.' || CLIENT_RELEASE || '.' || CLIENT_LEVEL || '.' || CLIENT_SUBLEVEL as ver,
	 APPLICATION_VERSION || '.' || APPLICATION_RELEASE || '.' || APPLICATION_LEVEL || '.' || APPLICATION_SUBLEVEL as app,
	 PLATFORM_NAME, 
	 CLIENT_OS_LEVEL,
	 TCP_NAME,TCP_ADDRESS, 
	 days(current date) - days(LASTACC_TIME) as LAST_ACC 
	from nodes 
	order by LAST_ACC desc, NODE_NAME asc
	```

	Do kopiowania:
  
	```sql
	select node_name,DOMAIN_NAME, CLIENT_VERSION || '.' || CLIENT_RELEASE || '.' || CLIENT_LEVEL || '.' || CLIENT_SUBLEVEL as ver,APPLICATION_VERSION || '.' || APPLICATION_RELEASE || '.' || APPLICATION_LEVEL || '.' || APPLICATION_SUBLEVEL as app ,PLATFORM_NAME, CLIENT_OS_LEVEL,TCP_NAME,TCP_ADDRESS, days(current date) - days(LASTACC_TIME) as LAST_ACC from nodes order by LAST_ACC desc, NODE_NAME asc
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

1. Filespacee z zakończonym backupem wcześniej niż 30 fdni temu:

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
	select cast(entity as char(20)) kto , sum(seconds_between(end_time, start_time))as sekundy, sum(bytes)/1024/1024 MiB 
	from summary 
	where activity='BACKUP' and  date(current date) = date(start_time)
	group by entity
	```

	Do kopiowania:

	```sql
	select cast(entity as char(20)) kto , sum(seconds_between(end_time, start_time))as sekundy, sum(bytes)/1024/1024 MiB from summary where activity='BACKUP' and  date(current date) = date(start_time)group by entity
	```

1. Ile MB zajmują nody, które nie kontaktowały się z serwerem dłużej niź 30 dni:

	```sql
	select a.node_name, sum(LOGICAL_MB) from occupancy a  where a.node_name in ( select node_name from  nodes where  (days(current date) - days(LASTACC_TIME))>30 ) group by a.node_name
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

	```sql
	select DOMAIN_NAME, CLASS_NAME, VEREXISTS, VERDELETED, RETEXTRA, RETONLY, DESTINATION from bu_copygroups  where set_name='ACTIVE'
	```

1. Polityki archiwizacji wraz z destination:

	```sql
	select DOMAIN_NAME,CLASS_NAME,RETVER,DESTINATION from ar_copygroups
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
