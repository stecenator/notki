---
icon: simple/qemu
---

![LibVirt](../assets/Libvirt_logo.svg)

# Zaklęcia związane z `libvirt` i `virsh`

Większość rzeczy poniżej można pewnie zrobic ładniej. Pewnie z czasem to upiększę.

## Klonowanie maszyny

**Założenia:**

- Bazuję na [tym](https://gist.github.com/aojea/7b32879f949f909f241d41c4c9dbf80c) giście.
- Maszyna źródłowa to `rhel9-srv` - Tylko XML vmki. Dysk mam już zamrożony w obrazie nieprzypisanym do VMki, żeby przez przypadek go nie zmienić.
- Maszynki docelowe to: `gpfs-1` i `gpfs-2`
- Obraz źródłowy dysku: `RHEL9-template-07.2025-don_not_run.qcow2`

Procedura:

1. Zwal XMLa maszyny źródłowej do tymczasowego pliku:

	```sh
	sudo virsh dumpxml rhel9-srv > golden-img.xml
	```

1. Utwórz zlinkowane klony dysków dla nowych VMek:

	```sh
	qemu-img create gpfs-1-os.qcow2 -f qcow2 -b RHEL9-template-07.2025-don_not_run.qcow2 -F qcow2
	qemu-img create gpfs-2-os.qcow2 -f qcow2 -b RHEL9-template-07.2025-don_not_run.qcow2 -F qcow2
	```

	??? Example "Przykład"

		```sh
		$ qemu-img create gpfs-1-os.qcow2 -f qcow2 -b RHEL9-template-07.2025-don_not_run.qcow2 -F qcow2
		Formatting 'gpfs-1-os.qcow2', fmt=qcow2 cluster_size=65536 extended_l2=off compression_type=zlib size=75161927680 backing_file=RHEL9-template-07.2025-don_not_run.qcow2 backing_fmt=qcow2 lazy_refcounts=off refcount_bits=16
		$ qemu-img create gpfs-2-os.qcow2 -f qcow2 -b RHEL9-template-07.2025-don_not_run.qcow2 -F qcow2
		Formatting 'gpfs-2-os.qcow2', fmt=qcow2 cluster_size=65536 extended_l2=off compression_type=zlib size=75161927680 backing_file=RHEL9-template-07.2025-don_not_run.qcow2 backing_fmt=qcow2 lazy_refcounts=off refcount_bits=16
		```


1. Spreparuj XMLa do klonowania: usuń UUD i adresy MAC z kart sieciowych.

	```sh
	$ sed  -i '/uuid/d' golden-img.xml
	$ sed -i '/mac address/d' golden-img.xml
	```

1. Przygotuj oddzielne XMLe dla klonów. Trzeba podskrobać nazwę maszyny.

	```sh
	$ cat golden-img.xml | sed 's/rhel9-srv/gpfs-1/' > gpfs-1.xml
	$ cat golden-img.xml | sed 's/rhel9-srv/gpfs-2/' > gpfs-2.xml
	```

1. W nowych XMLach trzeba zmienić nazwę dysku systemowego na nowoutworzone klony:

	**Uwaga:** to polecenie nie sprawdza, czy jest tam wiele dysków z podobnym prefixem, więc uruchamiać "ze zrozumieniem" ;-).

	```sh
	$ sed -i 's|\(.*source file.*/\).*\.qcow2|\1gpfs-1-os.qcow2|' gpfs-1.xml
	$ sed -i 's|\(.*source file.*/\).*\.qcow2|\1gpfs-2-os.qcow2|' gpfs-2.xml
	```

1. No i pora zdefiniować nowe maszynki:

	```sh
	$ sudo virsh define gpfs-1.xml
	Domain 'gpfs-1' defined from gpfs-1.xml

	$ sudo virsh define gpfs-2.xml
	Domain 'gpfs-2' defined from gpfs-2.xml

	```

1. I wystartować:

	```sh
	$ sudo virsh start gpfs-1
	Domain 'gpfs-1' started
	
	$ sudo virsh start gpfs-2
	Domain 'gpfs-2' started

	```

## Dołączanie nowego dysku działającej VM

1. Utwórz obraz dysku, który ma być dołączony. Jak nie wiesz, to zajrzyj [tu](qmu-img.md).
1. Dołącz dysk. 

	!!! Tip "Podpowiedź"
		Jeśli dysk będzie jednocześnie dostępny dla wiecej niż jednej maszyny, podaj `--targetbus scsi`. Format takiego dyksu **musi** być `raw`.

	=== "QCOW2"

		```sh title="Dołączanie dysku w formacie qcow2"
		virsh attach-disk VMka /ścieżka/do/pliku.qcow2 nazwa_blokowa --driver qemu --type disk --config --live --subdriver qcow2
		```

		??? Example "Przykład"

			```sh
			virsh attach-disk toy /backup/restore/videovg-rest.qcow2 vdc --driver qemu --type disk --config --live --subdriver qcow2
			```

	=== "RAW"

		```sh title="Dołączanie dysku w formacie RAW"
		virsh attach-disk VMka /ścieżka/do/pliku.raw nazwa_blokowa --driver qemu --type disk --config --live --subdriver raw
		```

		??? Example "Przykład"

			```sh
			virsh attach-disk toy /backup/restore/videovg-rest.img vdc --driver qemu --type disk --config --live --subdriver raw
			```

	=== "Klaster SCSI"

		```sh title="Dołączanie dysku w formacie RAW do magistrali SCSI"
		virsh attach-disk VMka /ścieżka/do/pliku.raw nazwa_blokowa_scsi --driver qemu --type disk --config --live --subdriver raw --targetbus scsi --shareable
		```

		??? Example "Przykład"

			```sh
			sudo virsh attach-disk sp-n1 /home/marcinek/media/Szajsung/vm/pcmk-inst.raw  sdb --driver qemu --type disk --config --live --subdriver raw --targetbus scsi
			```

	!!! Warning "Ważne"
		Nie zapomnij o opcji `--subdriver`. Bez tego `virsh` słabo zgaduje rozmiar dysku, np przy podlaczaniu _sparse_ `qcow2.`

## Odłączanie dysku od działającej VMki

1. Upewnij się, że maszyna już go nie używa, to jest: odmontowala filesystemy, deaktywowała grupę VG.
1. Odłącz dysk komendą:

	```sh title="Odłączanie dysku od VMki"
	sudo virsh detach-disk VMka /ścieżka/do/pliku.qcow2
	```

	??? Example "Przykład"

		```sh
		sudo virsh detach-disk sp-n1 /home/marcinek/media/Szajsung/vm/pcmk-inst.raw
		```

## Dodawanie adaptera `virtio-scsi`

Jak kleję klaster na moim KVM, to cześto okazuje się, że nie mam adpatera `virtio-scsi`, do któ©ego mogę podpiąć współdzielone dyski. Na żywca dodaje się to tak:

1. Utwórz plik `/tmp/virtio-scsi.xml` z definicją urządzenia:

	```xml title="Definicja adaptera virtio-scsi"
	<controller type='scsi' model='virtio-scsi'/>
	```

1. Dodaj je do maszyny:

	```sh title="Hotplug urządzenia do działającej VMki"
	sudo virsh attach-device VMka /tmp/virtio-scsi.xml --live --config
	```

	??? Example "Przykład"

		```sh
		sudo virsh attach-device sp-n1 /tmp/virtio-scsi.xml --live --config
		```