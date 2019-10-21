#!/usr/bin/env python3

import sys
import os, os.path
import yaml
import json

import msc_pyparser
from msc_pyparser import MSCUtils as u

if len(sys.argv) < 3:
    print("Argument missing!")
    print("Use: %s /path/to/crs/confdir /path/to/export/struct" % (sys.argv[0]))
    sys.exit(-1)

srcobj = sys.argv[1]
dstobj = sys.argv[2]

dt = u.getpathtype(dstobj)
if dt == u.UNKNOWN:
    print("Unknown dest path!")
    sys.exit(-1)
if dt == u.IS_FILE:
    print("Dest path is file!")
    sys.exit(-1)

st = u.getpathtype(srcobj)
if st == u.UNKNOWN:
    print("Unknown source path!")
    sys.exit()

configs = []
if st == u.IS_DIR:
    for f in os.listdir(srcobj):
        fp = os.path.join(srcobj, f)
        if os.path.isfile(fp) and os.path.basename(fp)[-5:] == ".conf":
            configs.append(fp)
if st == u.IS_FILE:
    configs.append(srcobj)

configs.sort()

for c in configs:
    print("Parsing CRS config: %s" % c)
    cname = os.path.basename(c)
    dname = cname.replace(".conf", ".yaml")
    #dname = cname.replace(".conf", ".json")

    try:
        with open(c) as file:
            data = file.read()
    except:
        print("Exception catched - ", sys.exc_info())
        sys.exit(-1)

    try:
        mparser = msc_pyparser.MSCParser()
        mparser.parser.parse(data)
    except:
        print(sys.exc_info()[1])
        sys.exit(-1)

    o = os.path.join(dstobj, dname)
    try:
        with open(o, "w") as file:
            yaml.dump(mparser.configlines, file, default_flow_style=False)
            #json.dump(mparser.configlines, file, indent = 4, sort_keys = True)
    except:
        print("Exception catched - ", sys.exc_info())
        sys.exit(-1)
