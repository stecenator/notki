# TSM QuickSheets

DSM_SYS=/usr/tivoli/tsm/client/ba/bin64/dsm.sys
DSM_OPT=/usr/tivoli/tsm/client/ba/bin64/dsm.opt
USR=admin
PWD=admin
# lista SErverNames
# grep -i servername $DSM_SYS| grep -v \* | awk '{print $2}'


# definicja funkcji zwracajacej zdefiniowane 


function get-servername() { 
  if [ "$#" -eq  "0" ]
    then
      grep -i servername $DSM_SYS| grep -v \* | awk '{print $2}'
  else
      echo "**** ServerName: $1 ****"; dsmc q sched -se=$1
  fi
}
  
 
 function get-nodename()  { 
  if [ "$#" -eq  "0" ]
    then
      grep -i nodename   $DSM_SYS| grep -v \* | awk '{print $2}'
  else
      echo  "**** NodeName: $nodeName ****";  dsmadmc -id=$USR -password=$PWD  q node f=d
  fi
}
  
