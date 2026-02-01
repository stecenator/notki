---
icon: material/hammer-screwdriver
---

# Instalacja oprogramowania Pacemaker

I przyległośći.

## Rpozytoria i instalacja softu

Włącz repozytoria _Pacemaker_ w RedHat. 

!!! Note "Uwaga"
    Trzeba mieć na to licencję "HA".

1. Sprawdź dostępne repozytoria:

    ```sh title="Dostępne repozytoria"
    sudo subscription-manager repos
    ```

    ??? Example "Przykład"

        ```sh hl_lines="2"
        $ sudo subscription-manager repos | grep -i high
        Repo ID:   rhel-9-for-x86_64-highavailability-eus-rpms
        Repo Name: Red Hat Enterprise Linux 9 for x86_64 - High Availability - Extended Update Support (RPMs)
        Repo URL:  https://cdn.redhat.com/content/eus/rhel9/$releasever/x86_64/highavailability/os
        ```

1. Włącz repozytriom z paczkami HA dla Twojego OS (1):
    { .annotate }

    1. U mnie to :simple-redhat: 9, ale procedurę przepisuję ze swojego starego dokumentu dla v7.

    ```sh title="Włączanie repo HA"
    sudo subscription-manager repos --enable rhel-9-for-x86_64-highavailability-rpms
    ```

1. Zainstaluj poaczki z _Pacemakerem_ i kilka, które mogą się przydać:

    - pacemaker
    - pcs
    - fence-virt # Jeśli klaster stoi na libvirt/KVM
    - fence-agents-ipmilan  # Jeśli stralam do fizycznych pudeł
    - psmisc
    - python3-policycoreutils

    ```sh title="Instalacja pakietów klastrowych"
    sudo dnf install pacemaker pcs fence-virt fence-agents-ipmilan psmisc python3-policycoreutils
    ```

    OS oczywiście szarpnie sobie pół internetu z zależności :wink:.