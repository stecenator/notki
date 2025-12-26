---
icon: 
---

# Tricki ogólnounixowe

## OpenSSH :material-ssh:

### Agent

Agent się przydaje, gdy ze względów bezpieczeńistwa, czyli teraz praktycznie zwasze, trzeba mieć klucz zabezpieczony passphrase. 

!!! Tip " :simple-linux: i Gnome"
    Sesja Gnome na linuxie (1) sam startuje agenta ssh i automatycznie ładuje wszystkie klucze z `~/.ssh/`. Daltego jeśli będziesz pracowac bezpośrednio ze swojej maszyny, prawdopodobnie nie musisz użuywac agenta. Ten rozdział przydaje się, gdy po drodze jest przesiadkowy host.
    { .annotate }

    1.  A pewnie i wszedzie tam, gdzie współczesnego Gnoma można spotkać.

    !!! Bug
        Sprawdzić jak to się zachowuje z kluczami z passphrase. 

#### Start agenta

1. Uruchom agenta:

    ```sh title="Start agenta SSH"
     eval "$(ssh-agent -s)"
    ```

    Uruchomienie przez `eval` spowoduje wykonanie także kodu wygenerowanego komendą `ssh-agent -s`, czyli ustawanie i wyexpotowanie zmiennych `SSH_AGENT_PID` i `SSH_AUTH_SOCK`.

     !!! Example "Przykład"

        ```sh
        [root@spns ibm]# eval "$(ssh-agent -s)"
        Agent pid 13518
        [root@spns ibm]# echo $SSH_AGENT_PID
        13518
        [root@spns ibm]# echo $SSH_AUTH_SOCK
        /tmp/ssh-XXXXXXSFYucr/agent.13517
        ```

1. Dodaj klucz do agenta

    ```sh title="Dodanie wszystkich kluczy do agenta"
    ssh-add
    ```

    ??? Example "Przykład:"

        ```sh
        [root@spbg01 ibm]# ssh-add
        Enter passphrase for /root/.ssh/id_ed25519:
        Identity added: /root/.ssh/id_ed25519 (root@spbg01.ad.nsz.gov.rs)
        ```

#### Ubicie agenta

Agent ma tę właściwość, że po zamknięciu sesji zostaje. Znając jego `$SSH_AUTH_SOCK` można się do niego ponownie podłączyć, co nie zawsze jest pożadane. Dlatego warto go :skull: koncząc pracę z terminalem:

```sh title="Zamknęcie ssh_agent"
[root@spns ibm]# ssh-agent -k
unset SSH_AUTH_SOCK;
unset SSH_AGENT_PID;
echo Agent pid 13518 killed;
```

!!! Tip "Do rozważenia"
    Pewnie warto wrzucić komendę `ssh-agent -k` do jakiegoś skryptu typu `~/.bash_logout` czy innego `~/.zlogout`. 