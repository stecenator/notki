---
icon: material/tape-drive
---

# Spis mądrości Widmowo Obronych

* [Kury SQLowe](SQL.md) - rożne przydatne zapytania SQLowe.
* [Setup serwera SP na Linuxie](setup/index.md) - Przygtowanie hosta, instalacja binariów i setup instancji metodą "na piechotę".
* [Przydatne makra](macros/README.md) - głównie do rożnych statystyk 
* [Konfiguracja TDP4VE](clients/TDP4VE.md) - konfiguracja klienta Spectrum Protect for Virtual Environments.
* [Opcje](srv_opts.md), które warto sobie ustawić.
* [Disaster recovery](dr/index.md) - szeroko pojęte kwestie związane z odtwarzaniem bazy.


## Tips & tricks

Rzeczy które nie dorobiły się oddzielnego rozdziału.

### Kopiowanie polityk pomiędzy serwerami

Najprościej, mając zapiętą komunikację:

```
export policy * toserver=tsm-a preview=yes
```

To nie kopiuje definicji nodów, dlatego warto to zrobć tak:

```
export node dom=<domena>
```

Oczywiście istnieje mnustwo opcji eksportu od pojedynczych nodów po nody z domeny jak na :arrow_up: przykładzie.
