---
icon: fontawesome/solid/explosion
---

# Disaster recovery

## Odtwarznie bazy

## Odtwarzanie bazy do punktu w czasie

## Odtwarzanie bazy bez `volhist` 

Siłą rzeczy też do punktu w czasie. Podstawą tej proceury jest [ten dokument](https://www.ibm.com/support/pages/rebuild-missing-volume-history-file-file-database-restore).


Dlaczego w ogóle może zejść potrzeba takiego odtwarzania? Ano przydarzyło mi się, że przez nieuwagę usunąłem sobie katalog instancji _Protecta_ przy próbie reinstalacji OSa. Myślałem, że wzystko jest w oddzielnych volume grupach, i że po ponownym zainstalowaniu OSa zrobię [ponowny import instancji](#import-istniejacej-instancji), z grupy `spvg` ale nie zauważyłem, że katalog instancji nie jest filesystemem tylko katalogiem w `/` fiesystemu :facepalm:.

### Stan początkowy

Mam właściwie wszystkie filesystemy i pewnie gdybym pamiętał jak były pomontowane i miał katalog instancji (`DFTDBPATH`) to mógłbym go skatalogować i po prostu działać. Ale nie mam :shrug:. Mam za to taką strukturę filesystemów/katalogów:

``` title="Struktura montowania /sp"
/sp/
├── actlog
├── archlog
├── db01
├── db02
├── db03
├── db04
├── dbb
│   └── upd
├── dp01
│   ├── 00
│   ├── 01
│   ├── 02
│   └── 03
└── spinst1
```

Tak jak wspomniałem, nie mam pomysłu jak dobrać się do bazy rozłożonej w tatalogach `/sp/db*` więc sformatowałem te filesytemy (i przy okazji zmieniłem ext4 na XFS). Podobonie z `/sp/a*log`. Zatem jedyna  pozostałość "starego" TSMa jaką mam, to backup bazy w `/sp/dbb` i pamięc, że _devclass_ nazywała się `DBB`. Resztę muszę zrobić od nowa.

### Nowa instancja

Żeby odtwozyć bazę, potrzebna jest nowa instancja. Można ją zrobić tekstowo, pry pomocy [tej procedury](../setup/setup_instance.md), albo pójś na łatwiznę i jesli masz X11, to odpalić :material-wizard-hat: wizarda `/opt/tivoli/tsm/server/bin/dsmicfgx` jako `root`.



## Import istniejącej instancji 


