#!/usr/bin/env bash
cd `dirname $0`
state_file="state"

usase_exit(){
    echo "Usase: $0 [get|set|toggle|list] key [set value]"
}

get_value(){
    if [ ! "$1" ]; then
        usase_exit
        exit 1
    fi
    key=$1

    cat $state_file | grep "^$key"$'\t' | tr "\t" "\n"
}

set_value(){
    if [ ! "$1" -o ! "$2" ]; then
        usase_exit
        exit 1
    fi
    key=$1
    value=$2

    sed $state_file -i -e "/^$key\t.*$/d"
    echo -e "$key\t$value" >> $state_file
    echo -e "$key\n$value"
}

toggle_value(){
    if [ ! "$1" ]; then
        usase_exit
        exit 1
    fi
    key=$1

    before=`cat $state_file | grep $key$'\t' | cut -f 2`
    case "$before" in
    0        ) value=1;;
    1        ) value=0;;
    [Ff]alse ) value=true;;
    [Tt]rue  ) value=false;;
    *        ) exit 1;;
    esac

    sed $state_file -i -e "/^$key\t.*$/d"
    echo -e "$key\t$value" >> $state_file
    echo -e "$key\n$value"
}

list_keys(){
    cat $state_file | sed -e 's/\t.*//g'
}

if [ ! "$1" ];then
    usase_exit
fi

touch $state_file

case "$1" in
    "get"    ) get_value $2;;
    "toggle" ) toggle_value $2;;
    "set"    ) set_value $2 $3;;
    "list"   ) list_keys;;
    *        ) usase_exit ;;
esac
