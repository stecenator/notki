---
icon: octicons/note-24
---

# Brudnopis

Tu są zapytania, które storzyłem na jakies partykularne potrzeby i może kiedyś przerobię na coś bardziej uniwersalnego. nie bawiłem się tu w ładne formatowanie SQL.

## Biblioteki i woluminy

### Puste wolumeny pulowe w bibliotece:

=== "Skrypt `q_empty`"

    ```
    --8<-- "scripts/isp-sql/q_empty.dsm"
    ```

!!! Warning
    To jest do poprawienia, bo zawiera zafixowane nazwy!


### Generator komendy `del vol` dla pustych taśm w puli:

```sql
select 'del vol ' as qra, -
	cast(volume_name as char(8)) VN, -
	' w=y' WAIT -
from volumes -
where volume_name  in ( select volume_name from libvolumes where library_name='TS4500KON' and volume_name like '%L5' and status='Private') and status='EMPTY' and stgpool_name='ORACLECOPY'
```

### Filespace na taśmie:

```sql
select distinct NODE_NAME NN,FILESPACE_NAME FN, volume_name VN  from contents where volume_name in ('180AABL5', '181AABL5')
```


## Dirpools

### Generator `move container` dla kontenerów z zadaną ilością wolnego miejsca

```sql
SELECT 'move container '|| SUBSTR(CONTAINER_NAME,1,50) AS CONTAINER_NAME, - 
        'defrag=yes '|| CAST(FREE_SPACE_MB AS DECIMAL(8,0)) as "FREE_SPACE_MB", -
        SUBSTR(TOTAL_SPACE_MB,1,5) AS TOTAL_SPACE_MB -
    from containers -
    where FREE_SPACE_MB>10 and STATE='AVAILABLE' and CONTAINER_NAME not like '%N:\%' -
    order by FREE_SPACE_MB desc
``` 

## Polityki

!!! Note "Jest lepszy sposób"
	Jeśli serwery, pomiędzy którymi chcesz przenieść plityki, wystarczy użyć którejś z komend `export`, np `export policy`. 

### Kopiowanie polityk archiwalnych. 



Generuje `define copyg` z istniejących polityk:

```sql
select 'def copyg SAP ',SET_NAME,CLASS_NAME, 't=a', concat('retver=',RETVER), concat('dest=',DESTINATION) from ar_copygroups where domain_name='SAP' and set_name <> 'ACTIVE'
```

### Kopiowanie polityk backupowych.

Generuje `define copyg` z istniejących polityk backupu:

```sql
select 'def copyg ', -
	DOMAIN_NAME, -
	SET_NAME, -
	class_name, - 
	concat('vere=',VEREXISTS), -
	concat('verd=',VERDELETED), -
	concat('rete=',RETEXTRA), -
	concat('reto=',RETONLY), -
	concat('dest=',destination) - 
from bu_copygroups -
where SET_NAME <> 'ACTIVE'
```

Wersja do skopiowania do terminala **Uwaga podstaw ID i hasło:**

```shell
$ dsmadmc -se=mój-tsm -id=XXX -pa=XXX -dataonly=yes "select 'def copyg ',DOMAIN_NAME, SET_NAME, class_name, concat('vere=',VEREXISTS), concat('verd=',VERDELETED), concat('rete=',RETEXTRA), concat('reto=',RETONLY) ,concat('dest=',destination)  from bu_copygroups where SET_NAME <> 'ACTIVE' " | tr -s ' '
```
