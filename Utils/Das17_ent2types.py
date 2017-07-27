# -*- coding: utf-8 -*-

import gzip
import json

ip_file = gzip.open('C:/Users/xiaotian/Desktop/entity_to_list_type.json.gz')
op_dir = 'C:/Users/xiaotian/Desktop/entity2types/'
e2ts = json.loads(ip_file.readline())
n2file = {}

print len(e2ts)

ip_file.close()

for e,ts in e2ts.iteritems():
    nts =  len(ts)
    if not n2file.has_key(nts):
        n2file[nts] = open(op_dir+str(nts), 'w')
    f = n2file[nts]
    f.write("{0}:  {1}\n".format(e, "  ".join(ts)))

for fl in n2file.values():
    fl.close()


if __name__ == '__main__':
    pass