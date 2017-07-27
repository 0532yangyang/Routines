# -*- coding: utf-8 -*-

# 用于检查Das17所用的数据集的各项指标和他报的是否相同；

import os
import sys

MaxPathLengthLimit = 9999 # 7
DS_DIR_PATH = sys.argv[1] # "D:/ExperimentsData/Das17/toy"

# 输出Das17报告的所有指标
def output_statistics():
    Ents = set()
    EntPairs = set()
    SP_rels = set()
    FB_rels = set()
    Paths = set()
    Query_rels = set()
    max_path_length = 0

    path_len_dists = {}    # 逐个qrel下路径长度与路径出现次数（不是路径数目。同一个路径可能出现若干次）的list（长度是下标）。

    for qrel in os.listdir(DS_DIR_PATH):
        print "Processing " + qrel
        if qrel[0]!= "_":
            continue
        Query_rels.add(qrel)
        path_len_dists[qrel] = [0]*(MaxPathLengthLimit+1)
        # for ds_split in ["negative"]:
        for ds_split in ["negative", "positive", "dev", "test"]:
            path = "{0}/{1}/{2}_matrix.tsv.translated".format(DS_DIR_PATH, qrel, ds_split)
            with open(path) as f:
                for line in f.readlines():
                    parts = line.strip().split('\t')
                    e1 = parts[0].strip()
                    e2 = parts[1].strip()
                    paths = parts[2].strip()
                    for path in paths.split(" ### "):
                        rels = path.strip().split('-')[1:-1]
                        path_len = len(rels)
                        if path_len > MaxPathLengthLimit:
                            continue
                        if path_len > max_path_length:
                            max_path_length = path_len
                        Ents.add(e1)
                        Ents.add(e2)
                        EntPairs.add("\t".join([e1,e2]))
                        for rel in rels:
                            try:
                                if rel[0] == "_":
                                    rel = rel[1:]
                            except:
                                print "rel[0] ERROR"
                                print 'path:'
                                print path
                                exit()
                            if rel.startswith("/"):
                                FB_rels.add(rel)
                            else:
                                SP_rels.add(rel)
                        path_len_dists[qrel][path_len] += 1
                        Paths.add(path.strip())

    n_path_occurance = 0.0
    acc_path_length = 0
    for path_len_dist in path_len_dists.values():
#         print path_len_dist
        for path_len in range(1,len(path_len_dist)):
            acc_path_length += path_len*path_len_dist[path_len]
            n_path_occurance += path_len_dist[path_len]
    avg_path_length = acc_path_length / n_path_occurance

    print ''
    print '----- Settings -----'
    print 'DS_DIR_PATH: ' + DS_DIR_PATH
    print 'MaxPathLengthLimit: ' + str(MaxPathLengthLimit)
    print "----- Statistics -----"
    print "# Freebase relation types: " + str(len(FB_rels))
    print "# textual relation types: " + str(len(SP_rels))
    print "# query relation types: " + str(len(Query_rels))
    print "# entities: " + str(len(Ents))
    print "# entity pairs: " + str(len(EntPairs))
    print "Avg. path length: " + str(avg_path_length)
    print "Max path length: " + str(max_path_length)
    print "Total # paths: " + str(len(Paths))
    print "Total # path occurance: " + str(n_path_occurance)

    with open("FB_rels.txt", 'w') as f:
        for rel in FB_rels:
            f.write(rel+"\n")
    with open("SP_rels.txt", 'w') as f:
        for rel in SP_rels:
            f.write(rel+"\n")
    with open("Entities.txt", 'w') as f:
        for ent in Ents:
            f.write(ent+"\n")


if __name__ == '__main__':
    output_statistics()