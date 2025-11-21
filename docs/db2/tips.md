# Użyteczne komendy DB2

I inne sprawy, które nie dorobiły się oddzielnej kategorii

## Instancje

!!! Tip "Wskazówka:"
	Komend zarzadzających instancjami zwykle nie ma na scieżce `PATH`, dlatego trzeba je tam sobie dodać, albo wołać bezwględnie, np:

	```shell
	[db2inst1@dibitu ~]$ /opt/ibm/db2/V12.1/instance/db2ilist
	```


Instancja ma swojego użytkwnika - właściciela. Członkowie *primary group* użyszkodnika instancji mają takie same prawa jak właściciel. Generalnie, DB2 dość mocno bazuje na uprawnieniach wynikających z OS.


### Lista instancji

Listę instancji wyświetla komenda `db2ilist`. :

```shell
[db2inst1@dibitu ~]$ /opt/ibm/db2/V12.1/instance/db2ilist 
db2inst1
```

### Tworzenie instancji

!!! Note inline end "Uwaga:"
	Instancję tworzy się z poziomu `root` na wcześniej przygotowanym użytkowniku.

Instancję tworzy komenda:

```shell
db2icrt -a server db2inst1 db2inst1
```

Dokumentacja jest [tu](https://www.ibm.com/docs/en/db2/12.1.x?topic=unix-creating-instance-using-db2icrt).

### Usunięcie instancji

Usunięcie instancji odbywa się komendą `db2idrop nazwa_instancji`.