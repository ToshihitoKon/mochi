#!/usr/bin/env bash
cd `dirname $0`
state_file="state"

usase_exit(){
    echo "Usase: $0 [get|set|toggle|addgroup|list|listgroup]"
    echo -e "\tget [keys...]"
    echo -e "\ttoggle [key]"
    echo -e "\tset [key] [value] (group)"
    echo -e "\taddgroup [group] [keys...] "
    echo -e "\tlist"
    echo -e "\tlistgroup"
    exit 1
}

_get_value_by_key(){
    value=`echo "$state" | grep $'\t'"$key"$'\t' | sed -e 's/.*\t.*\t//g'`
}

_get_value_by_group(){
    value=`echo "$state" | grep "^$group"$'\t'| sed -e 's/.*\t.*\t//g'`
}

_get_group_by_key(){
    group=`echo "$state" | grep $'\t'"$key"$'\t' | sed -e 's/\t.*\t.*//g'`
}

_set_value_by_key(){
    if [ ! "$group" ]; then
        _get_group_by_key
    fi
    sed $state_file -i -e "/^.*\t$key\t.*$/d"
    echo -e "$group\t$key\t$value" >> $state_file
}

get_value(){
    if [ "$#" -eq 0 ]; then
        usase_exit
        exit 1
    fi

    for key in $@; do
        key=$key
        _get_value_by_key
        echo -e "$key\n$value"
    done
}

set_value(){
    if [ ! "$1" -o ! "$2" ]; then
        usase_exit
        exit 1
    fi

    key=$1
    value=$2
    group=$3
    _set_value_by_key

    echo -e "$key\n$value"
}

toggle_value(){
    if [ ! "$1" ]; then
        usase_exit
        exit 1
    fi
    key=$1
    _get_value_by_key

    case "$value" in
    0        ) value=1;;
    1        ) value=0;;
    [Ff]alse ) value=true;;
    [Tt]rue  ) value=false;;
    *        ) exit 1;;
    esac

    _set_value_by_key
    echo -e "$key\n$value"
}

list_keys(){
    cat $state_file | sed -e 's/.*\t\(.*\)\t.*/\1/g'
}

list_group(){
    cat $state_file | sed -e 's/\t.*\t.*//g' | grep -v "^$"
}

_test(){
    echo [test _set_value_by_key]
    key=testkey
    value=testvalue
    group=testgroup
    _set_value_by_key
    echo $group  $key $value

    # refresh
    state=`cat $state_file`

    echo [test _get_value_by_key]
    value=""
    _get_value_by_key
    echo $group  $key $value

    echo [test _get_value_by_group]
    value=""
    _get_value_by_group
    echo $group  $key $value

    echo [test _get_group_by_key]
    group=""
    _get_group_by_key
    echo $group  $key $value

}

if [ ! "$1" ];then
    usase_exit
fi
command=$1

touch $state_file
state=`cat $state_file`

case "$command" in
    "get"    ) shift 1; get_value $*;;
    "toggle" ) toggle_value $2;;
    "set"    ) shift 1; set_value $*;;
    "addgroup" ) shift 1; add_group $*;;
    "list"   ) list_keys;;
    "listgroup" ) list_group;;
    "test" ) _test;;
    *        ) usase_exit ;;
esac
