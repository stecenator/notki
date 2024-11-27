# VIOS

## Mapowania vFC w CSV

```
# ioscli lsmap -all -npiv -field name clntid clntname vfcclient fc vfcclientdrc -fmt ,
```

## Mapowania vSCSI/vOPT w CSV

```
# ioscli lsmap -all -field svsa physloc vtd clientid backing -fmt ,
```