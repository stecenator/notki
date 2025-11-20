# Instalacja DB2 Community Edition

Instalka DB2 (LUW) jest w zasadzie jedna, pakowana na pierdylion sposobów. Ale liczy się tak naprawdę licencja, którą się jej wmuli. 

!!! Note "Instalacja w userspace"
	Instalator `db2_install` możńa puścić z konta, które ma być właścielem instancji. Wtedy taka instancja jest tworzona automatycznie oraz są instalowane wszystkie komponenty. **Nie polecam** tej metody. Na początek lepiej użyć `db2setup` puszczonego z roota, bo on wtedy o wszystko wypyta. Tylko trzeba mieć X11, co w nowoczesnych Linuxach może być kłpotliwe.

## Założenia

Wszystkie poniższe przykłady są zrobione na następującej konfiguracji:

- DB2 12.1.3 Community Edition. Można ją wziąć [stąd](https://www.ibm.com/products/db2/get-started).
- OS: Red Hat 9.7
- Platforma: PC-XT, ale może kiedyś sprawdzę to na PPC64LE
- Użyszkodnik instancji: `db2inst1`

## User instancji

Użyszkodnik instancji jest bogiem w zakresie baz tam zakładanych. A wszyscy członkiwie jego *primary grupy* są mu równi. Ja dodatkowo dokładam go do grupy `wheel`, bo zwykle tam mam skonfigurowane `sudo`. To nie jest konieczne, a pewnie z punktu widzenia bezpieki nawet niewskazane, ale to system testowy, a ja jestem leniem :smile:.

Zakładanie usera instancji (jako root):

```
useradd db2inst1 -c "Dibitu Juzer" -G wheel
passwd db2inst1
```

## OS pre-requisites

Jako obrazów podstawoawych używam profilu instalacji OSa:`Minimal server` co powoduje, że obraz co prawda jest niewielki, ale czesto, przy instalacji wyuzdanych programów  brakuje mu wymaganych paczek. Dla DB2 są to:

- pam.i686
- libstdc++.i686
- ksh

!!! Info inline end "Informacja:"
	Więcej na temat uruchamiania graficznych programów z hosta, który nie ma telewizora piszę [tutaj](/LNX/x11/).

Dla swojej wygody, żeby działało tunelowanie X11 po ssh i dało się uruchomić narzędzia graficzne np. instalator `db2setup`, dorzucam jeszcze:

- motif
- xorg-x11-xauth
- xterm


## Instalacja

Graficzna instalacja odbywa się przy pomocy instalatora `db2isetup`:

!!! Tip "Wskazówka:"
	Jeśli masz monitor o wysokiej rozdzielczości, np 142 DPI (4k 27"), ekran programu instalacyjnego może mieć bardzo małe czczionki. Ponieważ jest to aplikacja oparta o GTK3, honoruje ona zmienną `GDK_SCALE`, którą możńa ustawić na `2` co powiduje przeskalowanie okna o 100%. 


### Start instalatora

```shell
# export GDK_SCALE=2
# ./db2setup
```

W zależności od jakości łącza, pojawienie się ekranu powitalnego z licencją możę trochę potrwać. Zaakceptuj licencję.

### Tryb instalacji

Wybierz *Typical installation* i naciśnij *Next*:

![Typ instalacji](pix/db2setup1.png)

### Lokalizacja

Pozostaw domyślną lokalizację.

![Lokalizacja binariów](pix/db2setup1.png)

!!! Info
	W przypadku większości programów IBMa zmiana domyślnej lokalizacji binariów to głupi pomysł :smile:.

Klinkij *Next*.

### Użyszkodnik instancji

Wybierz, czy ma być tworzony nowy użytkownik instancji, czy użyć istniejącego.

![Nowy użytkownik instancji](pix/db2setup3.png)

Ja wcześniej stworzyłem usera `db2inst1`, więć po kliknięciu *Existing user* muszę wybrać *primary group* mojego użytkownika, a następnie samego usera.

![Istniejący użytkownik dla instancji](pix/db2setup4.png)

Kliknij *Next*.

### Fenced user

To chyba jest konta na któ©ym będą działać porcedury składowane bazy. Nie mam pojęcia co to jest, więc pozwalam mu założyć nowego usera. Podaj hasło i kliknij *Next*.

![Fenced user](pix/db2setup5.png)

### Przegląd ustawień i instalacja

To już wszystko. Przejrzyj ustawiania i kliknij *Next*.

![Przegląd](pix/db2setup6.png)

!!! Tip "Wskazówka:"
	Warto zapamiętać plik *response file*. Może przydać się do instalacji przez Ansible.
### Po instalacji

Po zakńczonej instalacji warto sprawdzić *Post-install steps*.

![Finish](pix/db2setup7.png)

W ramach kroków poinstalacyjnych IBM będzie namawiał do uruchomienia walidatora instalacji oraz zajrzenia do *First steps* w dokumentacji. Oraz straszył licencjami.

Kliknij *Finish*.

### Weryfikacja instalacji

Z ciekaowści można puścić weryfikację instalacji:

```shell
db2val
```

Przykładowy wynik:

```shell
[root@dibitu server_dec]# /opt/ibm/db2/V12.1/bin/db2val
DBI1379I  The db2val command is running. This can take several minutes.

DBI1335I  Installation file validation for the DB2 copy installed at
      /opt/ibm/db2/V12.1 was successful.

DBI1343I  The db2val command completed successfully. For details, see
      the log file /tmp/db2val-251120_155431.log.
```

I zawartość loga:

```
Installation file validation for the DB2 copy installed at "/opt/ibm/db2/V12.1" starts.

Task 1: Validating Installation file sets.
Status 1 : Success 

Task 2: Validating embedded runtime path for DB2 executables and libraries.
Status 2 : Success 

Task 3: Validating the accessibility to the installation path.
Status 3 : Success 

Task 4: Validating the accessibility to the /etc/services file.
Status 4 : Success 

DBI1335I  Installation file validation for the DB2 copy installed at
      /opt/ibm/db2/V12.1 was successful.

Installation file validation for the DB2 copy installed at "/opt/ibm/db2/V12.1" ends.

DBI1343I  The db2val command completed successfully. For details, see
      the log file /tmp/db2val-251120_155431.log.

```