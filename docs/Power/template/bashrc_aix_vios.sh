if [ "$EUID" -eq 0 ]; then
    USER_COLOR='\[\e[31m\]'   # czerwony
else
    USER_COLOR='\[\e[32m\]'   # zielony
fi

PS1="${USER_COLOR}\u\[\e[0m\]@\[\e[33m\]\h\[\e[0m\]:\[\e[34m\]\w\[\e[0m\]\\$ "

export PATH=/usr/es/sbin/cluster:/usr/es/sbin/cluster/utilities:/usr/ios/cli:/opt/ibm/dscli:$PATH