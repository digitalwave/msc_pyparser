#!/usr/bin/env python3

import yaml
import sys


class Transform(object):
    def __init__(self, data):
        self.data = data
        self.lineno = 0
 
    def beautify(self):
        writed_trans = 0
        for d in self.data:
            if d['type'] == "SecRule":
                # empty line before the rule
                self.lineno += 1
                d['oplineno'] = self.lineno
                d['lineno'] = self.lineno
                if "actions" in d:
                    aidx = 0
                    last_trans = ""
                    while aidx < len(d["actions"]):
                        if d['actions'][aidx]['act_name'] == "t":
                            # writed_trans could be used to limit the number of actions
                            # to place in one line
                            writed_trans += 1
                            if last_trans == "t":
                                pass
                            else:
                                self.lineno += 1
                        else:
                            self.lineno += 1
                            writed_trans = 0
                        d['actions'][aidx]['lineno'] = self.lineno
                        last_trans = d['actions'][aidx]['act_name']
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

    t = Transform(yaml.load(data))
    t.beautify()

    try:
        with open(oname, 'w') as outfile:
            outfile.write(yaml.dump(t.data))
        print("Transformed file written.")
    except:
        print("Can't open file: %s" % (oname))
        sys.exit()