# Konfiguracja DB2 jako klienta IBM Storage Protect

Wsparcie dla DB2 jest na poziomie API klienta BA - wystarczy mieć to skonfigurowane i gitara. Ale diabeł oczywiście tkwi w sczegółach, zatem... szczegóły poniżej.

## Serwer ISP

Serwer nie zajmuje się retencją backupów w imieniu DB2. Za to jest odpowiedzialna sama baza. Daltego wystarczy założyć prostą politykę:

- `VERE` = 1 
- `VERD` = 0
- `RETE` = 0
- `RETO` = 0

### Domena, policy set, managment classa i copy grupa

Zakładam, że jest już pula `dc01`, która u mnie zwykle jest kontenerowa. Oczywioście można tu użyć dowolnej puli, jak komu pasuje. Przy LAMFRee to będzie pewnie taśma, albo `FILE` na jakimś GPFSie.

```
reg dom db2 descr="Klienci db2"
def pol db2 prd desc="Polityka dla DB2"
def mgmt db2 prd dbb migdest=dc01
def copyg db2 prd dbb t=b vere=1 verd=0 rete=0 reto=0 dest=dc01
def copyg db2 prd dbb t=b vere=1 verd=0 rete=0 reto=0 dest=dc01
assign defmgmt db2 prd dbb
val pol db2 prd
act pol db2 prd
```

!!! note "Uwaga:"
	W powyższej liście komend jest kilka "zbędnych rzeczy": `migdest=dc01`  i copygrupa archiwalna są dla porządku, bo nie lubię mić ostrzeżeń podczas validacji policysetu. 

### Klient

Klientów będzie tak naprawdę dwóch: dla bazy (API) i dla OSa (BA).

Założenia:

- Hostname i nodename klienta db2: `dibitu`
- Nodename dla klienta API: `dibitu_db2`
- klientów API rejestruję w odpowiednich dla nich domenach.
- Klientów OS rejestruję w domenie np `OS` albo jak w poniżej w `LNX` jeśli akurat lubię mieć OSy porozdzielane. 


#### Klient dla bazy

Klient dla bazy będzie służył wyłącznie do połączeń API wykonych przez silnik bazy danych.

!!! Note "Uwaga:"
	Ważne jest, żeby klient miał prawo kasowania swoich backupów. W przeciwnym wypadku one nigdy nie wygasną! 

```
reg node dibitu_db2 tajne_hasło dom=DB2 backdel=yes
```

#### Klient dla OS i harmonogramów


Na tym kliencie będzie robiony backup plików z tego hosta, oraz będzie on słuchał harmonogramów, które np będą wywoływać skrypty backupujące bazę. 

```
reg node dibitu tajne_hasło dom=LNX
```