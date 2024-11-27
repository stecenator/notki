# Konwersja `lsvdisk` na `user_friendly_names` w LNX

1. Zbackupuj sobie plik `/etc/multipath.conf`.
1. Upewnij się, że plik `/etc/multipath.conf` zaczyna się mniej więcej tak:

    ```
    defaults {
    	polling_interval 	30
    	user_friendly_names	yes
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
    multipaths {
    ```
    Prawdopodobnie nie masz sekcji `multipaths { ... }`. Jeśli nie to dopisz ją na końcu tak jak na powyższym przykładzie. Na razie nie zamykaj jej `}`.

1. Zapisz gdzieś, gdzie masz `sed'a` output z macierzowego polecenia `lsvdisk`.

    ```
    ssh superuser@fs-sds01.p4 'lsvdisk -delim :' > lsvdisk.csv
    ```
	... i usuń z pliku `lsvdisk.csv` pierwszą linijkę (tę z naglówkiem).

1.  Zmień plik `sed'em` i `tr'em`:

    ```bash
    cat lsvdisk.csv | cut -f 2,14 -d ':' | sed 's/\(.*\):\(.*\)/\tmultipath {\n\t\twwid\t\t"3\2"\n\t\talias\t"\1"\n\t}/' | tr '[:upper:]' '[:lower:]' > multipaths.txt
    ```

1. Jeśli źródło wygląda tak:

    ```
    cat lsvdisk.csv

    0:sp-db00:0:io_grp0:online:0:Pool0:32.00GB:striped:::::60050768108101FB4000000000000002:0:1:not_empty:0:no:0:0:Pool0:::no:no:0:sp-db00::scsi

    [...]
    ```

    to output powinien wyglądać tak:

    ```
     cat multipaths.txt
        
        multipath {
            wwid:       "360050768108101fb4000000000000002"
            alias   "sp-db00"
        }

    [...]
    ```

1. Dodaj plik `multipaths.txt` do pliku `/etc/multipath.conf`. Upewnij się, że jego zawartość trafi do sekcji `multipaths { ... }` (zwórć uwagę na ostatnią linijkę wydruku z punku 1.)

    ```bash
    cat mutlipaths.txt >> /etc/multipath.conf
    ```

    i zamknij nawias sekcji `multipaths`:

    ```bash
    echo "}" >> etc/multipath.conf
    ```

1. Przeładuj `multipathd`:

	```
    systemctl reload multipathd
    ```

1. Sprawdź czy wszystko gra:

    ```bash
    [root@tsm-waw5-sds01 srv-8.1.18]# multipath -ll  | grep IBM
    sp-inst1 (360050768108101fb400000000000001d) dm-29 IBM,2145
    sp-dc12 (360050768108101fb4000000000000019) dm-11 IBM,2145
    ```