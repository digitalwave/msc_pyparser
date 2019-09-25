#!/usr/bin/python3

import sys
import os
import yaml
import msc_pyparser

if len(sys.argv) < 2:
    print("Argument missing!")
    print("Use: %s secrule.conf" % sys.argv[0])
    sys.exit(-1)

conffile = sys.argv[1]
if len(sys.argv) > 2:
    outputdir = sys.argv[2]
else:
    outputdir = "/".join(conffile.split("/")[:-1])

pdebug = False
if len(sys.argv) > 2:
    if sys.argv[2] == "debug":
        pdebug = True

print("Config: %s" % conffile)

with open(conffile) as file:
   data = file.read()

# not needed!
#lexer = ply.lex.lex(debug = pdebug, reflags = re.IGNORECASE | re.VERBOSE)
#lexer.input(data)

mparser = msc_pyparser.MSCParser()

try:
    mparser.parser.parse(data, debug = pdebug)
except:
    print(sys.exc_info()[1])
    sys.exit(-1)

outfile = conffile.split("/")[-1].replace(".conf", ".yml")

if pdebug == False:
    print(outputdir)
    print(os.path.join(outputdir, outfile))

    fp = open(os.path.join(outputdir, outfile), "w")
    yaml.dump(mparser.configlines, fp, default_flow_style=False)
    #print(parser.configlines)
    fp.close()
    #print(configlines)