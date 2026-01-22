---
icon: material/gauge
---

# :fontawesome-solid-gears: Opcje serwera

Opcje serwera, które najczęściej zmieniam. 

!!! Note "Informacja"
    Być może kiedyś zrobię z tego makro, albo jeszcze lepiej, szablon makra do :simple-ansible:.

| Opcja                   | Default | Moja  | Opis  |
| :---                    | :---    | :---  | :---  |
| `PWREUSELIMIT`          | 12      | 1     | Bo lubię na moich TSMach. Zwykle tego nie dotykam u klientu, bo to uwarunkowania bezpieki :shrug: |
| `MINPWLEN`              | 15      | 8     | OldSQL :stuck_out_tongue_winking_eye: |
| `PASSEXP`               | 90      | 0     | Tego nie da się zrobić globalnie. trzeba dodać `admin=cinek` |
| `PreallocReductionRate` | 1       | 2+    | Tricky. Ppreczytaj [rozdział o `PreallocReductionRate`](#preallocreductionrate). |


## PreallocReductionRate

!!! Note inline
    Teoretycznie, [problem](https://www.ibm.com/support/pages/apar/IT45823), który opisuję poniżej został rozwiązany w 8.1.23, ale obserwuję go na przypadku gdy *źródłem* jest 8.1.15 a *celem* jest 8.1.27.1. Zobaczymy co się stanie po aktualizacji *źródła*. 

To jest trochę ból w dudzie. Bo domyślnie jest 1, co oznacza, że np. podczas replikacji, gdzie źródłowy i docelowy serwer mają malutkie, 2TiBowe pule kontenerowe, a źródłowy obiekt jest np 10TiB'owy, to *target* będzie próbował zaalokować w docelowej puli 10 TiB, bo domyśłnie `PreallocReductionRate` wynosi `1` :man_facepalming:.

Dlatego jeśli stawiasz *target*, to zerknij jakie są uzyski na puli *source* i ustaw to porządnie. W moim przypadku, *źródło* podazało na puli redukcję rzędu 98%, czyli jakieś 50:1. niestety `PreallocReductionRate` maksymalnie może przyjąć wartość 25 czyli 25:1. [Tutaj dokumentacja](https://www.ibm.com/docs/en/storage-protect/8.1.25?topic=options-preallocreductionrate).

