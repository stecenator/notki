# Zaklęcia związane z `libvirt` i `virsh`

Większość rzeczy poniżej można pewnie zrobic ładniej. Pewnie z czasem to upiększę.

## Klonowanie maszyny

**Założenia:**

- Bazuję na [tym](https://gist.github.com/aojea/7b32879f949f909f241d41c4c9dbf80c) giście.
- Maszyna źródłowa to `rhel9-srv` - Tylko XML vmki. Dysk mam już zamrożony w obrazie nieprzypisanym do VMki, żeby przez przypadek go nie zmienić.
- Maszynki docelowe to: `gpfs-1` i `gpfs-2`
- Obraz źródłowy dysku: `RHEL9-template-07.2025-don_not_run.qcow2`

1. Zwal XMLa maszyny źródłowej do tymczasowego pliku:

	```sh
	$ sudo virsh dumpxml rhel9-srv > golden-img.xml
	```

1. Utwórz zlinkowane klony dysków dla nowych VMek:

	```sh
	$ qemu-img create gpfs-1-os.qcow2 -f qcow2 -b RHEL9-template-07.2025-don_not_run.qcow2 -F qcow2
	Formatting 'gpfs-1-os.qcow2', fmt=qcow2 cluster_size=65536 extended_l2=off compression_type=zlib size=75161927680 backing_file=RHEL9-template-07.2025-don_not_run.qcow2 backing_fmt=qcow2 lazy_refcounts=off refcount_bits=16
	$ qemu-img create gpfs-2-os.qcow2 -f qcow2 -b RHEL9-template-07.2025-don_not_run.qcow2 -F qcow2
	Formatting 'gpfs-2-os.qcow2', fmt=qcow2 cluster_size=65536 extended_l2=off compression_type=zlib size=75161927680 backing_file=RHEL9-template-07.2025-don_not_run.qcow2 backing_fmt=qcow2 lazy_refcounts=off refcount_bits=16
	```

1. Spreparuj XMLa do klonowania: uzuń UUD i adresy MAC z kart sieciowych.

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

	**Uwaga:** to polecenie nie sprawdza, czy jest tam wiele dysków z podobnym prefixem, więc uruchamiać "ze zrozumieniem" ;-).

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