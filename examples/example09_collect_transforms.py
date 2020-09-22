#!/usr/bin/env python3

import yaml
import sys
from msc_pyparser import MSCUtils as u
import os

class Check(object):
    def __init__(self, src, data):
        self.source = src
        self.data = data
        self.current_ruleid = 0
        self.curr_lineno = 0
        self.chained = False
        self.chainlevel = 0
        self.transforms = "base64DecodeExt|base64Decode|base64Encode|cmdLine|compressWhitespace|cssDecode|escapeSeqDecode|hexDecode|hexEncode|htmlEntityDecode|jsDecode|length|lowercase|md5|none|normalisePathWin|normalisePath|normalizePathWin|normalizePath|parityEven7bit|parityOdd7bit|parityZero7bit|removeCommentsChar|removeComments|removeNulls|removeWhitespace|replaceComments|replaceNulls|sha1|sqlHexDecode|trimLeft|trimRight|trim|uppercase|urlDecodeUni|urlDecode|urlEncode|utf8toUnicode".split("|")
        self.transformsl = [t.lower() for t in self.transforms]

    def collect(self):
        # create a dict with keys name of transforms, values are empty lists
        transforms = {tname: [] for tname in self.transformsl}
        for d in self.data:
            if "actions" in d:
                aidx = 0
                if self.chained == True:
                    self.chained = False
                while aidx < len(d['actions']):
                    a = d['actions'][aidx]

                    self.curr_lineno = a['lineno']
                    if a['act_name'] == "id":
                        self.current_ruleid = int(a['act_arg'])

                    if a['act_name'] == "chain":
                        self.chained = True
                        self.chainlevel += 1

                    if a['act_name'] == "t":
                        # check the transformation is valid
                        if a['act_arg'].lower() not in self.transformsl:
                            print("Invalid transformation")
                        else:
                            transforms[a['act_arg'].lower()].append(str(self.chainlevel))
                    aidx += 1

                # need to check only if there is an action at least
                # check if the rules are chained or not, if it is, then
                # need to handle them as one
                if self.chained == False:
                    print("%s;%s;%d;%d;%s" % (self.source, d['type'], self.current_ruleid, self.chainlevel, ";".join([",".join([str(tr) for tr in transforms[tk]]) for tk in self.transformsl])))
                    self.current_ruleid = 0
                    self.chained = False
                    self.chainlevel = 0
                    transforms = {tname: [] for tname in self.transformsl}

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Argument missing!")
        print("Use: %s /path/to/exported/dir" % (sys.argv[0]))
        sys.exit(-1)

    flist = sys.argv[1:]
    if len(flist) == 0:
        print("No such file or directory: %s" % (sys.argv[1:-1]))
    else:
        for fname in flist:
            try:
                with open(fname, 'r') as inputfile:
                    data = inputfile.read()
            except:
                print("Can't open file: %s" % (fname))
                sys.exit()

            c = Check(fname, yaml.load(data, Loader = yaml.FullLoader))
            c.collect()
