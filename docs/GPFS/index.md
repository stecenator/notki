# Storage Scale / GPFS 

## Instalacja scoutfree

Żeby zainstalować GPFS bez `dsmcscoutd`, przed instalacją pakietów i w `.profile` roota ustaw:

```
export HSMINSTALLMODE=SCOUTFREE
```

## Komendy GPFS:

- **`mmlsfs fileystem`** - Sprawdzić czy `-A no` i `-z no` - potem się `z` przestawi a `A` ma zostać na no, bo HSM nie supportuje yes.
- **`mmlscluster`** - pokazuje właściwości klastra GPFS.
- **`mmlsconfig`** - Parametry klastra takie jak `pagepool`, czy `maxWorkerThreads`

## Komendy HSM:

- **`dsmmigfs query -d filesystem_gpfs`** - właściwości migracji
- **`dsmmigfs add filesystem_gpfs`** -  dodaje filesystem do migracji.