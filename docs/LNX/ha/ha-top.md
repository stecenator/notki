---
icon: material/graph
---

# Topografia i rozruch klastra

Na tym etapie tworzę pusty klaster, bez zasobów. Żródłem mojej mądrości jest [ten](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/configuring_and_managing_high_availability_clusters/assembly_getting-started-with-pacemaker-configuring-and-managing-high-availability-clusters#proc_learning-to-configure-failover-getting-started-with-pacemaker) kawałek dokumentacji :simple-redhat:.

1. Po zainstalowaniu `pcsd` zostanie utowrzony użyszkodnik klastra: `hacluster`. Nadaj mu hasło:

    ```sh title="Zmiana hasła dla hacluster"
    passwd hacluster
    ```

1. Uwierzytelnianie węzłów. Trzeba to zrobić przynajmniej z jednego węzła, ale lepiej z obu. Wtedy będzie można uruchamiać komendy `pcs cośtam` z obydwu nodów.

    ```sh title="Uwierzytlenianie węzłów"
    pcs host auth sp-n1 sp-n2
    ```

    !!! Warning "Uwaga"
        Składnia tego polecenia zminiła sie! W RH7 było `pcs cluster auth` a nie `pcs host auth`. Nie wiem jak jest w 8.

    ??? Example "Przykład"

        ```sh
        # pcs host auth sp-n1 sp-n2 
        Username: hacluster
        Password: 
        sp-n1: Authorized
        sp-n2: Authorized
        ```

1. Utwórz klaster o nazwie `sp`:

    !!! Tip "Wskazówka"
        Lepiej jest od razu skonfigurować więcej niż jedną sieć

    === "1 sieć, sprawdzone polecenie"
    
        ```sh title="Tworzenie i start klastra sp"
        pcs cluster setup sp --start sp-n1 sp-n2
        ```

    === "2 sieci, halucynowane"

        Halucynowane, ale wygląda sensownie.

        ```sh title="Tworzenie klastra z dwoma sieciami"
        sudo pcs cluster setup nazwa_klastra \
          wezel1 addr=192.168.1.101 addr=10.0.0.101 \
          wezel2 addr=192.168.1.102 addr=10.0.0.102
        ```


    ??? Example "Przykład"

        ```sh hl_lines="1"
        [root@sp-n1 ~]# pcs cluster setup sp --start sp-n1 sp-n2
        No addresses specified for host 'sp-n1', using 'sp-n1'
        No addresses specified for host 'sp-n2', using 'sp-n2'
        Destroying cluster on hosts: 'sp-n1', 'sp-n2'...
        sp-n2: Successfully destroyed cluster
        sp-n1: Successfully destroyed cluster
        Requesting remove 'pcsd settings' from 'sp-n1', 'sp-n2'
        sp-n1: successful removal of the file 'pcsd settings'
        sp-n2: successful removal of the file 'pcsd settings'
        Sending 'corosync authkey', 'pacemaker authkey' to 'sp-n1', 'sp-n2'
        sp-n1: successful distribution of the file 'corosync authkey'
        sp-n1: successful distribution of the file 'pacemaker authkey'
        sp-n2: successful distribution of the file 'corosync authkey'
        sp-n2: successful distribution of the file 'pacemaker authkey'
        Sending 'corosync.conf' to 'sp-n1', 'sp-n2'
        sp-n1: successful distribution of the file 'corosync.conf'
        sp-n2: successful distribution of the file 'corosync.conf'
        Cluster has been successfully set up.
        Starting cluster on hosts: 'sp-n1', 'sp-n2'...
        ```

1. __Tymczasowo__ Wyłącz _STONITH_:

    ```sh title="Wyłączanie mechanizmu STONITH"
    pcs property set stonith-enabled=false
    ```

    !!! Danger "Uwaga"
        To jest tylko do czasu, kiedy skonfiguruję zasób typu STONITH. Ja mam ty prosty klaster na KVM. Dla Prawdziwych klastrów trzeba będzie dodak kilka mechnizmów, najprawdopodobniej bazujących na `IPMI` lub `SBD`.

---
To jest dobry moment, żeby wziąc się za konfigurowanie zasobów. Wróć tu jak skonfigurujesz IP i filesystemy klastrowe.
---

## Dodawanie sieci do klastra

_Corosync_ odpowiedzialny za topografię klastra, komunikuje się po sieciach skonfigurowanych podczas budowania klastra. Jeśli jest tylko jedna sieć, a klaster ma dwa węzły i nie ma quorum, to wyłączenie sieci na jednym z węzłów jest intrpretowane jako __split brain__ i np SBD inicjuje awaryjny odstrzał... obu węzłow. Dlatego warto dodać drugą sieć, najlepiej korzystającą z niezależnych od piwrwszej przełaczników i kart.

1. Lista __ringów__ klastra:

    ```sh title="Ringi klastra"
    corosync-cfgtool -s
    ```

    ??? Example "Klaster z 1 ringiem"

        ```sh
        # corosync-cfgtool -s
        Local node ID 2, transport knet
        LINK ID 0 udp
                addr    = 10.20.27.202
                status:
                        nodeid:          1:     connected
                        nodeid:          2:     localhost
        ```

1. Można to robić komendami `pcs link ...`, ale prościej jest wyedytować __na wszystkich węzłach__ plik `/etc/corosync/corosync.conf` i po prostu dopisać tam dodatkową sieć:

    ``` hl_lines="12 19"
    totem {
        version: 2
        cluster_name: tsm-b
        transport: knet
        crypto_cipher: aes256
        crypto_hash: sha256
        cluster_uuid: 0e885cb67f1640a1b127e3e162941419
    }

    nodelist {
        node {
            ring0_addr: tsm-b1.storage.psnc
            ring1_addr: tsm-b1.hb
            name: tsm-b1.storage.psnc
            nodeid: 1
        }

        node {
            ring0_addr: tsm-b2.storage.psnc
            ring1_addr: tsm-b2.hb
            name: tsm-b2.storage.psnc
            nodeid: 2
        }
    }

    quorum {
        provider: corosync_votequorum
        two_node: 1
    }

    logging {
        to_logfile: yes
        logfile: /var/log/cluster/corosync.log
        to_syslog: yes
        timestamp: on
    }
    ```

1. Przeładuj `corosync`.

    ```sh title="Przeładowanie corosync"
    sudo corosync-cfgtool -R
    ```

1. Sprawdź czy nowy ring działa 

    ```sh hl_lines="1 8-12"
    # corosync-cfgtool -s
    Local node ID 2, transport knet
    LINK ID 0 udp
            addr    = 10.20.27.202
            status:
                    nodeid:          1:     connected
                    nodeid:          2:     localhost
    LINK ID 1 udp
            addr    = 10.20.54.2
            status:
                    nodeid:          1:     connected
                    nodeid:          2:     localhost
    ```

## Konfiguracja mechanizmów STONITH

Tezeba mieć minimim jeden mechanizm STONITH. Warto dwa. Ja użyję takiech:

- [SBD](#storage-based-death-sbd)
- [IPMI](#ipmi)

### Storage Based Death (SBD)

W sytuacji, gdy węzły nie mogą komunikować się np z modułami IMM albo virt, warto jest udostępnić moduł SBD - przesyła on komunikaty poprzez współdzielnoe urządzenie. Ma to też dodatni plus w postaci dodatkowej ścieżki po SAN do komunikacji w klastrze.

1. Zainstaluj pakied `sbd`:

    ```sh title="instalacja SBD"
    sudo dnf install sbd fence-agents-sbd
    ```

1. Określ jakie urządzenie blokowe będzie odpowiedzialne za SBD. W tym przykładzie to LUN z macierzy, tóry dzieki dobrodziejstwu _friendly names_ w `multipath.conf` nazywa się `pcmk-sbd`

    !!! Note 
        Tę czynniość rób na jednym węźle.

    ```sh title="Tworzenie SBD"
    sudo sbd -d /dev/mapper/pcmk-sbd create
    ```

1. Na drugim węźle sprawdź czy widzisz zainicjalizowane SBD:

    ```sh title="Weryfikacja SBD"
    sudo sbd -d /dev/mapper/pcmk-sbd dump
    ```

    ??? Example "Przykład"
        ```sh
        [root@sp01-n1 ~]# sbd -d /dev/mapper/pcmk-sbd dump
        ==Dumping header on disk /dev/mapper/pcmk-sbd
        Header version     : 2.1
        UUID               : 33b85d88-b4ed-4e3d-9a60-ba56d9f99a6f
        Number of slots    : 255
        Sector size        : 512
        Timeout (watchdog) : 5
        Timeout (allocate) : 2
        Timeout (loop)     : 1
        Timeout (msgwait)  : 10
        ==Header on disk /dev/mapper/pcmk-sbd is dumped
        ```

1. __Na obu  węzłach__ dopisz do `/etc/sysconfig/sbd` sekcję `SBD_DEVICE`. Plik po modysikacji powinien zawirać takie sekcje (pomijając komentarze):

    ``` title="/etc/sysconfig/sbd"
    SBD_DEVICE="/dev/mapper/pcmk-sbd"
    SBD_PACEMAKER=yes
    SBD_STARTMODE=always
    SBD_DELAY_START=no
    SBD_WATCHDOG_DEV=/dev/watchdog
    SBD_WATCHDOG_TIMEOUT=5
    SBD_TIMEOUT_ACTION=flush,reboot
    SBD_MOVE_TO_ROOT_CGROUP=auto
    SBD_SYNC_RESOURCE_STARTUP=yes
    SBD_OPTS=
    ```

1. Skonfguruj _watchdog_. __Na obu pudłach__. Moduł `softdog` pewnie będzie załadowany przez _Pacemakera_ ale lepiej go dopisać do atutomatycznego logowania:

    ```sh
    echo softdog > /etc/modules-load.d/softdog.conf
    ```

    Jeśli `lsmod` nie pokazał tego modułu, to go załaduj. Weryfikacja:

    ```sh
    [root@sp01-n1 ~]# ls -l /dev/watchdog
    crw------- 1 root root 10, 130 Mar 25 12:51 /dev/watchdog
    ```

1. __Na obu pudłach__ włącz usługę _SBD_.

    ```sh title="Włączanie SBD"
    systemctl enable sbd
    ```

    !!! Note 
        Nie uruchamiaj jej. Zrobi to _Pacemaker_.

1. Dodaj zasób _STONITH_ do klastra:

    ```sh title="Tworzenie zasobu STONITH SBD"
    pcs stonith create sbd-fencing fence_sbd devices=/dev/mapper/pcmk-sbd op monitor interval=30s
    ```

1. Włącz _STONITH_ w klastrze:

    ```sh title="Włączanie STONITH w klastrze"
    pcs property set stonith-enabled=true
    ```

1. Sprawdź status _STONITH_:

    ```sh title="Status STONITH"
    pcs stonith status
    ```

    ??? Example "Przykład"
        ```sh
        [root@sp01-n2 ~]# pcs stonith status 
        * sbd-fencing (stonith:fence_sbd):     Started sp01-n1
        ```

    !!! Tip "Wskazówka"

        Jeżeli `pcs status` pokaże, że zasób stonith jest `inactive`, przestartuj klaster komendami:

        ```sh title="Ostrzegawczy strzał w tył głowy"
        sudo pcs cluster stop --all
        sudoo pcs cluster start --all
        ```

### IPMI

!!! Bug
    Dopiszę ten fragment, jak będe miał dostęp do klastra gdzie OS ma dostęp do IPMI sąsiada :smile:.


Strzelanie przez IPMI jest przydatne gdy klaster ma fizycznie inną sieć do administracji i kontaktu z IPMI niż do produkcji. 

1. Upewnij się, że na węzłach klastra jest zainstalowana paczka `fence-agents-ipmilan`.
1. 

## Quorum

!!! Bug 
    Muszę to rozkminić. :simple-redhat: ładnie to [opisuje](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/8/html/configuring_and_managing_high_availability_clusters/assembly_configuring-quorum-devices-configuring-and-managing-high-availability-clusters).