#!/usr/bin/python3

import yaml
import sys


class Check(object):
    def __init__(self, data):

        self.actions = [
            "id",
            "phase",
            "allow",
            "block",
            "deny",
            "drop",
            "pass",
            "proxy",
            "redirect",
            "status",
            "capture",
            "t",
            "log",
            "nolog",
            "auditlog",
            "noauditlog",
            "msg",
            "logdata",
            "tag",
            "sanitiseArg",
            "sanitiseRequestHeader",
            "sanitiseMatched",
            "sanitiseMatchedBytes",
            "ctl",
            "ver",
            "severity",
            "multiMatch",
            "initcol",
            "setenv",
            "setvar",
            "expirevar",
            "chain",
            "skip",
            "skipAfter",
        ]

        self.data = data
        self.current_ruleid = 0
        self.curr_lineno = 0
        self.chained = False
        self.orderacts = []

    def check_ignore_case(self):
        for d in self.data:
            if "actions" in d:
                aidx = 0
                max_order = 0
                if self.chained == False:
                    self.current_ruleid = 0
                else:
                    self.chained = False

                while aidx < len(d['actions']):
                    a = d['actions'][aidx]

                    self.curr_lineno = a['lineno']
                    if a['act_name'] == "id":
                        self.current_ruleid = int(a['act_arg'])

                    if a['act_name'] == "chain":
                        self.chained = True

                    try:
                        act_idx = self.actions.index(a['act_name'])
                    except ValueError:
                        print("ERROR: '%s' not in actions list!" % (a['act_name']))
                        sys.exit(-1)

                    if act_idx >= max_order:
                        max_order = act_idx
                    else:
                        if self.actions.index(prevact) > act_idx:
                            self.orderacts.append([0, prevact, pidx, a['act_name'], aidx])
                    prevact = a['act_name']
                    pidx = aidx
                    aidx += 1
                for a in self.orderacts:
                    if a[0] == 0:
                        a[0] = self.current_ruleid

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Argument missing!")
        print("Use: %s input_to_check" % (sys.argv[0]))
        sys.exit(-1)

    fname = sys.argv[1]
    try:
        with open(fname, 'r') as inputfile:
            data = inputfile.read()
    except:
        print("Can't open file: %s" % (fname))
        sys.exit()

    c = Check(yaml.load(data, Loader = yaml.FullLoader))
    c.check_ignore_case()
    for a in c.orderacts:
        print("Rule ID: {}, action '{}' at pos {} is wrong place against '{}' at pos {}".format(*a))


