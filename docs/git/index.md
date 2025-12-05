---
icon: material/git
---

# Mądrości-gitości

## Konfiguracja

Leży w `.git/config` i jest automatycznie ustawiane po skolnowaniu zdalengo repo:

```ini
[core]
    repositoryformatversion = 0
    filemode = true
    bare = false
    logallrefupdates = true
[remote "origin"]
    url = git@github.com:stecenator/chrum-chrum.git
    fetch = +refs/heads/*:refs/remotes/origin/*
[branch "main"]
    remote = origin
    merge = refs/heads/main
```


## Branch

Wszelkie aspekty pracy z branchami. 

### Branching strategy

Warto rozważyć posiadanie kilku gałęzi, np:

- **main** - to działa produkcyjnie
- **devel** - tu wpadają pull-requesty z gałęzi poszczególnych releasów
- **feature/nazwa_ficzura** - implementacja nowych funkcji
- **bug/nr_buga** - praca nad problemem.

### Dobre praktyki

Czyli jak zabezpieczyć się przed głupimi błędami.

#### Kontrolny pull

Kontrolny `git pull` przed rozpoczęciem pracy, możę zaoszczędzić sporo roboty przy mergowaniu.

#### Sprawdź branch przed commitem

Ja używam `zsh` z pierdylionem pluginów więc widzę to w prompcie, ale zawsze można sprawdzić gdzie jestem komendą `git branch`:

```shell
$ git branch
* feature/users
  main
(END)
```

### Tworzenie branch'y

Branch można tworzyć wraz z "taskiem", który może przyjść z proejktu np z Jiry.
Fajnie jest nawać zgodnie z jakąś nomentklaturą projektową, np `feature/nazwa_ficzura`.

Komenda:

```
git checkout -b "feature/users"
```

Przykład:

```shell
$ git checkout -b "feature/users"
Przełączono na nową gałąź „feature/users”
```

### Sklejanie  branch'y (merge)

Chyba można zrobić to na dwa sposoby. Przez *pull request* albo lokalnie i wypchnąć. 

#### Merge lokalny

Da się zrobić, gdy jestem praktycznie sam w repo i nikt mi z boku nie prosi o merge gałęzi, bo wszystki ficzury i tak developuję sam. 

#### Sprawdź status

W razie czego zrób ostatni *commit* w gałęzi:

```shell title="Status gałęzi"
~/Dokumenty/IBM/dox/notki mkdocs ⇡ ❯ git status
Na gałęzi mkdocs
Twoja gałąź jest do przodu względem „origin/mkdocs” o 2 zapisy.
  (użyj „git push”, aby opublikować swoje zapisy)
```

### Pull-request

Czasem przyjdą zmiany z boku. Wtedy trzeba dołączyć zmiany z jednej gałęzi do drugiej. Tak się dziej np gdy zostanie naprawiony jakiś bug. Albo dodany ficzur. C

1. Wypchnij zmiany z bocznej gałęzi do nowego repo. W razie potrzeby utwórz tę gałąź w `ORIGIN`.
1. Zaloguj sie na GithHub i zrób pull-request.


## Tricki

Wypadki się zdarzają.

### Powrót do wersji pliku ze wskazengo commitu

Zdarzyło mi się, że tak napsułem jeden plik, że wolałem się cofnąć do konkretnej wersji.

1. Przejrzyj log commitów:

    === "Log commitów"

        Tak zobaczysh SHA commitów i autorów: 

        ```sh
        git log ścieżka/do/pliku
        ```

    === "Log commitów ze zmianami"

        Czasem łatwiej rozpoznać wersję po treści. przełącznik `-p` możę pomóc:

        ```sh
        git log -p ścieżka/do/pliku
        ```

    !!! Example "Przykład:"

        Tu jest wywołanie bez `-p`:

        ```sh
        $ git restore log -p docs/git/index.md

        commit c87ef3893628614b5a6569138f0fd89eaf700bfd
        Author: Marcin Steć <coyote@acme.com>
        Date:   Tue Nov 25 20:42:21 2025 +0100

            Dodane ikony do wszystkich głóœnych sekcji. Kilka custom ikon też

        commit 6982fe6149e434339fd15d7750c191e8e7483fc2
        Author: Marcin Steć <coyote@acme.com>
        Date:   Tue Nov 25 12:22:50 2025 +0100

            Nie trzyma się otwartego edytora przy merdżowaniu gałęzi gita

        commit 3c2971993aa61e5d671274aaefaf3d0b0f793394 (origin/mkdocs, mkdocs)
        Author: Marcin Steć <coyote@acme.com>
        Date:   Tue Nov 25 11:19:32 2025 +0100

            Baron Munchaussen

        commit ae20ebd4e3c4eca2ee445d89a517be4c6aac503a
        Author: Marcin Steć <coyote@acme.com>
        Date:   Tue Nov 25 11:13:05 2025 +0100

            Koniec porządków w kodzie po przejściu na strukturę dla mkdocs

        commit ff00bbdca0d9d97bbf61b1d64f64199d6d108f3a
        Author: Marcin Steć <coyote@acme.com>
        Date:   Sat Nov 15 23:43:22 2025 +0100

            porządki w strukturze mkdocs

        commit f424fac8e64209308ae926118551c672a09d0c00
        Author: Marcin Steć <coyote@acme.com>
        Date:   Mon Nov 10 20:38:10 2025 +0100

            Porządki w spójności linków po przestawianie się na hierarchię mkdocs

        commit ab3b26dd444ae3bd41ae823016860d6afade3b58
        Author: Marcin Steć <coyote@acme.com>
        Date:   Thu Oct 30 23:56:41 2025 +0100

            rozkurwione linki
        ```

1. Odkręć plik do wybranogo commitu używając hasha SHA:

    ```sh title="Odkręcanie pliku do wskazanego commitu"
    git restore --source=3c2971993aa61e5d671274aaefaf3d0b0f793394 docs/git/index.md
    ```

    ??? Example "Przykład:"

    ```sh
    $ git restore --source=3c2971993aa61e5d671274aaefaf3d0b0f793394 docs/git/index.md
    ```
