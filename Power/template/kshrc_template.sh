HOST=`hostname`
PS1="[1;31m$USER[0;31m@[0m$HOST[0;36m:\$PWD [0m# "
PATH=/usr/es/sbin/cluster:/usr/es/sbin/cluster/utilities:/usr/ios/cli:/opt/ibm/dscli:$PATH
HISTSIZE=5000
EXTENDED_HISTORY=ON
export PS1 PATH HISTSIZE EXTENDED_HISTORY 
eval $(/usr/bin/X11/resize)
alias rs='eval $(/usr/bin/X11/resize)'
set -o vi
