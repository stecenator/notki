# Ulubione makra

Do zbierania danych z TSM/Protect potrzebne są dwa makra.

## `def-stats.mac` - przydatne skrypty

Definicja skryptów zbierających przydatne informacje (opisanych w notce [SQL](../SQL.md))

- `node_stats` - trupy w szafie
- `stg_stats` - ogólna kondycja pul
- `tape_stats` - stan taśm w bibliotekach
- `vol_stats` - stan woluminów w pulach
- `dom_auditocc` - suma audito grupowana po domenach

Przed zbieraniem danych trzeba puścić makro definujące te skrypty:

```shell
$ dsmadmc -id=mój_admin -pa=tajne_hasło -itemcommit macro def-stats.mac
```

## `isp_info.mac` - raport o stanie instancji TSM/Protect

Korzysta ze skryptów definiowanych wyżej, puszczać tak:

```shell
dsmadmc -id=mój_admin -pa=tajne_hasło -itemcommit -outfile=raport.txt macro isp_info.mac
```

**Uwaga:** parametr `-outfile=raport.txt` jest lepszy niż przekierowanie wyjścia `> raport.txt` bo komendy typu `q status` są sformatowane jak na konsoli, a nie w linijkowo.