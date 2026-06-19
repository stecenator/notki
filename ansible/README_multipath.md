# Generowanie konfiguracji multipath dla dysków GPFS

## Opis

Playbook `gen_multipath_conf.yaml` automatycznie generuje plik konfiguracyjny multipath dla dysków GPFS Data utworzonych na macierzy IBM FlashSystem 5200.

## Wymagania

- Ansible z kolekcją `ibm.storage_virtualize`
- Dostęp do macierzy FlashSystem (zmienne `fs_user`, `fs_pass` w `secrets.enc`)
- Dyski utworzone przez playbook `mk_gpfs_data_vdisks.yaml`

## Użycie

### 1. Uruchomienie playbooka

```bash
ansible-playbook gen_multipath_conf.yaml --ask-vault-pass
```

### 2. Wygenerowany plik

Playbook utworzy plik `mio.conf` zawierający wpisy multipath w formacie:

```
multipaths {
    multipath {
        wwid "3600507681081818bc8000000000001a"
        alias "cinek-gpfs-nsd01"
    }
    multipath {
        wwid "3600507681081818bc8000000000001b"
        alias "cinek-gpfs-nsd02"
    }
    ...
}
```

### 3. Wdrożenie na serwerach GPFS

Na każdym serwerze GPFS (cinek-gpfs01 do cinek-gpfs04):

```bash
# Skopiuj zawartość mio.conf do /etc/multipath.conf
sudo vi /etc/multipath.conf
# Wklej sekcję multipaths {} z pliku mio.conf

# Przeładuj konfigurację multipath
sudo systemctl reload multipathd

# Sprawdź czy dyski są widoczne z prawidłowymi aliasami
sudo multipath -ll
```

### 4. Weryfikacja

Po wdrożeniu, dyski powinny być widoczne jako:
- `/dev/mapper/cinek-gpfs-nsd01`
- `/dev/mapper/cinek-gpfs-nsd02`
- itd.

## Parametry playbooka

Można dostosować następujące zmienne w sekcji `vars`:

- `output_file`: nazwa pliku wyjściowego (domyślnie: `mio.conf`)
- `disk_prefix`: prefiks nazw dysków (domyślnie: `cinek-gpfs-nsd`)
- `disk_count`: liczba dysków do przetworzenia (domyślnie: `8`)

## Przykład dostosowania

Jeśli chcesz wygenerować konfigurację dla innej liczby dysków:

```yaml
vars:
  output_file: "custom_mio.conf"
  disk_prefix: "cinek-gpfs-nsd"
  disk_count: 16  # dla 16 dysków
```

## Uwagi

- WWID dysków jest generowany przez dodanie prefiksu "3" do vdisk_UID z macierzy
- Format WWID jest zgodny ze standardem SCSI (3 + 32 znaki hex)
- Aliasy odpowiadają nazwom dysków na macierzy dla łatwej identyfikacji