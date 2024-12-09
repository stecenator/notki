# Przydatne Powershella
Pewnie każdy windziarz to zna, ale dla mnie to jak odkrycie koła.

## OS

1. Wyświetlanie **`pipe`** w systemie

	```PowerShell
	Get-ChildItem \\.\pipe\
	```

1. Wyświetlanie **WWPNów kart FC** (przegrałem flaszkę, bo twierdziłem, że się nie da):

	```PowerShell
	Get-WmiObject -class MSFC_FCAdapterHBAAttributes -namespace "root\WMI" | ForEach-Object {(($_.NodeWWN) | ForEach-Object {"{0:x}" -f $_}) -join ":"}
	```
