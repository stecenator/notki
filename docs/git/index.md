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
