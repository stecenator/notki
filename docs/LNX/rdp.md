---
icon: material/remote-desktop
---

# Zdalny pulpit dla wialu użyszkodników

Wymagane paczki:

- `gnome-remote-desktop`
- `gdm`
- `freerdp`

!!! Info
    RDP w RedHat działa jako usługa, która wymaga hasła w dostępie do ekranu. Także do ekranu logowania systemowego :man_facepalming:, dlatego użytkownicy chcący się zalogować zdalnie będą musieli znać hasło sesji RDP **oraz** poziadać własne konto w systemie. 

## Instalacja wymagań

Jeśli wcześniej tego nie zrobiono, warto zainstalować cały profil "Server with GUI".

1. Lista dostępnych profili instalacji:

    ```sh title="Lista profili instalacji"
    sudo dnf grouplist
    ```

    ??? Example "Przykład"

        ```sh hl_lines="5 9-10"
        root@cinek-lnx01:~#  dnf grouplist
        Updating Subscription Management repositories.
        IBM_Power_Tools                                                 3.6 kB/s | 1.5 kB     00:00    
        Available Environment Groups:
           Server with GUI
           Minimal Install
           Workstation
           Custom Operating System
        Installed Environment Groups:
           Server
        Installed Groups:
           Headless Management
           Container Management
        Available Groups:
           Smart Card Support
           Legacy UNIX Compatibility
           Security Tools
           Graphical Administration Tools
           .NET Development
           Console Internet Tools
           System Tools
           Scientific Support
           RPM Development Tools
           Development Tools
           Network Servers
        ```

1. Jeśli na liście *Installed Environment Groups* nie ma *Server with GUI*, zainstaluj ją.

    ```sh title="Instalacja grupy pakietów"
    sudo dnf groupinstall "Server with GUI"
    ```

    W zależności od tego co było wcześniej zinatalowane, system może szarpnąc pół Internetu :shrug:. Jest to dość wygodna metoda "wyrównania" systemu tak, żeby uzupełnił sobie brakujące paczki.

    ??? Example "Przykład"

        ```sh hl_lines="55"
        root@cinek-lnx01:~# sudo dnf groupinstall "Server with GUI"
        Updating Subscription Management repositories.
        Last metadata expiration check: 0:05:56 ago on Tue 16 Dec 2025 09:04:43 PM CET.
        no group 'base-graphical' from environment 'graphical-server-environment'
        Dependencies resolved.
        ============================================================================================================================================
         Package                                           Arch        Version                         Repository                              Size
        ============================================================================================================================================
        Upgrading:
         amd-gpu-firmware                                  noarch      20251008-15.8.el10_0            rhel-10-for-ppc64le-appstream-rpms      28 M
         at                                                ppc64le     3.2.5-14.el10_1                 rhel-10-for-ppc64le-baseos-rpms         67 k
         buildah                                           ppc64le     2:1.41.6-1.el10_1               rhel-10-for-ppc64le-appstream-rpms     8.9 M
         fprintd                                           ppc64le     1.94.5-1.el10_0                 rhel-10-for-ppc64le-appstream-rpms     191 k
         fprintd-pam                                       ppc64le     1.94.5-1.el10_0                 rhel-10-for-ppc64le-appstream-rpms      24 k
         glibc                                             ppc64le     2.39-58.el10_1.2                rhel-10-for-ppc64le-baseos-rpms        2.9 M

        [ ... Bardzo dużo komunikatow ...] 

        Installing Environment Groups:
         Server with GUI                                                                                                                           
        Installing Groups:
         Container Management                                                                                                                      
         Core                                                                                                                                      
         Fonts                                                                                                                                     
         GNOME                                                                                                                                     
         GNOME Server Defaults                                                                                                                     
         Guest Desktop Agents                                                                                                                      
         Hardware Monitoring Utilities                                                                                                             
         Hardware Support                                                                                                                          
         Headless Management                                                                                                                       
         Internet Browser                                                                                                                          
         Multimedia                                                                                                                                
         Common NetworkManager submodules                                                                                                          
         Printing Client                                                                                                                           
         Server product core                                                                                                                       
         Standard                                                                                                                                  

        Transaction Summary
        ============================================================================================================================================
        Install  559 Packages
        Upgrade   50 Packages

        Total download size: 883 M
        Is this ok [y/N]: y

        [ ... Znowu bardz odużo komunikatów ...]

          xprop-1.2.7-3.el10.ppc64le                                               yelp-tools-42.1-8.el10.noarch                                    
          yelp-xsl-42.1-7.el10.noarch                                             

        Complete!
        ```

        !!! Note
            Ponieważ system przy okazji zaktuzliaował pakieg `glibc` nalezy mu się reboot. Ale to poźniej, bo po skonfigurowaniu zdalnego pupitu też będzie to potrzebne.

            RDP dla wielu użytkowników będzie także wymagać utworzenie certyfikatu TLS.  

1. Upewnij się, że zależność wciągnąłyu odpowiednie paczki:

    ```sh title="Sprawdzanie czy wymagane pakiety są zainstalowane"
    rpm -q gnome-remote-desktop gdm freerdp
    ```

    !!! Example "Przykład"

        ```sh
        root@cinek-lnx01:~# rpm -q gnome-remote-desktop gdm freerdp
        gnome-remote-desktop-47.3-2.el10_0.ppc64le
        gdm-47.0-11.el10.ppc64le
        package freerdp is not installed
        ```

    Jak widać na przykladzie pakiet `freerdp` nie nalezy do zainstalowanego środowiska, nalezy go więc zainstalaowć dodatkowo.

1. Zainstaluj pakiet `freerdp`

    ```sh
    sudo dnf install freerdp
    ```

1. Jako użytkownik `gnome-remote-desktop` (1) wykonaj poniższe polecenie:
    { .annotate }
    1. Właściciel procesu serwera RDP w systemie.

    ```sh
    sudo -u gnome-remote-desktop mkdir -p ~gnome-remote-desktop/.local/share/gnome-remote-desktop
    ```

1. Wygeneruj certyfikat TLS dla serwera RDP:

    ```sh
    sudo -u gnome-remote-desktop winpr-makecert -silent -rdp -path ~gnome-remote-desktop/.local/share/gnome-remote-desktop tls
    ```

1. Ustaw klucz i certyfikat dla usługi RDP:

    ```sh
    sudo grdctl --system rdp set-tls-key ~gnome-remote-desktop/.local/share/gnome-remote-desktop/tls.key
    sudo grdctl --system rdp set-tls-cert ~gnome-remote-desktop/.local/share/gnome-remote-desktop/tls.crt
    ```

1. Ustaw użytkownika i hasło do ekranu RDP

    ```sh
    sudo grdctl --system rdp set-credentials
    Init TPM credentials failed because No TPM device found, using GKeyFile as fallback.
    Username: rdpuser
    Password: P@$$4RDP
    ```
1. Włącz usługę RDP:

    ```sh
    sudo grdctl --system rdp enable
    ```

1. Włącz zdalne logowanie przez `GDM`

    ```sh
    sudo systemctl enable --now gdm
    sudo systemctl enable --now gnome-remote-desktop.service  # przy właczaniu tego system może sobie przypomnieć, że należał mu się reboot"
    sudo systemctl set-default graphical.target
    ```

1. Dodaj na firewallu regułe zezwalającą na ruch RDP:

    ```sh
    sudo firewall-cmd --add-service=rdp
    sudo firewall-cmd --add-service=rdp --permanent
    ```

1. Ostrzegawczy strzał w tył głowy:

    ```sh
    sudo shutdown -r now 
    ```

1. Weryfikacja (po restarcie):

    ```sh hl_lines="17"
    sudo systemctl status gnome-remote-desktop.service
    ● gnome-remote-desktop.service - GNOME Remote Desktop
         Loaded: loaded (/usr/lib/systemd/system/gnome-remote-desktop.service; enabled; preset: disabled)
         Active: active (running) since Tue 2025-12-16 21:58:08 CET; 6min ago
     Invocation: f12e3f62c49849e3b8be92a50ff7c013
       Main PID: 1133 (gnome-remote-de)
          Tasks: 4 (limit: 21840)
         Memory: 30.3M (peak: 41.6M)
            CPU: 48ms
         CGroup: /system.slice/gnome-remote-desktop.service
                 └─1133 /usr/libexec/gnome-remote-desktop-daemon --system

    Dec 16 21:58:08 cinek-lnx01 systemd[1]: Starting gnome-remote-desktop.service - GNOME Remote Desktop...
    Dec 16 21:58:08 cinek-lnx01 gnome-remote-de[1133]: Init TPM credentials failed because No TPM device found, using GKeyFile as fallback
    Dec 16 21:58:08 cinek-lnx01 systemd[1]: Started gnome-remote-desktop.service - GNOME Remote Desktop.
    Dec 16 21:58:09 cinek-lnx01 gnome-remote-de[1133]: RDP server started
    ```

1. Zaloguj się do serwera klientem RDP:
    <br><br>
    ![Logowanie do RDP](../assets/lnx-rdp-1.png)
    <br><br>

1. Po podaniu hasła RDP zobaczysz ekran logowania do systemu (GDM):
    <br><br>
    ![Logowanie do RDP](../assets/lnx-rdp-2.png)
    <br><br>

1. Po zalogowaniu dostaniesz dostęp do zdalnegu pulpitu. 
    
    !!! Danger ":skull: :skull: :skull: Uwaga :skull: :skull: :skull:"
        Nie klikaj w pomarańczową ikonę :material-cast:, bo odetniesz się od zdalnej sesji, która jednak będzie nadal wisiała w systemie. Jesli jednak to zrobisz, trzeba bedzie zrestartować usługę `gnome-remote-desktop`:

        ```sh title="restart zdalnego pupitu"
        sudo systemctl restart  gnome-remote-desktop
        ```
