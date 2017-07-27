import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i',"--input_dir", required=True, help="input dir that contains cs file")
args = parser.parse_args()
input_dir = args.input_dir

optim_test_aps=[]
for rel in os.listdir(input_dir):
    if not rel.startswith("_"):
        continue
    with open("{0}/{1}".format(input_dir, rel)) as cvalues_file:
        c_values = []
        dev_aps = []
        test_aps = []
        for i, line in enumerate(cvalues_file.readlines()):
            try:
                if i%3 == 0:
                    c_values.append(float(line.split(", AP on dev, test ")[0].split("C=")[1]))
                elif i%3 == 1:
                    dev_aps.append(float(line.split("\t Path:")[0].split("AP: ")[1]))
                elif i%3 == 2:
                    test_aps.append(float(line.split("\t Path:")[0].split("AP: ")[1]))
                else:
                    raise ValueError
            except:
                print 'line: ' + str(line)
                print 'file: ' + str(rel)
                raise NotImplementedError
        idx=dev_aps.index(max(dev_aps))
        print ("Select: C={0} , Get: dev_ap={1}, test_ap={2} , For Relation {3}".format(
            c_values[idx], dev_aps[idx], test_aps[idx], rel))
        optim_test_aps.append(test_aps[idx])

print "MAP={0}".format(sum(optim_test_aps)/len(optim_test_aps))

