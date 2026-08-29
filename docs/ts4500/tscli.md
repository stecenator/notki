---
icon: octicons/terminal-16
---

# Command Line - TSCLI

!!! Tip inline end

	`TS4500CLI.jar` można siągnąć z [IBM Fix Central](https://www.ibm.com/support/fixcentral/swg/quickorder?parent=Tape%20autoloaders%20and%20libraries&product=ibm/Storage_Tape/TS4500+Tape+Library+(3584)&release=1.0&platform=All&function=all&source=fc).
	Leży sobie na dole strony, za firmłerami, w sekcji _Tools_.

Duże biblioteki mają CLI, i jak to z CLI bywa, niektóre rzeczy robi się tu szybciej. Np. reset napędów :smile:. Tutaj lista moich ulubionych komend. 

**Minusem** uzywania CLI jest to, że w historii shella odkłada się hasło :man_facepalming:. 

## Lista bibliotek logicznych

---
Komenda: `--viewLogicalLibraries`

---

```sh
java -jar ~/bin/TS4500CLI.jar -u admin -p xxxx -ip ts4500.nowhere.com -ssl --viewLogicalLibraries
```

??? Example "Przykład"

	```bash
	$ java -jar ~/bin/TS4500CLI.jar -u admin -p xxxx -ip ts4500.nowhere.com -ssl --viewLogicalLibraries
                Name,           Type, Assigned Cartridges,   Virtual I/0 cartridges,    Drives,                       Encryption Method, Queued Exports,VOLSER Reporting (6/8/All/Last8 characters)
                lib1,            LTO,                2119,                        0,         8
	```

## Lista napędów 

---
Komenda: `--viewDriveSummary`

---

Używam tego do znalezioenie nummeru seryjnego i WWNN.

```sh
java -jar ~/bin/TS4500CLI.jar -u admin -p xxxx -ip ts4500.nowhere.com -ssl --viewDriveSummary
```

??? Example "Przykład"

	```sh
	$ java -jar ~/bin/TS4500CLI.jar -u admin -p xxxx -ip ts4500.nowhere.com -ssl --viewDriveSummary
	Location(F,C,R),               State,           Operation,            Type,        Contents,    Firmware,         Serial,             WWWNN, Element Address,Logical Library
     F3, C2, R1,              ONLINE,               EMPTY,        3588-FAC,           Empty,       T3S0 ,     000781B79D,  50050760441b2704,             263,UNASSIGNED
     F3, C2, R2,              ONLINE,               EMPTY,        3588-FAC,           Empty,       T3S0 ,     000781B0ED,  50050760441b2705,             262,UNASSIGNED
     F3, C2, R3,              ONLINE,               EMPTY,        3588-FAC,           Empty,       T3S0 ,     000781B0FD,  50050760441b2706,             261,UNASSIGNED
     F3, C2, R4,              ONLINE,               EMPTY,        3588-FAC,           Empty,       T3S0 ,     0007819E0D,  50050760441b2707,             260,UNASSIGNED
     F3, C3, R1,              ONLINE,               EMPTY,        3588-F8C,           Empty,       S2T0 ,     000781B09D,  50050760441b2708,             263,    lib1
     F3, C3, R2,              ONLINE,               EMPTY,        3588-F8C,           Empty,       S2T0 ,     000781B08D,  50050760441b2709,             262,    lib1
     F3, C3, R3,              ONLINE,               EMPTY,        3588-F8C,           Empty,       S2T0 ,     00078320AB,  50050760441b270a,             257,    lib1
     F3, C3, R4,              ONLINE,               EMPTY,        3588-F8C,           Empty,       S2T0 ,     0007810FCD,  50050760441b270b,             258,    lib1
     F3, C4, R1,              ONLINE,               EMPTY,        3588-F8C,           Empty,       S2T0 ,     000781B07D,  50050760441b270c,             264,    lib1
     F3, C4, R2,              ONLINE,               EMPTY,        3588-F8C,           Empty,       S2T0 ,     000783219B,  50050760441b270d,             259,    lib1
     F3, C4, R3,              ONLINE,               EMPTY,        3588-F8C,           Empty,       S2T0 ,     00078320EB,  50050760441b270e,             260,    lib1
     F3, C4, R4,              ONLINE,               EMPTY,        3588-F8C,           Empty,       S2T0 ,     00078320FB,  50050760441b270f,             261,    lib1
	```

## Lista napędów z adresami WWPN

---
Komenda: `--viewFibreChannel`

---

Przy zoningu point-to-point lepiej jest używać WWPNów (choć podobno można i WWNNów, ale nigdy nie próbowałem).

```sh
java -jar ~/bin/TS4500CLI.jar -u admin -p xxxx -ip ts4500.nowhere.com -ssl --viewFibreChannel
```

??? Example "Przykład"

	```sh
		$ java -jar ~/bin/TS4500CLI.jar -u admin -p xxxx -ip ts4500.nowhere.com -ssl --viewFibreChannel                                                                                                                                         8s 15:47:38
                    Drive,Location(F,C,R),                         Logical Library,           Type,                Port(1,2),    Link Status,Configured Link Speed,Configured Topology,Actual Link Speed,Actual Topology
         50050760441b270a,     F3, C3, R3,                                    lib1,       3588-F8C,         50050760445b270a, Light Detected,           Auto,         N Port,         8 Gb/s,         N Port
                         ,               ,                                        ,               ,         50050760449b270a, Light Detected,           Auto,         N Port,         8 Gb/s,         N Port
         50050760441b270b,     F3, C3, R4,                                    lib1,       3588-F8C,         50050760445b270b, Light Detected,           Auto,         N Port,         8 Gb/s,         N Port
                         ,               ,                                        ,               ,         50050760449b270b, Light Detected,           Auto,         N Port,         8 Gb/s,         N Port
         50050760441b2704,     F3, C2, R1,                              UNASSIGNED,               ,         50050760445b2704, Light Detected,           Auto,         N Port,               ,         N Port
                         ,               ,                                        ,               ,         50050760449b2704, Light Detected,           Auto,         N Port,               ,         N Port
         50050760441b2705,     F3, C2, R2,                              UNASSIGNED,               ,         50050760445b2705, Light Detected,           Auto,         N Port,               ,         N Port
                         ,               ,                                        ,               ,         50050760449b2705, Light Detected,           Auto,         N Port,               ,         N Port
         50050760441b2706,     F3, C2, R3,                              UNASSIGNED,               ,         50050760445b2706, Light Detected,           Auto,         N Port,               ,         N Port
                         ,               ,                                        ,               ,         50050760449b2706, Light Detected,           Auto,         N Port,               ,         N Port
         50050760441b2707,     F3, C2, R4,                              UNASSIGNED,               ,         50050760445b2707, Light Detected,           Auto,         N Port,               ,         N Port
                         ,               ,                                        ,               ,         50050760449b2707, Light Detected,           Auto,         N Port,               ,         N Port
         50050760441b2708,     F3, C3, R1,                                    lib1,       3588-F8C,         50050760445b2708, Light Detected,           Auto,         N Port,         8 Gb/s,         N Port
                         ,               ,                                        ,               ,         50050760449b2708, Light Detected,           Auto,         N Port,         8 Gb/s,         N Port
         50050760441b2709,     F3, C3, R2,                                    lib1,       3588-F8C,         50050760445b2709, Light Detected,           Auto,         N Port,         8 Gb/s,         N Port
                         ,               ,                                        ,               ,         50050760449b2709, Light Detected,           Auto,         N Port,         8 Gb/s,         N Port
         50050760441b270c,     F3, C4, R1,                                    lib1,       3588-F8C,         50050760445b270c, Light Detected,           Auto,         N Port,         8 Gb/s,         N Port
                         ,               ,                                        ,               ,         50050760449b270c, Light Detected,           Auto,         N Port,         8 Gb/s,         N Port
         50050760441b270d,     F3, C4, R2,                                    lib1,       3588-F8C,         50050760445b270d, Light Detected,           Auto,         N Port,         8 Gb/s,         N Port
                         ,               ,                                        ,               ,         50050760449b270d, Light Detected,           Auto,         N Port,         8 Gb/s,         N Port
         50050760441b270e,     F3, C4, R3,                                    lib1,       3588-F8C,         50050760445b270e, Light Detected,           Auto,         N Port,         8 Gb/s,         N Port
                         ,               ,                                        ,               ,         50050760449b270e, Light Detected,           Auto,         N Port,         8 Gb/s,         N Port
         50050760441b270f,     F3, C4, R4,                                    lib1,       3588-F8C,         50050760445b270f, Light Detected,           Auto,         N Port,         8 Gb/s,         N Port
                         ,               ,                                        ,               ,         50050760449b270f, Light Detected,           Auto,         N Port,         8 Gb/s,         N Port
    ```

