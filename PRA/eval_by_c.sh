#!/bin/bash

ll_path=$1    # liblinear path
ip_dir=$2    # input dataset dir, like /home/jiangxiaotian/Experiments/AttPathRNN/PRA/ACL2015_dataset/dataset_PRA_NBin
op_dir=$3    # output dir, like /home/jiangxiaotian/Experiments/AttPathRNN/PRA/ACL2015_dataset/FindC

c_values=(0.03125 0.625 0.125 0.25 0.5 1 2 4 8 16 32)

# for each query relation, evaluate its model on different c_values.
echo "-------- [Evaluate on different c values] --------"
for rel in `ls $ip_dir`    # rel = query relation
do
    if [ "${rel:0:1}" != "_" ] ;then continue; fi
    rel_model_pred=$op_dir/model_and_predictions/$rel
    mkdir -p $rel_model_pred
    op_file=$op_dir/${rel}.cs.txt
    for c_value in ${c_values[@]}
    do
        echo "Rel="$rel", C="$c_value | tee $op_dir/train.log
        modelname="c$c_value.train.txt.model"
        $ll_path/train -s 0 -c $c_value $ip_dir/$rel/train.txt $rel_model_pred/$modelname >> $op_dir/train.log
        sleep 1
        $ll_path/predict -b 1 $ip_dir/$rel/dev.txt $rel_model_pred/$modelname $rel_model_pred/c${c_value}.dev_predictions.txt >> $op_dir/dev_predict.log
        $ll_path/predict -b 1 $ip_dir/$rel/test.txt $rel_model_pred/$modelname $rel_model_pred/c${c_value}.test_predictions.txt >> $op_dir/test_predict.log
        echo "C="$c_value", AP on dev, test = " >> $op_file
        python cal_ap.py -p $rel_model_pred/c${c_value}.dev_predictions.txt -l $ip_dir/$rel/dev.txt >> $op_file
        python cal_ap.py -p $rel_model_pred/c${c_value}.test_predictions.txt -l $ip_dir/$rel/test.txt >> $op_file
        # $ll_path/predict -b 1 $rel_model_pred/test.txt $rel_model_pred/train.txt.model $rel_model_pred/test_predictions.txt > test_predict.log
    done
done

echo "-------- [Find optim c value on each query relation, and calculate MAP] --------"
python ./findOptimC_getMAP.py -i $op_dir > $op_dir/optimC_MAP.txt