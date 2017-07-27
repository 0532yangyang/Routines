# -*- coding:utf-8 -*-

import argparse
import os
import re

parser = argparse.ArgumentParser()
parser.add_argument('-i',"--input_dir", required=True, help="input predicate dir")
parser.add_argument('-o',"--output_dir", required=True, help="output predicate dir")
parser.add_argument('-m',"--max_path_length", required=True, help= "filter paths that is too long")
parser.add_argument('-E', "--ent_in_path", action="store_true", default=False, help="if there is entities in path")
parser.add_argument('-B',"--bin_feat", action="store_true", default=False ,help="feature value is set to binary or path count")
args = parser.parse_args()
MAX_POSSIBLE_LENGTH_PATH = int(args.max_path_length)
input_dir = args.input_dir
out_dir = args.output_dir
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
USE_BIN_FEATURE = args.bin_feat
ENTITY_IN_PATH = args.ent_in_path
print "[Settings]"
print " - MAX_POSSIBLE_LENGTH_PATH: {0}".format(MAX_POSSIBLE_LENGTH_PATH)
print " - USE_BIN_FEATURE: {0}".format(USE_BIN_FEATURE)
print " - ENTITY_IN_FEATURE: {0}".format(ENTITY_IN_PATH)
PATH_DELIMIT = " ### " if not ENTITY_IN_PATH else "###"

# MAX_POSSIBLE_LENGTH_PATH = 7
# input_dir = "D:/gen_pra_format/_aviation_airport_serves"
# out_dir = "D:/gen_pra_format/out/_aviation_airport_serves"
# if not os.path.exists(out_dir):
#     os.makedirs(out_dir)

# max_length = -1
# train_files = ['/positive_matrix.tsv.translated','/negative_matrix.tsv.translated','/dev_matrix.tsv.translated','/test_matrix.tsv.translated'] ##dont change the ordering or remove entries. This is bad coding, I know.
# for counter,input_file in enumerate(train_files):
#     input_file = input_dir+input_file
#     print 'Processing '+input_file
#     with open(input_file) as f:
#         for entity_count, line in enumerate(f): #each entity pair
#             split = line.split('\t')
#             e1 = split[0].strip()
#             e2 = split[1].strip()
#             paths = split[2].strip()
#             split = paths.split('###').strip()    # [JXT] separate paths with ###
#             for path in split:
#                 path_len = len(path.split('-'))
#                 path_len = path_len/2 + 1
#                 if path_len > max_length:
#                     max_length = path_len
# print(max_length)
#
#
# max_length = min(MAX_POSSIBLE_LENGTH_PATH,max_length)    # MAX_POSSIBLE_LENGTH_PATH
# print 'Max length is '+str(max_length)

relpath2pid = {}
pid2freq = {}
max_pid=0
missed_entity_count = 0 #entity pair might be missed when we are putting constraints on the max length of the path.

label=''
input_files = ['/positive_matrix.tsv.translated','/negative_matrix.tsv.translated','/dev_matrix.tsv.translated','/test_matrix.tsv.translated']
for ip_file_cnt, input_file_name in enumerate(input_files):
    if ip_file_cnt == 0 or ip_file_cnt == 1:
        output_file = out_dir+'/train.txt'
        if ip_file_cnt == 0:    # train_positive
            label = '1'
        if ip_file_cnt == 1:    # train_negative
            label = '-1'
    if ip_file_cnt == 2:
        output_file = out_dir+'/dev.txt'
    if ip_file_cnt == 3:
        output_file = out_dir+'/test.txt'
    input_file = input_dir+input_file_name
    if ip_file_cnt != 1 and os.path.exists(output_file):    # 读到negative时, 如果没有old文件, 之前的positive也肯定会生成train.txt.
        print "Old {0} detected and deleted.".format(output_file)
        os.remove(output_file)
    print "Processing: {0} Output: {1}".format(input_file, output_file)
    with open(input_file ,'r') as f_in, open(output_file, 'a') as f_out:
        for entity_count, line in enumerate(f_in): #each entity pair 对于每对实体
            ep_pidlist = list()    # 保存每个ep的paths的id顺序. (包含重复)
            ep_pid2freq = dict()
            parts = line.strip().split('\t')
            e1 = parts[0].strip()
            e2 = parts[1].strip()
            assert e1[0] != '_' and e2[0] != '_'
            if len(parts) == 4:    # dev或test. 最后是1/-1(label)
                assert(ip_file_cnt == 2 or ip_file_cnt == 3)
                label = str(parts[3].strip())
            output_line = label + " "
            ep_path_cnt = 0
            for path in parts[2].strip().split(PATH_DELIMIT):
                path = path.strip()
                if path == "":
                    continue
                # if not ENTITY_IN_PATH:
                #     relpath = path
                relPath2join = []  # 区分逆关系(为了还原)
                for ele in path.split("-"):
                    if ele == "":    # ACL2015数据集中会出现
                        continue
                    if ENTITY_IN_PATH and "/m/" in ele:    # 忽略entity
                        continue
                    rel = ele
                    relPath2join.append(rel)
                relpath = "-".join(relPath2join)  # 路径特征
                # [DEBUG]
                if not ENTITY_IN_PATH:
                    try:
                        assert "-" + relpath + "-" == path
                    except AssertionError:
                        print "paths: " + parts[2]
                        print "rel_path: " + relpath
                        print "path: " + path.strip()
                        exit()
                path_len = len(relPath2join)
                if path_len > MAX_POSSIBLE_LENGTH_PATH:    # 路径长度过长的不要.
                    continue

                # reg_str = ur"/m/.*?-"    # 过滤掉路径中的实体    # [可能出错, 以后]
                # rel_path = re.sub(reg_str, "", path.strip())
                # path_len = len(rel_path.split('-')) + 1    # TODO [做错了] 我去我为啥要+1. 这样想要过滤掉长度>7的, 实际上会过滤掉>6的....
                # if path_len > MAX_POSSIBLE_LENGTH_PATH:    # 路径长度过长的不要.
                #     continue
                # # [DEBUG]
                # if relpath2id.has_key(rel_path):
                #     print "[HIT]: "+rel_path

                if not relpath2pid.has_key(relpath):
                    max_pid += 1
                    relpath2pid[relpath] = max_pid
                ep_pidlist.append(relpath2pid[relpath])
                # 两个freq计数
                pathid = relpath2pid[relpath]
                if not ep_pid2freq.has_key(pathid):
                    ep_pid2freq[pathid] = 0
                ep_pid2freq[pathid] += 1
                if not pid2freq.has_key(pathid):
                    pid2freq[pathid] = 0
                pid2freq[pathid] += 1

                ep_path_cnt += 1
            sorted_pidlist = sorted(set(ep_pidlist))    # liblinear格式要求每行的特征ids从小到大.
            ep_feat = ""
            for pid in sorted_pidlist:
                f_v = 1 if USE_BIN_FEATURE else ep_pid2freq[pid]
                ep_feat += "{0}:{1} ".format(pid, f_v)
            output_line += ep_feat
            # if max(ep_pid2freq.values()) > 1:
            #     print "[Find path freq > 1 in a EP], max={0}".format(max(ep_pid2freq.values()))

                # relation_types = each_path.split('-')    # rel+ent数目. 如果输入不含ent(isOnlyRelation=True), 则为|rel|
                # path_vec = []
                # for i, pname in relation_types:
                #     if i%2==1:
                #         continue
                #     path_vec.append(pname)
                # path_string = '-'.join(path_vec)
                # if path_ids.has_key(path_string):
                #     line += '\t'

            if ep_path_cnt != 0:
                f_out.write(output_line+'\n')
            else:
                print "  - [Drop EP] {0}".format(line)
            if entity_count % 1000 == 0:
                print "  - {0} entity pairs processed.".format(entity_count)

print "Writing relpath2id ..."
fmt_str = "{0}\t{1}\t{2}\n"
with open(out_dir+"/relpath2id", 'w') as f_p2id:
    f_p2id.write(fmt_str.format("relation_path", "feature_id", "path_frequency_in_dataset"))
    for k, v in relpath2pid.iteritems():
        f_p2id.write(fmt_str.format(k, v, pid2freq[v]))