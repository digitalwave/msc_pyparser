#!/usr/bin/python3

import sys
import yaml

class Transform(object):
    def __init__(self, data):
        self.data = data
        self.lineno = 1
        self.lineno_shift = 0

    def inserttag(self):
        for d in self.data:
            d['lineno'] += self.lineno_shift
            if "oplineno" in d:
                d['oplineno'] += self.lineno_shift
            if "actions" in d:
                aidx = 0
                while aidx < len(d['actions']):
                    a = d['actions'][aidx]
                    if a['act_name'] == "tag" and a['act_arg'] == "OWASP_CRS":
                        newtag = {'act_arg': "OWASP_CRS_NEW", 'act_name': "tag", 'act_quote': "quotes", 'lineno': a['lineno']+self.lineno_shift}
                        d['actions'].insert(aidx, newtag)
                        self.lineno_shift += 1
                        aidx += 1
                    a['lineno'] += self.lineno_shift
                    aidx += 1

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
    t.inserttag()

    try:
        with open(oname, 'w') as outfile:
            outfile.write(yaml.dump(t.data))
        print("Transformed file written.")
    except:
        print("Can't open file: %s" % (oname))
        sys.exit()
