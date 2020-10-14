#!/usr/bin/python3

import yaml
import json
import glob
import msc_pyparser
import sys
import os

if len(sys.argv) < 2:
    print("Argument missing")
    sys.exit(1)

def read_file(inp):
    try:
        with open(inp, 'r') as inputfile:
            data = inputfile.read()
    except:
        print("Can't open file: %s" % inp)
        print(sys.exc_info())
        sys.exit(1)
    return data

def parse_file(fname):
    content = read_file(fname)
    try:
        mparser = msc_pyparser.MSCParser()
        mparser.parser.parse(content)
    except:
        print("Can't parse data")
        print(sys.exc_info())
        sys.exit(1)
    return mparser.configlines

def expand_path(fname):
    dname = os.path.dirname(fname)
    fname = os.path.basename(fname)

    if os.path.isdir(dname):
        absdir = dname
    else:
        absdir = "./"

    return os.path.join(absdir, fname)

configs = {}
includes = []

includes.append(expand_path(sys.argv[1]))

for i in includes:
    print(i)
    configs[i] = parse_file(i)
    for d in configs[i]:
        if d['type'].lower() == "include":
            for f in glob.glob(d['arguments'][0]['argument']):
                if f[0] != "/":
                    dname = os.path.dirname(i)
                    f = os.path.join(dname, f)
                includes.append(f)

#print(configs)
fp = open("output.json", "w")
fp.write(json.dumps(configs, indent=4))
fp.close()
