---
icon: material/graph
---

# Topografia i rozruch klastra

Na tym etapie tworzę pusty klaster, bez zasobów. Żródłem mojej mądrości jest [ten](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/configuring_and_managing_high_availability_clusters/assembly_getting-started-with-pacemaker-configuring-and-managing-high-availability-clusters#proc_learning-to-configure-failover-getting-started-with-pacemaker) kawałek dokumentacji :simple-redhat:.

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

    ```sh title="Tworzenie i start klastra sp"
    pcs cluster setup sp --start sp-n1 sp-n2
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
        To jest tylko do czasu, kiedy skonfiguruję zasób typu STONITH. Ja mam ty prosty klaster na KVM. Dla Prawdziwych klastrów trzeba będzie dodak kilka mechnizmów, najprawdopodobniej bazujących na `IPMI`.
        