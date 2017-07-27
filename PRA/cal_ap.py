import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-p','--prediction_path', required=True)
parser.add_argument('-l','--label_path', required=True)
args = parser.parse_args()

prediction_path = args.prediction_path
label_path = args.label_path


def cal_ap_from_score(pred_file, lb_file):
    input_list = []    # model_name, ep_index, score, label
    with open(pred_file, 'r') as fl:
        for ep_idx, line in enumerate(fl.readlines()[1:]):    # ep_index starts from 0
            label, score, _ = line.strip().split(' ')
            input_list.append([int(ep_idx), float(score), int(label)])
    with open(lb_file, 'r') as t_fl:
        for i, line in enumerate(t_fl.readlines()):
            label = int(line.split(" ")[0])
            input_list[i][2] = label

    sorted_list = sorted(input_list, key=lambda x: x[1], reverse=True)

    ap = 0.0
    count_ones = 0
    for i, tu in enumerate(sorted_list):
        # if tu[2] < 0.5:    # if predicted as negative
        #     break
        if tu[2] == 1:
            count_ones += 1
            tmp = count_ones/float((i+1))
            ap += tmp
    ap /= count_ones
    return ap

ap_value = cal_ap_from_score(prediction_path, label_path)
print " - AP: {0}\t Path: {1}".format(ap_value, prediction_path)


