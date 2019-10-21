#!/usr/bin/env python3

import yaml
import sys


class Check(object):
    def __init__(self, data):

        self.operators = "beginsWith|containsWord|contains|detectSQLi|detectXSS|endsWith|eq|fuzzyHash|geoLookup|ge|gsbLookup|gt|inspectFile|ipMatch|ipMatchF|ipMatchFromFile|le|lt|noMatch|pmFromFile|pmf|pm|rbl|rsub|rx|streq|strmatch|unconditionalMatch|validateByteRange|validateDTD|validateHash|validateSchema|validateUrlEncoding|validateUtf8Encoding|verifyCC|verifyCPF|verifySSN|within".split("|")
        self.operatorsl = [o.lower() for o in self.operators]
        self.actions = "accuracy|allow|append|auditlog|block|capture|chain|ctl|deny|deprecatevar|drop|exec|expirevar|id|initcol|logdata|log|maturity|msg|multiMatch|noauditlog|nolog|pass|pause|phase|prepend|proxy|redirect|rev|sanitiseArg|sanitiseMatched|sanitiseMatchedBytes|sanitiseRequestHeader|sanitiseResponseHeader|setenv|setrsc|setsid|setuid|setvar|severity|skipAfter|skip|status|tag|t|ver|xmlns".split("|")
        self.actionsl = [a.lower() for a in self.actions]
        self.transforms = "base64DecodeExt|base64Decode|base64Encode|cmdLine|compressWhitespace|cssDecode|escapeSeqDecode|hexDecode|hexEncode|htmlEntityDecode|jsDecode|length|lowercase|md5|none|normalisePathWin|normalisePath|normalizePathWin|normalizePath|parityEven7bit|parityOdd7bit|parityZero7bit|removeCommentsChar|removeComments|removeNulls|removeWhitespace|replaceComments|replaceNulls|sha1|sqlHexDecode|trimLeft|trimRight|trim|uppercase|urlDecodeUni|urlDecode|urlEncode|utf8toUnicode".split("|")
        self.transformsl = [t.lower() for t in self.transforms]
        self.ctls = "auditEngine|auditLogParts|debugLogLevel|forceRequestBodyVariable|hashEnforcement|hashEngine|requestBodyAccess|requestBodyLimit|requestBodyProcessor|responseBodyAccess|responseBodyLimit|ruleEngine|ruleRemoveById|ruleRemoveByMsg|ruleRemoveByTag|ruleRemoveTargetById|ruleRemoveTargetByMsg|ruleRemoveTargetByTag".split("|")
        self.ctlsl = [c.lower() for c in self.ctls]

        self.data = data
        self.current_ruleid = 0
        self.curr_lineno = 0
        self.chained = False

    def show_error(self, prefix, actstr):
        if self.current_ruleid > 0:
            pval = self.current_ruleid
            ptype = "rule id"
        else:
            pval = self.curr_lineno
            ptype = "line"
        print("%s in %s %d: '%s'" % (prefix, ptype, pval, actstr))

    def check_ignore_case(self):
        for d in self.data:
            if "actions" in d:
                aidx = 0
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

                    if a['act_name'].lower() not in self.actionsl:
                        self.show_error("Invalid action", a['act_name'])
                    if self.actions[self.actionsl.index(a['act_name'].lower())] != a['act_name']:
                        self.show_error("Action case mismatch", a['act_name'])
                    if a['act_name'] == 'ctl':
                        if a['act_arg'].lower() not in self.ctlsl:
                            self.show_error("Invalid ctl", a['act_arg'])
                        if self.ctls[self.ctlsl.index(a['act_arg'].lower())] != a['act_arg']:
                            self.show_error("Ctl case mismatch", a['act_arg'])
                    if a['act_name'] == 't':
                        if a['act_arg'].lower() not in self.transformsl:
                            self.show_error("Invalid transform", a['act_arg'])
                        if self.transforms[self.transformsl.index(a['act_arg'].lower())] != a['act_arg']:
                            self.show_error("Transform case mismatch", a['act_arg'])
                    aidx += 1
            if "operator" in d and d["operator"] != "":
                self.curr_lineno = d['oplineno']
                op = d['operator'].replace("!", "").replace("@", "")
                if op.lower() not in self.operatorsl:
                    self.show_error("Invalid operator", d['operator'])
                if self.operators[self.operatorsl.index(op.lower())] != op:
                    self.show_error("Operator case mismatch", d['operator'])

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


