#!/usr/bin/env python3

import sys
import yaml
import os.path

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
                        newtag = {'act_arg': "OWASP_CRS_NEW", 'act_name': "tag", 'act_quote': "quotes", 'lineno': a['lineno']+self.lineno_shift, 'act_arg_val': "", 'act_arg_val_param': "",'act_arg_val_param_val': ""}
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
            t.inserttag()
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
