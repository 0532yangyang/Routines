#!/bin/bash

input_dir=$1
output_dir=$2
max_path_l=$3

for rel in `ls $input_dir`
do
    if [ "${rel:0:1}" != "_" ] ;then continue; fi
    cmd="./predicate2PRAFormat.py -i $input_dir/$rel -o $output_dir/$rel -m $max_path_l"
    if [ $# == 4 ]; then
      cmd=$cmd" $4"
    elif [ $# == 5 ]; then
      cmd=$cmd" $4 $5"
    else
      cmd=$cmd
    fi
    echo "Command="$cmd
    python $cmd
done
