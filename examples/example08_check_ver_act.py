#!/usr/bin/env python3

import yaml
import sys
import os

class Check(object):
    def __init__(self, src, data):
        self.source = src
        self.data = data
        self.current_ruleid = 0
        self.curr_lineno = 0
        self.chained = False
        self.chainlevel = 0

    def check_ver_act(self):
        for d in self.data:
            if "actions" in d:
                check_actions = True
                aidx = 0
                has_ver = False
                ver_value = ""
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

                    if a['act_name'] == "ver":
                        has_ver = True
                        ver_value = a['act_arg']
                    aidx += 1

                # need to check only if there is an action at least
                # check if the rules are chained or not, if it is, then
                # need to handle them as one
                if self.chained == False:
                    is_ver = "no"
                    if has_ver == True:
                        is_ver = "yes"
                    print("%s;%s;%d;%d;%s;%s" % (self.source, d['type'], self.current_ruleid, self.chainlevel, is_ver, ver_value))
                    self.current_ruleid = 0
                    self.chained = False
                    self.chainlevel = 0

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
            c.check_ver_act()
