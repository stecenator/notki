# Instalacja klienta BA

## Łindołs

Winda jaka jest, kazdy widzi. Tu piszę tricki które się przydają w chodzeniu na skróty ;-)

### Instalacja `CAD` i `schedule`  przy pomocy `dsmcutil.exe`


```
dsmcutil install scheduler /name:"tsmscheduler" /node:dwhb /password:ibm12345 /startnow:no 
dsmcutil install cad /node:dwhb /password:ibm12345 /autostart:yes /startnow:no 
dsmcutil update cad /name:"tsm client acceptor" /cadschedname:"tsmscheduler" 
dsmcutil start /name:"tsm client acceptor"
```