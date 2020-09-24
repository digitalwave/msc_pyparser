#!/usr/bin/env python3

import sys
import os, os.path
import yaml
import json

import msc_pyparser
from msc_pyparser import MSCUtils as u

if len(sys.argv) < 2:
    print("Argument missing!")
    print("Use: %s /path/to/parsed_struct.file" % (sys.argv[0]))
    sys.exit(-1)

srcobj = sys.argv[1]

print("Parsing CRS structure: %s" % srcobj)

dname = srcobj.replace(".yml", "_out.conf")


try:
    with open(srcobj) as file:
        if yaml.__version__ >= "5.1":
            data = yaml.load(file, Loader=yaml.FullLoader)
        else:
            data = yaml.load(file)
        # data = json.load(file)
except:
    print("Exception catched - ", sys.exc_info())
    sys.exit(-1)

try:
    mwriter = msc_pyparser.MSCWriter(data, indentstr = "\t", indentchained = False)
except:
    print(sys.exc_info()[1])
    sys.exit(-1)

#try:
if True:
    with open(dname, "w") as file:
        mwriter.generate()
        # add extra new line at the end of file
        mwriter.output.append("")
        file.write("\n".join(mwriter.output))
#except:
#    print("Exception catched - ", sys.exc_info())
#    sys.exit(-1)
