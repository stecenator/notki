---
icon: octicons/container-24
---

# Pule kontenerowe

Jak z nimi żyć? 

Pojawiły się wraz z 7.1.3, czyli są już na rynku od 2017 roku, a nadal dostarczają sporo radośći. Ty jest zbiór moich doświaczeń z pulami kontenerowymi. 

## Zasady użycia

- [x] Pule konetenerowe nie nadają się do składowania danych zaszyfrowanych przezd zapisem (np szyfrowanych RMANem)
- [x] Dane wcześniej skompresowane też nie bardzo nadają się do składowania w kontenerach, choć dają się _deduplikować_. 
- [x] Migracja pomiędzy pulami zwykłymi i kontenerowymi jest [nietrywialna](#migracja-i-kopiowanie-pomiedzy-pulami).
- [x] Disaster recovery lepiej oprzeć na replikacji
- [x] [Utrzymanie](#utrzymanie) puli kontnerowej oznacza replkację, backup i regularne [audyty](#audyt).

## Utrzymanie

### Audyt

Audyt trzeba robić przy pomocy regułki, zdefiniowanej tak:

``` title="Definicja reguły audytowej"
def stgrule dp01chk dp01 action=audit ative=yes 
```

Po audycie mogą zostać znalezione uszkodzone extenty. jeśli nie ma repliki to trzeba je usunąć.

1. Wygeneruj listę uszkodzonych kontenerów:

    ```
    q damaged dp01 type=container
    ```

1. Wygrneruj listę nodów, których dotyczą uszkodzenia:

    ```
    q damaged dp01 type=node
    ```

1. Opcjonalnie, jeśli masz __dużo czasu__, zrób listę uszkodzonych plików:

    ```
    q damaged dp01 type=inventory
    ```

1. Usuń uszkodzone extenty. Dla każdego kontenera z listy uszkodzonych, wykonaj:

    ```
    audit container /scieżka/do/kontenera action=removedamaged
    ```


    !!! Danger 

        To powoduje __usuwanie__ obiektów, które odwolują się do uszkodzonych nodów.


    !!! Node "Ciekawostka"

        W sytuacji, gdzie kontenery nawet po `removedamaged` są uszkodzone, komenda `q damaged type=node` nie zwraca żadnych wyników, po prostu idź na kawę. TSM/Protect potrzebuję po prostu około 2h (może mniej, ale akurat tyle mnie nie było)




## Migracja i kopiowanie pomiędzy pulami