---
icon: material/notebook
---

# Komendy klastra

Spis cześo używanych poleceń zwoązanych z klastrem Pacemaker.

## Status klastra

```sh title="status klstra"
sudo pcs cluster status
```

## Start/stop klastra

### Start na wszystkich węzłach

```sh title="Start klastra na wszystkich węzłach"
sudo pcs cluster start --all
=======
Rozsądne jest, żeby klaster nie startował autoamatycznie wraz systemem. bo w pewnych systuacjach węzły mogą się wystrzelać  zanim zdążysz rozwiązać problem.

```sh title="Ręczny start klastra na wszystkich nodach"
sudo pcs cluster start --all
```

??? Example "Przykład"

    ```sh
    $ sudo pcs cluster start --all
    sp-n2: Starting Cluster...
    sp-n1: Starting Cluster...
    ```



## Zasoby

### Status zasobów

```sh title="Lista i stan zasobów klastra"
sudo pcs resource status
```

### Włączanie i wyłączanie zasobów

```sh title="Włączenie zasobu"
sudo pcs resource enable <zasób>
```

??? Example "Przykład"

# Testowanie klastra

Testy obejmują sprawdzenie czy klaster przełacza zasoby w przypppadku różnych awarii. 

## Wyłączenie węzła

Tymczasowe wyłączenie węzła i wymuszenie przeniesiania zasobów.

```sh title="Node stanby"
sudo pcs node standby <węzeł klastra>
```

??? Example "Przykład"

    ```sh hl_lines="1 11-12 14-16 26-27"
    $ sudo pcs cluster status
    Cluster Status:
     Cluster Summary:
       * Stack: corosync (Pacemaker is running)
       * Current DC: sp-n1 (version 2.1.10-1.el9-5693eaeee) - partition with quorum
       * Last updated: Mon Feb 16 20:59:15 2026 on sp-n1
       * Last change:  Mon Feb 16 20:58:37 2026 by root via root on sp-n1
       * 2 nodes configured
       * 1 resource instance configured
     Node List:
       * Online: [ sp-n1 sp-n2 ]
     $ sudo pcs resource status
      * Resource Group: spinst1-rg:
        * spvg_lvm  (ocf:heartbeat:LVM-activate):    Started sp-n1
    $ sudo pcs node standby sp-n1
    $ sudo pcs cluster status
    Cluster Status:
     Cluster Summary:
       * Stack: corosync (Pacemaker is running)
       * Current DC: sp-n1 (version 2.1.10-1.el9-5693eaeee) - partition with quorum
       * Last updated: Mon Feb 16 21:10:18 2026 on sp-n1
       * Last change:  Mon Feb 16 21:10:06 2026 by root via root on sp-n1
       * 2 nodes configured
       * 1 resource instance configured
     Node List:
       * Node sp-n1: standby
       * Online: [ sp-n2 ]
    PCSD Status:
      sp-n2: Online
      sp-n1: Online
    ```

    Dla weryfikacji warto sprawdzić na drugm węźle czy zasób faktycznie jest. W tym przykładzie sprawdzam czy grupa `spvg` jest aktywna i jakie ma `systemid`:

    ```sh
    $ sudo vgs -o+systemid
      VG   #PV #LV #SN Attr   VSize    VFree System ID
      rhel   1   3   0 wz--n-  <69.00g    0           
      spvg   6   6   0 wz--n- <307.98g    0  sp-n2    
    ```

## Włączenie węzła bedącego w trybie `standby`

!!! Note "Uwaga"
    Operacja `unstandby` nie przywraca zasobów na ten węzeł. Jesłi jest taka potrzeba, to przenieś je ręcznie.

```sh title="PRzywrócenie węzła do klastra"
sudo pcs node unstandby <węzeł klastra>
```

# OS

Komendy systemowe, które mogą przydać się w kontekście klastra.

## Wykrywanie PV na drugim węźle klastra

```
sudo pvscan --cached
```
