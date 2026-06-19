# Moduł Ansible dla IBM Power

## Przygotowanie stacjji kontrolnej

Musisz mieć w miarę współczesnego :simple-linux:. Np :simple-fedora: Fedora się świetnie nada. . Potrzebujesz następujących paczek systemowych:

- ansible-core
- ansible


Dodatkowo bedą potrzebne takie kolekcje z [Ansible Galaxy](https://galaxy.ansible.com):


| Collection                  | Version |
|-----------------------------|---------|
| ansible.windows             | 3.5.0   |
| ibm.power_aix               | 2.0.3   |
| ibm.power_hmc               | 1.15.0  |
| ibm.power_vios              | 1.3.0   |
| ibm.storage_virtualize      | 3.3.0   |

### Katalog projektu :simple-ansible:

W katalogu projektu, np `~/projects/gpfs-workshop` utwórz plik `ansible.cfg` z następującą zawartością:



Struktura katalogu `ansible`:

```bash title="Struktura katalogu ansible"
$ tree                                                                                                                                                  13:43:47
.
├── ansible.cfg
├── group_vars
│   └── all.yml
├── hmc_info.yaml
├── hosts
├── secrets.enc
└── vios_info.yaml
```

### Konfiguracja ansible


```ini title="ansible.cfg"
--8<-- "ansible/ansible.cfg"
```

## Projekt Storage Scale

### Hosts

```ini title="hosts"
--8<-- "ansible/hosts"
```

### Zmienne globalne `all`

```yaml title="group_vars/all.yml"
--8<-- "ansible/group_vars/all.yml"
```

### Zmienne grupy `gpfs`

```yaml title="group_vars/gpfs.yaml"
--8<-- "ansible/group_vars/gpfs.yaml"
```

### Sekrety

!!! Note

    Plik `secrets.enc` zawiera dane w formacie Ansible Vault. Aby go odszyfrować, należy użyć polecenia:

    ```bash
    ansible-vault view secrets.enc 
    ```

    Analogicznie do edycji będą służyć parametry `edit` a do utworzenie `create`. Za każdym razem trzeba będzie podać hasło do _sejfu_.

<br>

```yaml title="secrets.enc"
---
hmc_user: "twój_użyszkodnik_hmc"
hmc_pass: "tajne_haslo_hmc"
fs_user: "twój_użyszkodnik_fs"
fs_pass: "tajne_haslo_fs"

```

## Przydatne playbooki

W kolejności losowej ;-) 

### Power

#### :octicons-play-16: Tworzenie LPARów

```yaml title="mklpar.yaml"
--8<-- "ansible/mklpar.yaml"
```

!!! Info "Informacja"
    Ten playbook tworzy profile o nazwie _default_profile_. Potem z tych profili będziemy wydłubywać np _WWPNy_ kart fc do zoningu.

#### :octicons-play-16: dodawanie vscsi do LPARów

Ponieważ z jakichś tajemniczych powodów moduł _ibm.power_hmc.lpar_instance_ nie potrafi założyć LPAR z wirtualnym CD, dodaję CeDeki w drugim kroku:

```yaml title="add_vscsi.yaml"
--8<-- "ansible/add_vscsi.yaml"
```

#### :octicons-play-16: Usuwanie LPARów

!!! Bug
    Dorobić.

### FlashSystem

#### :octicons-play-16: Tworzenie dysków systemowych

```yaml title="mk_os_vdisks.yaml"
--8<-- "ansible/mk_os_vdisks.yaml"
```

#### :octicons-play-16: Snapshot dysków systemowych

```yaml title="mk_os_snap.yaml"
--8<-- "ansible/mk_os_snap.yaml"
```

#### :octicons-play-16: Usuwanie dysków systemowych

#### :octicons-play-16: Wyciąganie WWPNów z profili LPARów

```yaml title="ansible/get_wwpn.yaml"
--8<-- "ansible/get_wwpn.yaml"
```

Tworzy plik `wwpn_addresses.txt`, krego można użyć do zoningu i definicji hostów na macierzy.

### Linux

#### :octicons-play-16: PRzygotowanie OSa do pracy z GPFS

```yaml title="ansible/os_prep.yaml"
--8<-- "ansible/os_prep.yaml"
```

### Uruchamianie playbooków

Wszystkie playbooki tego warsztatu są uruchamiane podobnie do przykładu poniżej. Zmień tylko nazwę pliku _yaml_ :wink:.

Przykładowy playbook odpytujący HMC o interesuące rzeczy:

```yaml title="hmc_info.yaml"
--8<-- "ansible/hmc_info.yaml"
```

Uruchomienie playbooka może wwyglądać tak:

```bash title="Uruchomienie playbooka hmc_info:"
$ ansible-playbook hmc_info.yaml -e @secrets.enc --ask-vault-pass
```

:simple-ansible: spyta Cię o hasło do pliku `secrets.enc`. Pniżej znajduje się przykład uruchomienia tego playbooka:

??? Example "Przykładowe uruchomienie"

    ```bash
    $ ansible-playbook hmc_info.yaml -e @secrets.enc --ask-vault-pass                                                                                                                          6s 14:29:23
    Vault password: 

    PLAY [localhost] *****************************************************************************************************************************************************************************************************************************************

    TASK [Odpytywanie HMC] ***********************************************************************************************************************************************************************************************************************************
    [WARNING]: Platform linux on host localhost is using the discovered Python interpreter at /usr/bin/python3, but future installation of another Python interpreter could change the meaning of that path. See https://docs.ansible.com/ansible-
    core/2.18/reference_appendices/interpreter_discovery.html for more information.
    ok: [localhost]

    TASK [Wyświetlenie konsoli] ******************************************************************************************************************************************************************************************************************************
    ok: [localhost] => {
        "build_info": {
            "ansible_facts": {
                "discovered_interpreter_python": "/usr/bin/python3"
            },
            "build_info": {
                "BASEVERSION": "V11R1",
                "FIXPACKS": [
                    "MF71740 - iFix for HMC V11R1 M1110"
                ],
                "HMCBUILDLEVEL": "2510290407",
                "RELEASE": "1",
                "SERVICEPACK": "1110",
                "VERSION": "11"
            },
            "changed": false,
            "failed": false,
            "warnings": [
                "Platform linux on host localhost is using the discovered Python interpreter at /usr/bin/python3, but future installation of another Python interpreter could change the meaning of that path. See https://docs.ansible.com/ansible-core/2.18/reference_appendices/interpreter_discovery.html for more information."
            ]
        }
    }

    TASK [Informacje o zarządzanym pudle] ********************************************************************************************************************************************************************************************************************
    ok: [localhost]

    TASK [Wyświetlenie informacji o pudle] *******************************************************************************************************************************************************************************************************************
    ok: [localhost] => {
        "sys_info": {
            "changed": false,
            "failed": false,
            "system_info": {
                "ActivatedLevel": "88",
                "ActivatedServicePackNameAndLevel": "fw1110.01 (88)",
                "BMCVersion": null,
                "CapacityOnDemandMemoryCapable": "true",
                "CapacityOnDemandProcessorCapable": "true",
                "ConfigurableSystemMemory": 4194304,
                "ConfigurableSystemProcessorUnits": 40.0,
                "CurrentAvailableSystemMemory": 3659776,
                "CurrentAvailableSystemProcessorUnits": 12.3,
                "DeferredLevel": null,
                "DeferredServicePackNameAndLevel": null,
                "Description": null,
                "EBMCSystemIPv6Capable": "true",
                "IPAddress": "172.16.222.160",
                "InstalledSystemMemory": 4194304,
                "InstalledSystemProcessorUnits": 48,
                "IsClassicHMCManagement": "true",
                "IsNotPowerVMManagementController": "false",
                "IsNotPowerVMManagementMaster": "false",
                "IsPowerVMManagementController": "false",
                "IsPowerVMManagementMaster": "false",
                "MTMS": "9824-42A*78DF551",
                "ManufacturingDefaultConfigurationEnabled": "false",
                "MaximumPartitions": 960,
                "MemoryDefragmentationState": "Not_In_Progress",
                "MergedReferenceCode": "",
                "MeteredPoolID": null,
                "PNORVersion": null,
                "PermanentSystemMemory": 4194304,
                "PermanentSystemProcessors": 40,
                "PhysicalSystemAttentionLEDState": "true",
                "ProcessorThrottling": "false",
                "ReferenceCode": "",
                "ServiceProcessorVersion": "000B000A",
                "State": "operating",
                "StateDetail": "",
                "SystemFirmware": "OB1110_fw1110.01 (88)",
                "SystemLocation": "",
                "SystemName": "POWER11-Showroom",
                "SystemType": "ebmc"
            }
        }
    }

    PLAY RECAP ***********************************************************************************************************************************************************************************************************************************************
    localhost                  : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
    ```