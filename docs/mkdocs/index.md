# mkdocs - brudnopis i co fajniejsze tricki

Wiem, że trochę przepisuję to co jest [tutaj](https://squidfunk.github.io/mkdocs-material/reference/), ale niektóre rzeczy są tam opisane dość skąpo.

## Adminitions

### Ogólne

Czyli ramki w tekscie. Przydatne do rożnych uwag. Np taki fragment kodu:

```
!!! Note "Uwaga:"
    *Adminitions* działają, gdy Twój edytor używa TABów do wcięć, ale będa się pierdolić, gdy spróbujesz użyć kilku akapitów albo wstawić np fragment kodu czy listę.
```

Zadziała tak:

!!! Danger "Uwaga:"
    *Adminitions* działają, gdy Twój edytor używa TABów do wcięć, ale będa się pierdolić, gdy spróbujesz użyć kilku akapitów albo wstawić np fragment kodu czy listę, dlatego lepiej przestawić edytor na wstawianie **4 spacji** zamiast tabulatora.
 
### Rozwijana ramka z kodem i listą

Odrobina perwersji:

??? Example "Przykład"
    Żeby zrobić rozwijaną ramkę z fragmentem kodu i listą, np w C trzeba napisać:

    ```
    ??? Example "Przykład"
        Żeby zrobić rozwijaną ramkę z fragmentem kodu i listą, np w C trzeba napisać:
        ```C
        #include stdio.h;
        int maint()
        {
            printf("Hello world.\n");
            return(0);
        }
        ```

        A potem można dodać listę rozszerzeń do włączenia, żeby to zadziałało:

        - admonition                # Ramki z Uwagami
        - pymdownx.details
        - pymdownx.superfences
    ```

    Wpomniany kawałek kodu, żęby się ładnie świecił:
    ```C
    #include stdio.h;
    int maint()
    {
        printf("Hello world.\n");
        return(0);
    }
    ```

    A potem można dodać listę rozszerzeń do włączenia, żeby to zadziałało:

    - admonition                # Ramki z Uwagami
    - pymdownx.details
    - pymdownx.superfences

Rozwijane ramki robi się, używając `???` zamiast `!!!`.

## Zakładki

Czasem jak coś jest do zrobienia na klika sposobów, warto te sposoby umieścić na zakładkach:

=== "Po pierwsze"

    Sposób pierwszy

=== "Po drugie"

    Tu można umieścić rożne rzeczy, np listę:

    - jeden
    - dwa

=== "Po trzecie"

    Można też wrzuć kwałek kodu:

    ```shell
    $ echo Hellow world
    ```

Kod tej ramki wygląda tak:

```
    == "Po pierwsze"

        Sposób pierwszy

    === "Po drugie"

        Tu można umieścić rożne rzeczy, np listę:

        - jeden
        - dwa

    === "Po trzecie"

        Można też wrzuć kwałek kodu:

        ```shell
        $ echo Hellow world
        ```
```

## Adnotacje (Annotations)

Adnotacje są trochę dziwne. Nie zawsze działają i działają inaczej w blokach kodu a inaczej w gołym tekście. 

Generalnie polega to na umieszczeniu `(1)`, `(2)` itd gdzieś w tekscie. A potem pod blokiem tekstu daje się znacznik `{ .annotate }` a po nim w kolejnym akapicie numerowaną listę z opisami poszczególnych anotacji.

W bloku kodu trzeba je umieszczać w komentarzach języka, więc jak `pygments` go nie obsluguje to nie ma.

=== "Adnotacje w zwykłm tekscie"

    Taki kawałek tekstu:

    ```
    Zwykły tekst z (1) adnotacją. I z drugą (2)
    { .annotate }

    1.  Hej, to jest adnotacja :smile:
    2.  A to druga.
    ```

    Będzie wyglądać tak:

    Zwykły tekst z (1) adnotacją. I z drugą (2)
    { .annotate }

    1.  Hej, to jest adnotacja :smile:
    2.  A to druga.

=== "Adnotacje w kodzie"

    Adnotacje w kodzie działają inaczej, bo trzeba je umieszczać w komentarzach kodu co ma swoje ograniczenia. Przykładowo:

    ```
        ```shell
        echo To jest test # (1)
        ```

        1.  Adnotacja kodu w shellu
    ```

    Będzie wyglądać tak:

    ```shell
    echo To jest test # (1)
    ```

    1.  Adnotacja kodu w shellu
