#!/usr/bin/env python3

import yaml
import sys
import os

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
            t.beautify()
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
