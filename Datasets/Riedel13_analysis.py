# -*- coding: utf-8 -*-



def gen_KB_SP_triples_from_trainingset():
    # trainingset = "C:/Users/xiaotian/Desktop/Uschema/nyt-freebase.train.triples.universal.txt"
    trainingset = "C:/Users/xiaotian/Desktop/t1"
    op_path = trainingset+".out"
    with open(trainingset) as ip_file, open(op_path, 'w') as op_file:
        for line in ip_file:
            parts = line.strip().split('\t')
            e1 = parts[1]
            e2 = parts[2]
            rels = filter(lambda x: x.startswith("REL$/") or x.startswith("path#"), parts)
            for rel in rels:
                op_file.write("{0}\t{1}\t{2}\n".format(e1,rel,e2))


if __name__ == '__main__':
    gen_KB_SP_triples_from_trainingset()