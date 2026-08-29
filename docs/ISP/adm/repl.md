---
icon: material/content-duplicate
---

# Replikacja

Replikacja jest najlepszą metodą na zabezpieczenie puli kontenerowej. Właściwie to jedyną, bo metoda na `protect stgpool` & `replicate node` jest już _passe_, `protect stgpool` do lokalnej puli typu `container-copy` nigdy nie działał wydajnie, a reguła typu `copy` do standardowej _copy puli_  działa tylko w jedną stronę:dane są zabezpieczone, ale nie da się z nich odpudować zniszczonej puli kontenerowej (1).
{ .annotate }

1. Przynajmniej w lipcu 2026. Kto wie co przyniesie przyszłość :shrug: ?

!!! Note inline

    Jeżeli masz serwery w rożnych wersjach, to trzymaj się zasady, że __target musi być w wyższej wersji__ niż źródło. Ta [tabela](https://www.ibm.com/support/pages/replication-compatibility-ibm%C2%AE-storage-protect-servers)

Replikacja przy pomocy reguł pojawiła się gdzieś w okolicy 8.1.13, ale dojrzałości można mówić jakoś tak w kolicy 8.1.22. Nie mniej jednak warto jej używać,
bo:

- [x] Reguły mogą działać w trybie _opt-in_ i _opt-out_.
- [x] Kontrola co wchodzi, a co nie jest na pziomie _filespace_.
- [x] Reguły mogą mieć wyjątki przy pomocy _subrules_.
- [x] Reguły, gdy są `active=yes` będa startować automatycznie, według własnego, niestety bardzo prostegu harmonogramu.
- [x] Nieaktywne reguły można startować komendą `start stgrule`, np. w sktypcie [maint](../setup/maint.md).
- [x] `start stgrule` pozwala dodawać rożne parametry, z których najużyteczniejszy jest `focereconcile=` :wink:.

## Tworzenie reguł replikacyjnych

Warunki konieczne:

- [x] Dwa [^1] serwery, które ze sobą gadają. Mogą być skonfigirowane [tym sposobem]().
- [x] Definicje polityk i nodów takie same na obu serwerach. [^2]
- [x] Nody podlegające replikacji muszą być odpowiednio oznaczone przy pomocy atrybutów `replstate` i `replmode`.

[^1]: Według dokumentacji max 3 dla jednego zestawu danych. To się da obejść, ale nie polecam.
[^2] Nie koniecznie, przy włączeniu różnych polityk, ale zarządzanie jest upierdliwe.

### Definicja reguły replikacyjnej

Co mam:

- Zdefiniowaną komunikację:
    - Serwer źródłowy: `TSM`
    - Serwer docelowy: `TSM-A`
- Oba mają zsychronizowane węzły i polityki. Np [tym](../README.md#kopiowanie-polityk-pomiedzy-serwerami) trickiem.
- Oba mają pulę kontenerową [`dp01`](../setup/setup_dc.md). 

=== "Opt-Out"
    Ta reguła próbuje zreplikować wszystko co jest zazanczaone do replikacji

    ``` title="Definicja reguły replikacyjnej"
    define stgrule repl2drc 
    ```

    !!! Bug
        Dokończyć

=== "Opt-In"
    Ta reguła olewa wszystko co jest zazanczone do replikacji i czeka na wyjątek.

    ``` title="Definicja reguły replikacyjnej"
    define stgrule repl2drc 
    ```

    !!! Bug
        Dokończyć


## Komendy związane z replikacją

### Start, stop, monitoring

### Najczęstsze problemy 