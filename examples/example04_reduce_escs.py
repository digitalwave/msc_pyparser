#!/usr/bin/env python3

import sys
import yaml
import os

class Transform(object):
    def __init__(self, data):
        self.lineno = 1
        self.data = data

    def stripescape(self):
        for d in self.data:
            if "operator_argument" in d:
                d['operator_argument'] = d['operator_argument'].replace("\\\\", "\\")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Argument missing!")
        print("This script converts the '\\\\\\\\' to '\\\\' in rule 941330")
        print("Use: %s REQUEST-941-APPLICATION-ATTACK-XSS.yml output" % (sys.argv[0]))
        sys.exit(-1)



if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Argument missing!")
        print("Use: %s input output" % (sys.argv[0]))
        sys.exit(-1)

    iname = sys.argv[1]
    oname = sys.argv[-1]
    if os.path.isdir(oname):
        otype = "dir"
    else:
        otype = "file"
    flist = sys.argv[1:-1]
    if len(flist) == 0:
        print("No such file or directory: %s" % (iname))
    else:
        for fname in flist:
            print(fname)
            try:
                with open(fname, 'r') as inputfile:
                    if yaml.__version__ >= "5.1":
                        data = yaml.load(inputfile, Loader=yaml.FullLoader)
                    else:
                        data = yaml.load(inputfile)
            except:
                print("Can't open file: %s" % (fname))
                sys.exit()

            t = Transform(data)
            t.stripescape()
            if otype == "dir":
                ofile = os.path.join(oname, os.path.basename(fname))
            else:
                ofile = oname
            try:
                with open(ofile, 'w') as outfile:
                    outfile.write(yaml.dump(t.data))
                print("Transformed file written.")
            except:
                print("Can't open file: %s" % (oname))
                sys.exit()
