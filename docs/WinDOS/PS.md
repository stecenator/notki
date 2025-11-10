# Przydatne Powershelle
Pewnie każdy windziarz to zna, ale dla mnie to jak odkrycie koła.

## Wyświetlanie **`pipe`** w systemie

Przy uruchamianiu *Journal Engine* klienta Backup-Archive, czasem trzeba sprawdzić jakie `NamedPipe` zostały utworzone:

```PowerShell
Get-ChildItem \\.\pipe\
```

## WWPNy kart FC

Przegrałem flaszkę, bo twierdziłem, że się nie da:

```PowerShell
Get-WmiObject -class MSFC_FCAdapterHBAAttributes -namespace "root\WMI" | ForEach-Object {(($_.NodeWWN) | ForEach-Object {"{0:x}" -f $_}) -join ":"}
```
