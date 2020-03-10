#!/usr/bin/env python3

import yaml
import sys
from msc_pyparser import MSCUtils as u
import os
import re

class Check(object):
    def __init__(self, src, data):
        self.source = src
        self.data = data
        self.current_ruleid = 0
        self.last_ruleid = 0
        self.curr_lineno = 0
        self.chained = False
        self.chainlevel = 0
        self.re_patt = re.compile("tx.anomaly_score_")
        self.lineno_shift = 0
        self.dataidx = 0
        self.file_modified = False

    def initialize_variable(self, ruleid):
        """
          this function puts a SecRule to the end of the current rule set (specially REQUEST-901-INITIALIZATION)
          argument is the ruleid - that's what can change in a different version

          the result will be:

          ==%==
          # Default ID list of anomaly scoring rules
          SecRule &TX:anomaly_scoring_rules "@eq 0" \
              "id:901170,\
              phase:1,\
              pass,\
              nolog,\
              setvar:'tx.anomaly_scoring_rules= '"
          ==%==
          look at the extra space at the end of setvar!
        
        """
        self.lineno_shift += 2
        l = {'argument': '# Default ID list of anomaly scoring rules', 'lineno': self.curr_lineno + self.lineno_shift, 'quoted': 'no_quote', 'type': 'Comment'}
        self.data.append(l)
        self.dataidx += 1
        self.lineno_shift += 1
        l = {
            'type': 'SecRule',
            'chained': False,
            'lineno': self.curr_lineno + self.lineno_shift,
            'variables': ['&TX:anomaly_scoring_rules'],
            'operator': '@eq',
            'operator_argument': '0',
            'oplineno': self.curr_lineno + self.lineno_shift,
            'actions': [
                { 'act_name': 'id', 'act_arg': '%s' % (ruleid), 'act_quote': 'no_quote', 'lineno': self.curr_lineno + self.lineno_shift + 1 },
                { 'act_name': 'phase', 'act_arg': '1',  'act_quote': 'no_quote', 'lineno': self.curr_lineno + self.lineno_shift + 2 },
                { 'act_name': 'pass',  'act_arg': None,   'act_quote': 'no_quote', 'lineno': self.curr_lineno + self.lineno_shift + 3 },
                { 'act_name': 'nolog', 'act_arg': None,   'act_quote': 'no_quote', 'lineno': self.curr_lineno + self.lineno_shift + 4 },
                { 'act_name': 'setvar', 'act_arg': 'tx.anomaly_scoring_rules= ', 'act_quote': 'quotes', 'lineno': self.curr_lineno + self.lineno_shift + 5 }
            ]
        }
        self.data.append(l)

    def check_action(self, coll_defined = False):
        """
          this function iterates over a rule set
          if the item is a SecRule object, get the rule id
          if the list of actions contains the setvar with "tx.anomaly_score_...", then
          inserts a new setvar action with value
            tx.anomaly_scoring_rules=%%{tx.anomaly_scoring_rules} CURRENT_RULE_ID
          this will result when the rule will logged, the log can contains the msg:
            list of triggered rules: RULE1 ... RULE_N
        """
        for d in self.data:
            d['lineno'] += self.lineno_shift
            if "oplineno" in d:
                d['oplineno'] += self.lineno_shift
            if "actions" in d:
                act_idx = 0
                if self.chained == True:
                    self.chained = False
                while act_idx < len(d['actions']):
                    a = d['actions'][act_idx]

                    self.curr_lineno = a['lineno']
                    if a['act_name'] == "id":
                        self.current_ruleid = int(a['act_arg'])

                    if a['act_name'] == "chain":
                        self.chained = True
                        self.chainlevel += 1

                    if a['act_name'] == "setvar":
                        if self.re_patt.search(a['act_arg']):
                            if coll_defined == True:
                                newact = {
                                    'act_name': "setvar", 
                                    'act_arg': "tx.anomaly_scoring_rules=%%{tx.anomaly_scoring_rules} %s" % (self.current_ruleid),
                                    'act_quote': "quotes",
                                    'lineno': a['lineno']+self.lineno_shift+1
                                }
                                d['actions'].insert(act_idx, newact)
                                act_idx += 1
                                self.lineno_shift += 2
                                self.file_modified = True

                    if a['act_name'] == "msg":
                        if re.search("tx\.anomaly\_score", a['act_arg'], re.I):
                            a['act_arg'] += ", list of triggered rules: %{tx.anomaly_scoring_rules}"

                    a['lineno'] += self.lineno_shift
                    act_idx += 1

                # end of (chained) rule
                if self.chained == False:
                    self.current_ruleid = 0
            self.dataidx += 1

if __name__ == "__main__":

    if len(sys.argv) < 4:
        print("Argument missing!")
        print("Use: %s /path/to/exported/dir /path/to/modified/dir RULEID" % (sys.argv[0]))
        sys.exit(-1)

    srcobj = sys.argv[1]
    dstobj = sys.argv[2]
    ruleid = sys.argv[3]

    st = u.getpathtype(srcobj)
    if st == u.UNKNOWN:
        print("Unknown source path!")
        sys.exit()

    dt = u.getpathtype(dstobj)
    if dt == u.UNKNOWN:
        print("Unknown dest path!")
        sys.exit()

    configs = []
    if st == u.IS_DIR:
        for f in os.listdir(srcobj):
            fp = os.path.join(srcobj, f)
            if os.path.isfile(fp) and os.path.basename(fp)[-5:] == ".yaml":
                configs.append(fp)
    if st == u.IS_FILE:
        configs.append(srcobj)

    configs.sort()
    collection_defined = False

    for c in configs:
        try:
            with open(c) as file:
                print("Reading file: %s" % c)
                if yaml.__version__ >= "5.1":
                    data = yaml.load(file, Loader=yaml.FullLoader)
                else:
                    data = yaml.load(file)
        except:
            print("Exception catched - ", sys.exc_info())
            sys.exit(-1)

        chk = Check(c.replace(".yaml", "").replace(srcobj, ""), data)
        chk.check_action(collection_defined)
        if c.replace(".yaml", "").split("/")[-1] == "REQUEST-901-INITIALIZATION":
            chk.initialize_variable(ruleid)
            collection_defined = True

        dpath = os.path.join(dstobj, c.split("/")[-1])
        try:
            with open(dpath, 'w') as file:
                file.write(yaml.dump(chk.data))
        except:
            print("Exception catched - ", sys.exc_info())
            sys.exit(-1)
