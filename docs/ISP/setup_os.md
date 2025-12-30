# Przygotowanie Linuxa pod pracę z IBM Spectrum Protect

Procedura instalacji ISP na hoscie linuxowym, mądrości zebrane i ciągle zbierane. MAm to ubrane w Ansibla. Opublikuję jak będzie moało ręce i nogi.

## Wymagania wstępne

Sprawdź [oficjalne wymagania](https://www.ibm.com/support/pages/overview-ibm-spectrum-protect-supported-operating-systems) na stronie IBM. 

Jeżeli plaujesz używać taśm IBM, to jedynymi praktycznymi dystrybucjami są SuSE i Red Hat. Wsparcie `lin_tape` na Ubuntu jest koszmarne. Tutaj skupiam się na Red Hat.

## SELinux

`Disabled` albo `Permissive`. Po utworzeniu insancji można właczyć na `Enforcing`.

## Pakiety

RHEL może być zainstalowany z profilu *Minimal Server*, ale będzie potrzebować jeszcze:

* `ksh`

Opcjonalne, ułatwiające życie:

* `motif` - daje `mwm`
* `xterm`
* `tigervnc-server` - choć w tej procedurze instaluję "na piechotę" ale jak by ktoś chciał tworzyć instancję przez przez `dsmicfgx`
* `tmux` - bo jest lepszy niż screen 
* `libnsl` - na RHEL8 może tego nie byc w minimalnej instalacji.

Jesli maszyna ma chodzić z taśmami IBM to:

* `kernel-devel` - wciągnie masę przyległości, w tym `gcc`.
* `rpm-build`

## Multipath

W przypadku uzycia SVC, albo FlashSystem warto storzyć `multipath.conf` zawierający poniższe ustawienia:

```
defaults {
    find_multipaths yes
    user_friendly_names yes
    polling_interval    30
}
devices {
    device {
        vendor "IBM"
        product "2145"
        path_grouping_policy "group_by_prio"
        path_selector "service-time 0" 
        prio "alua"
        path_checker "tur"
        failback "immediate"
        no_path_retry 5 # or no_path_retry "fail"
        retain_attached_hw_handler "yes"
        fast_io_fail_tmo 5
        rr_min_io 1000
        rr_min_io_rq 1
        rr_weight "uniform"
    }
}

blacklist {
}
```

!!! note "Uwaga"
    W firmłerach 8.5 i wyższych, IBM nie wymaga modyfikacji `multipath.conf`. Ja ją jednak stosuję zwłaszcza ze względu na `friendly_names`. 

## Regułki `udev` dla dysków (IBM)

Utworzyć plik `/etc/udev/rules.d/99-ibm-2145.rules` z taką treścią:

```
SUBSYSTEM=="block", ACTION=="add", ENV{ID_VENDOR}=="IBM",ENV{ID_MODEL}=="2145", RUN+="/bin/sh -c 'echo 120 >/sys/block/%k/device/timeout'"
```

!!! note "Uwaga"
    W firmłerach 8.5 i wyższych, IBM nie wymaga wydlużania timeoutów na ścieżkach. 

## Ustawienia FC dla taśm

Coś o `r-port`.

## Parametry dla DB2

## Instancja

[Ważne do obczjenia](https://www.ibm.com/support/knowledgecenter/SSEQVQ_8.1.10/srv.install/t_srv_config_dbopts-linux.html)

# AIX

Parę rzeczy w AIXie wyjętym z pudełka trzeba zmienić:

## `ulimit` dla usera instancji

!!! Info inline end "Informacja"
    To ma tendencę do zmieniania się z wersji na wersję. Szczegółowe informacje o ulimitach i nie tylko są [tutaj](https://www.ibm.com/docs/en/storage-protect/8.2.0?topic=isos-installing-aix-systems)

Do `/etc/security/limits` w sekcji `default` albo dla `spinst1` wpisać:

```
nofiles = 65536
nproc = 8192
fsize = -1
```

## Parametry FC i fscsi 

Dla taśm, AIX wymaga innych ustawiań niż dla dysków, dlatego trzeba dać dedykowane kontrolery (v)fc:



