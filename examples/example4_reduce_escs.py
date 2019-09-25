#!/usr/bin/python3

import sys
import yaml

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

    fname = sys.argv[1]
    oname = sys.argv[2]
    try:
        with open(fname, 'r') as inputfile:
            data = inputfile.read()
    except:
        print("Can't open file: %s" % (fname))
        sys.exit()

    t = Transform(yaml.load(data, Loader = yaml.FullLoader))
    t.stripescape()

    try:
        with open(oname, 'w') as outfile:
            outfile.write(yaml.dump(t.data))
        print("Transformed file written.")
    except:
        print("Can't open file: %s" % (oname))
        sys.exit()
