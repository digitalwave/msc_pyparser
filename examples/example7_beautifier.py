#!/usr/bin/python3

import yaml
import sys


class Transform(object):
    def __init__(self, data):
        self.data = data
        self.lineno = 0
 
    def beautify(self):
        for d in self.data:
            if d['type'] == "SecRule":
                # empty line before the rule
                self.lineno += 1
                d['oplineno'] = self.lineno
                d['lineno'] = self.lineno
                if "actions" in d:
                    aidx = 0
                    while aidx < len(d["actions"]):
                        d['actions'][aidx]['lineno'] =  self.lineno
                        self.lineno += 1
                        aidx += 1
                # empty line after the rule
                self.lineno += 1
            else:
                d['lineno'] = self.lineno
                self.lineno += 1


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Argument missing!")
        print("Use: %s input output" % (sys.argv[0]))
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
    t.beautify()

    try:
        with open(oname, 'w') as outfile:
            outfile.write(yaml.dump(t.data))
        print("Transformed file written.")
    except:
        print("Can't open file: %s" % (oname))
        sys.exit()