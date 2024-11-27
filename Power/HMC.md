# Dynamiczne partycjonowanie

## Dodanie do viosa adaptera typu `vfchost`

```
chhwres -r virtualio -m Server-8284-22A-SN7889EFX --id 3 -o a -s 101 --rsubtype fc -a "adapter_type=server,remote_lpar_id=10,remote_slot_num=21"
```

Gdzie:

- **-r virtualio** - typ zasobu
- **-m Server-8284-22A-SN7889EFX** - pudło
- **--id 3** - LPAR ID VIOSa
- **-o a** - chyba operacja, `a` że dodaję
- **-s 101** - wirtualny slot na partycji VIOS
- **--rsubtype fc** - że to będzie `vfchost`
- **-a** - lista atrybutów w cudzysłowach: "adapter_type=server,remote_lpar_id=10,remote_slot_num=21"
 - **adapter_type=server** - adapter serwerowy
 - **remote_lpar_id=10** - id LPARu klienckiego
 - **remote_slot_num=21** - slot LPARu klienckiego

Drugi przykład z dynamicznym dołożeniem 4 adapterów z dwóch viosów do klienta:

```bash
chhwres -r virtualio -m CG-9080-M9S-SN7853F48 --id 12 -o a -s 720 --rsubtype fc -a "adapter_type=server,remote_lpar_id=10,remote_slot_num=10"
chhwres -r virtualio -m CG-9080-M9S-SN7853F48 --id 13 -o a -s 720 --rsubtype fc -a "adapter_type=server,remote_lpar_id=10,remote_slot_num=11"
chhwres -r virtualio -m CG-9080-M9S-SN7853F48 --id 12 -o a -s 721 --rsubtype fc -a "adapter_type=server,remote_lpar_id=10,remote_slot_num=12"
chhwres -r virtualio -m CG-9080-M9S-SN7853F48 --id 13 -o a -s 721 --rsubtype fc -a "adapter_type=server,remote_lpar_id=10,remote_slot_num=13"

chhwres -r virtualio -m CG-9080-M9S-SN7853F48 --id 10 -o a -s 10 --rsubtype fc -a "adapter_type=client,remote_lpar_id=12,remote_slot_num=720"
chhwres -r virtualio -m CG-9080-M9S-SN7853F48 --id 10 -o a -s 11 --rsubtype fc -a "adapter_type=client,remote_lpar_id=13,remote_slot_num=720"
chhwres -r virtualio -m CG-9080-M9S-SN7853F48 --id 10 -o a -s 12 --rsubtype fc -a "adapter_type=client,remote_lpar_id=12,remote_slot_num=721"
chhwres -r virtualio -m CG-9080-M9S-SN7853F48 --id 10 -o a -s 13 --rsubtype fc -a "adapter_type=client,remote_lpar_id=13,remote_slot_num=721"
