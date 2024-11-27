# Nazewnictwo na przydkladzie elixir
```
hostnames
	- elixira
	- elixirb
virtual IP
	- elixirservice

TSM nody:
	- elixira			  	# dsmcad na domyslnym dsm.opt 
	- elixirb				# dsmcad na domyslnym dsm.opt 
	- elixirservice			# dsmcad -se=elixirservice - klastrowy agent  np: uruchamiany przez /hacmp/ora.start
	- elixir-ora          	# chroniona aplikacja - odpowiedzialna za oracle'a
TSM servernames:
	- elixira				# nodename elixira
	- elixirb				# nodename elixirb
	- elixirservice			# nodename elixirservice
	- elixir-ora			# nodename elixir-ora
		- schedlogname /var/log/tsm/elixir-ora/dsmsched.log
		- errorlogn    /var/log/tsm/elixir-ora/dsmerror.log		
		- errorlogret 60 d
		- schedlogret 60 d
		- passworddir /local/data/tsm/PWD				# Katalog w zasobie klastrowym z uprawnieniami dla oracle




Wazne:

nie zapominac o dsm.sys w katalogu
/usr/tivoli/tsm/client/api/bin64

najlepiej zrobic ln -s

ln -s ../../ba/bin64/dsm.sys dsm.sys
```

