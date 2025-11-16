# Konwencje

Rożne konwencje i standardy któ©e sobie wymyśliłem w trakcie moich rozlicznych wdrożeń.

## Struktura katalogów

## Użyszkodnik instancji

## Domeny i nodename
### Oracle
Standaryzacja konfiguracji TSM dla srodowisk baz danych Oracle

## Nazewnictwo hostów w klastrze Power HA



| Wzorzec         | Przykład          | Uwagi      |
| --------------- | ----------------- | ---------- |
| NAME**a**       | elixir**a**       | hostname 1 |
| NAME**b**       | elixir**b**       | hostname 2 |
| NAME**service** | elixir**service** | service IP |

```
[root@elixirb:tsm]# for i in a b service; do host  elixir$i;done
elixira is 10.200.0.204
elixirb is 10.200.0.205
elixirservice is 10.200.0.206
```



## TSM nodes

| Wzorzec         | Przykład          | Uwagi                                                        |
| --------------- | ----------------- | ------------------------------------------------------------ |
| NAME**a**       | elixir**a**       | FS backup, dsmcad na domyslnym dsm.opt                       |
| NAME**b**       | elixir**b**       | FS backup, dsmcad na domyslnym dsm.opt                       |
| NAME**service** | elixir**service** | DB bakup, /usr/bin/dsmcad -optfile=/local/data/tsm/dsm.opt<br />klastrowy agent  np: uruchamiany, tu są podpięte harmonogramy |
| NAME**-ora**    | elixir**-ora**    | DB backup chroniona aplikacja - odpowiedzialna za oracle'a . Command backup uruchamiany przez NAME**service** |

```
tsm: TSM>q node elixir*

Node Name                     Platform     Policy Domain  
-------------------------     --------     -------------- 
ELIXIR-ORA                    TDP Orac     ORACLE                                                  
ELIXIRA                       AIX          AIX            
ELIXIRB                       AIX          AIX            
ELIXIRSERVICE                 AIX          AIX            
```







1. Pliki konfiguracyjne

1. RMAN konfiguracja
2. RMAN catalog scripts
3. Backup scripts
4. TSM Nodes
5. TSM Schedulers and Associations
6. Monitoring
7. Przydatne polecenia

