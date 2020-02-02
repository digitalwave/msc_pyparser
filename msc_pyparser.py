#
# This file is part of the msc_pyparser distribution (https://github.com/digitalwave/msc_pyparser).
# Copyright (c) 2019 digitalwave and Ervin Hegedüs.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#


import ply.lex
import ply.yacc
import re
import os

__version__ = "0.2"

class MSCLexer(object):
    """Lexer class"""

    t_secrulesecvar_ignore = ''
    t_ANY_ignore = ' \t'


    tokens = [
        'COMMENT',

        'AND',
        'PIPE',
        'COLON',
        'EXCLAMMARK',
        'QUOTED',
        'QUOTES',
        'ATSIGN',
        'BACKSLASH',
        'NUMBER',
        'COMMA',
        'EQUALMARK',
        'SEMICOLON',

        'CONFDIR_SECCOMPSIGNATURE',
        'CONFDIR_SECRULE',
        'CONFDIR_SECACTION',
        'CONFDIR_SECMARKER',
        'SECRULE_VARIABLE',
        'SECRULE_VARIABLE_ARG',

        'SECCOMPSIGNARG',

        'SECRULE_OPERATOR',
        'SECRULE_OPERATOR_ARG',
        'SECRULE_OPERATOR_ARG_NOQUOTE',

        'SECRULE_ACTION',
        'SECRULE_ACTION_ARG',
        'SECRULE_ACTION_TRANSFORMS',
        'SECRULE_ACTION_CTLACTION',
        'SECRULE_ACTION_CTLACTIONARG',
        'SECRULE_ACTION_CTLACTIONARGPARAM',
        'SECRULE_ACTION_SKIPAFTERACTIONARG',
        'SECRULE_ACTION_INITCOLACTIONARG',
        'SECRULE_ACTION_INITCOLACTIONARGPARAM',

        'SECMARKERARG',

    ]

    states = (
        ('seccompsign',                   'exclusive'),
        ('dirsecrule',                    'exclusive'),
        ('secrulesecvar',                 'exclusive'),
        ('secrulesecvararg',              'exclusive'),
        ('secrulesecop',                  'exclusive'),
        ('secrulesecoparg',               'exclusive'),
        ('secruleaction',                 'exclusive'),
        ('secruleactionarg',              'exclusive'),
        ('secruleactionargqs',            'exclusive'),
        ('secruleactiontrans',            'exclusive'),
        ('secruleactionctl',              'exclusive'),
        ('secruleactionctlargeq',         'exclusive'),
        ('secruleactionctlarg',           'exclusive'),
        ('secruleactionctlargparam',      'exclusive'),
        ('secruleactionskipafter',        'exclusive'),
        ('secruleactioninitcolarg',       'exclusive'),
        ('secruleactioninitcolargparam',  'exclusive'),

        ('secmarker',                     'exclusive'),

        ('continue',                      'inclusive'),

    )

    def __init__(self, debug = False, reflags = re.IGNORECASE | re.VERBOSE):
        self.lexer = ply.lex.lex(module=self, debug = debug, reflags = reflags)

    def t_ANY_AND(self, t):
        r'&'
        return t

    def t_dirsecrule_EXCLAMMARK(self, t):
        r'!'
        return t

    def t_secrulesecvar_EXCLAMMARK(self, t):
        r'!'
        return t

    def t_secrulesecop_EXCLAMMARK(self, t):
        r'!'
        return t

    def t_COMMENT(self, t):
        r'\#.*'
        return t

    def t_secrulesecvar_secruleaction_secruleactionarg_secruleactiontrans_secruleactionctl_secruleactioninitcolarg_secruleactionskipafter_COLON(self, t):
        r':'
        if t.lexer.lexstate == 'secrulesecvar':
            t.lexer.push_state('secrulesecvararg')
        return t

    def t_dirsecrule_secrulesecvar_PIPE(self, t):
        r'\|'
        if t.lexer.lexstate == 'secrulesecvar':
            t.lexer.pop_state()
        return t

    def t_secrulesecoparg_QUOTED(self, t):
        r'"'
        if t.lexer.lexstate == "secrulesecoparg":
            t.lexer.push_state('secruleaction')
        return t

    def t_secrulesecvararg_SECRULE_VARIABLE_ARG(self, t):
        r"([^\s|']+)|('(\.|[^'\\])*')"
        t.lexer.pop_state()
        return t

    def t_ANY_QUOTED(self, t):
        r'(?<!\\)"'
        if t.lexer.lexstate == "secrulesecoparg":
            t.lexer.push_state('secruleaction')
        elif t.lexer.lexstate == "secrulesecop":
            t.lexer.lexstate = "secrulesecoparg"
        elif t.lexer.lexstate in ["dirsecrule", "secrulesecvar"]:
            t.lexer.push_state('secrulesecop')
        return t

    def t_ANY_QUOTES(self, t):
        r"(?<!\\)'"
        if t.lexer.lexstate == "secruleactionargqs":
            t.lexer.pop_state()
            return t
        if t.lexer.lexstate == "secruleactionarg":
            t.lexer.push_state("secruleactionargqs")
        return t

    def t_ANY_ATSIGN(self, t):
        r'@'
        if t.lexer.lexstate == "secrulesecoparg":
            t.lexer.pop_state()
            t.lexer.push_state('secrulesecvar')
        return t

    def t_ANY_BACKSLASH(self, t):
        r'\\([ \t]+|\n)'
        if t.value[-1] == '\n':
            t.lexer.lineno += 1
            t.value = t.value[0]
        else:
            t.lexer.push_state('continue')

    def t_dirsecrule_secrulesecvar_secruleaction_secruleactionarg_secruleactionctlargeq_secruleactionctlargparam_secruleactionctlarg_COMMA(self, t):
        r','
        if t.lexer.lexstate == 'secrulesecvar':
            t.lexer.pop_state()
        if t.lexer.lexstate == 'secruleactionarg':
            t.lexer.pop_state()
        elif t.lexer.lexstate == 'secruleactionctlargeq':
            t.lexer.pop_state()
            t.lexer.pop_state()
        elif t.lexer.lexstate == 'secruleactionctlargparam':
            t.lexer.pop_state()
            t.lexer.pop_state()
        elif t.lexer.lexstate == 'secruleactionctlarg':
            t.lexer.pop_state()
            t.lexer.pop_state()
        return t

    def t_ANY_newline(self, t):
        r'\n'
        t.lexer.lineno += 1
        if t.lexer.lexstate == 'continue':
            t.lexer.pop_state()
        else:
            t.lexer.lexstatestack = []
            t.lexer.begin('INITIAL')

    def t_ANY_error(self, t):
        act_pos = 0
        a_data = t.lexer.lexdata.split("\n")
        pos_data = {}
        for li in range(len(a_data)):
            pos_data[li] = act_pos
            act_pos += len(a_data[li])+1
            if act_pos > t.lexer.lexpos:
                break
        aff_line = a_data[li]
        pos = t.lexer.lexpos - pos_data[li]
        output = ("Lexer error: illegal token found in line %d at pos %d, column %d\n%s\n%s^" % \
                    (li, t.lexer.lexpos, pos, aff_line, (pos * "~")))
        raise Exception(output)

    def t_CONFDIR_SECCOMPSIGNATURE(self, t):
        r'SecComponentSignature'
        t.lexer.push_state('seccompsign')
        return t

    def t_seccompsign_SECCOMPSIGNARG(self, t):
        r'[^"]{1,}'
        t.lexer.pop_state()
        return t

    def t_CONFDIR_SECRULE(self, t):
        r'SecRule'
        t.lexer.push_state('dirsecrule')
        return t

    def t_CONFDIR_SECACTION(self, t):
        r'SecAction'
        t.lexer.push_state('secruleaction')
        return t

    def t_CONFDIR_SECMARKER(self, t):
        r'SecMarker'
        t.lexer.push_state('secmarker')
        return t

    def t_dirsecrule_SECRULE_VARIABLE(self, t):
        r'(ARGS_COMBINED_SIZE|ARGS_GET_NAMES|ARGS_GET|ARGS_NAMES|ARGS_POST_NAMES|ARGS_POST|ARGS|AUTH_TYPE|DURATION|ENV|FILES_COMBINED_SIZE|FILES_NAMES|FULL_REQUEST|FULL_REQUEST_LENGTH|FILES_SIZES|FILES_TMPNAMES|FILES_TMP_CONTENT|FILES|GEO|HIGHEST_SEVERITY|INBOUND_DATA_ERROR|MATCHED_VAR_NAME|MATCHED_VARS_NAMES|MATCHED_VARS|MATCHED_VAR|MODSEC_BUILD|MULTIPART_CRLF_LF_LINES|MULTIPART_FILENAME|MULTIPART_NAME|MULTIPART_STRICT_ERROR|MULTIPART_UNMATCHED_BOUNDARY|OUTBOUND_DATA_ERROR|PATH_INFO|PERF_ALL|PERF_COMBINED|PERF_GC|PERF_LOGGING|PERF_PHASE1|PERF_PHASE2|PERF_PHASE3|PERF_PHASE4|PERF_PHASE5|PERF_RULES|PERF_SREAD|PERF_SWRITE|QUERY_STRING|REMOTE_ADDR|REMOTE_HOST|REMOTE_PORT|REMOTE_USER|REQBODY_ERROR_MSG|REQBODY_ERROR|REQBODY_PROCESSOR|REQUEST_BASENAME|REQUEST_BODY_LENGTH|REQUEST_BODY|REQUEST_COOKIES_NAMES|REQUEST_COOKIES|REQUEST_FILENAME|REQUEST_HEADERS_NAMES|REQUEST_HEADERS|REQUEST_LINE|REQUEST_METHOD|REQUEST_PROTOCOL|REQUEST_URI_RAW|REQUEST_URI|RESPONSE_BODY|RESPONSE_CONTENT_LENGTH|RESPONSE_CONTENT_TYPE|RESPONSE_HEADERS_NAMES|RESPONSE_HEADERS|RESPONSE_PROTOCOL|RESPONSE_STATUS|RULE|SCRIPT_BASENAME|SCRIPT_FILENAME|SCRIPT_GID|SCRIPT_GROUPNAME|SCRIPT_MODE|SCRIPT_UID|SCRIPT_USERNAME|SDBM_DELETE_ERROR|SERVER_ADDR|SERVER_NAME|SERVER_PORT|SESSIONID|SESSION|STATUS_LINE|STREAM_INPUT_BODY|STREAM_OUTPUT_BODY|TIME_DAY|TIME_EPOCH|TIME_HOUR|TIME_MIN|TIME_MON|TIME_SEC|TIME_WDAY|TIME_YEAR|TIME|TX|UNIQUE_ID|URLENCODED_ERROR|USERID|USERAGENT_IP|WEBAPPID|WEBSERVER_ERROR_LOG|XML|ENV|GLOBAL|IP|RESOURCE|SESSION|TX|USER)'
        if t.value in ["ARGS_GET_NAMES", "ARGS_NAMES", "ARGS_POST_NAMES", "MULTIPART_FILENAME", "MULTIPART_NAME", "REQUEST_HEADERS_NAMES", "RESPONSE_HEADERS_NAMES", "ARGS_GET", "ARGS_POST", "ARGS", "FILES_SIZES", "FILES_NAMES", "FILES_TMP_CONTENT", "MATCHED_VARS_NAMES", "MATCHED_VARS", "FILES", "REQUEST_COOKIES_NAMES", "REQUEST_HEADERS", "RESPONSE_HEADERS", "GEO", "REQUEST_COOKIES", "RULE", "FILES_TMP_NAMES", "XML", "ENV", "GLOBAL", "IP", "RESOURCE", "SESSION", "TX", "USER"]:
            t.lexer.push_state('secrulesecvar')
        return t

    def t_secrulesecvar_end(self, t):
        r'[ \n\t\|]'
        t.lexer.pop_state()

    def t_secrulesecop_SECRULE_OPERATOR(self, t):
        r'beginsWith|containsWord|contains|detectSQLi|detectXSS|endsWith|eq|fuzzyHash|geoLookup|ge|gsbLookup|gt|inspectFile|ipMatch|ipMatchF|ipMatchFromFile|le|lt|noMatch|pmFromFile|pmf|pm|rbl|rsub|rx|streq|strmatch|unconditionalMatch|validateByteRange|validateDTD|validateHash|validateSchema|validateUrlEncoding|validateUtf8Encoding|verifyCC|verifyCPF|verifySSN|within'
        t.lexer.push_state('secrulesecoparg')
        return t

    def t_secrulesecop_secrulesecoparg_SECRULE_OPERATOR_ARG(self, t):
        r'((?:[^"\\]|\\.)+)'
        return t

    def t_dirsecrule_SECRULE_OPERATOR_ARG_NOQUOTE(self, t):
        r'[^ ]+'
        t.lexer.push_state('secruleaction')
        return t

    def t_secruleaction_SECRULE_ACTION(self, t):
        r'accuracy|allow|append|auditlog|block|capture|chain|ctl|deny|deprecatevar|drop|exec|expirevar|id|initcol|logdata|log|maturity|msg|multiMatch|noauditlog|nolog|pass|pause|phase|prepend|proxy|redirect|rev|sanitiseArg|sanitiseMatched|sanitiseMatchedBytes|sanitiseRequestHeader|sanitiseResponseHeader|setenv|setrsc|setsid|setuid|setvar|severity|skipAfter|skip|status|tag|t|ver|xmlns'
        if t.value == 't':
            t.lexer.push_state('secruleactiontrans')
        elif t.value == 'ctl':
            t.lexer.push_state('secruleactionctl')
        elif t.value == 'skipAfter':
            t.lexer.push_state('secruleactionskipafter')
        elif t.value == 'initcol':
            t.lexer.push_state('secruleactioninitcolarg')
        else:
            t.lexer.push_state('secruleactionarg')
        return t

    def t_secruleactionargqs_SECRULE_ACTION_ARG(self, t):
        r"((?:\\'|[^'])+)"
        # didn't pop the stack, needs to handle at "'" - see above
        return t

    def t_secruleactionarg_SECRULE_ACTION_ARG(self, t):
        r"((?:\\'|[^,\"])+)"
        t.lexer.pop_state()
        return t

    def t_secruleactiontrans_SECRULE_ACTION_TRANSFORMS(self, t):
        r'(base64DecodeExt|base64Decode|base64Encode|cmdLine|compressWhitespace|cssDecode|escapeSeqDecode|hexDecode|hexEncode|htmlEntityDecode|jsDecode|length|lowercase|md5|none|normalisePathWin|normalisePath|normalizePathWin|normalizePath|parityEven7bit|parityOdd7bit|parityZero7bit|removeCommentsChar|removeComments|removeNulls|removeWhitespace|replaceComments|replaceNulls|sha1|sqlHexDecode|trimLeft|trimRight|trim|uppercase|urlDecodeUni|urlDecode|urlEncode|utf8toUnicode)'
        t.lexer.pop_state()
        return t

    def t_secruleactionctl_SECRULE_ACTION_CTLACTION(self, t):
        r'auditEngine|auditLogParts|debugLogLevel|forceRequestBodyVariable|hashEnforcement|hashEngine|requestBodyAccess|requestBodyLimit|requestBodyProcessor|responseBodyAccess|responseBodyLimit|ruleEngine|ruleRemoveById|ruleRemoveByMsg|ruleRemoveByTag|ruleRemoveTargetById|ruleRemoveTargetByMsg|ruleRemoveTargetByTag'
        t.lexer.push_state('secruleactionctlargeq')
        return t

    def t_secruleactionctlarg_SECRULE_ACTION_CTLACTIONARG(self, t):
        r'[^;,"]{1,}'
        return t

    def t_secruleactionctlargparam_SECRULE_ACTION_CTLACTIONARGPARAM(self, t):
        r'[^,"]{1,}'
        return t

    def t_secruleactionctlarg_SEMICOLON(self, t):
        r';'
        t.lexer.pop_state()
        t.lexer.push_state('secruleactionctlargparam')
        return t

    def t_secruleactionctlargeq_EQUALMARK(self, t):
        r'='
        t.lexer.pop_state()
        t.lexer.push_state('secruleactionctlarg')
        return t

    def t_secruleactionskipafter_SECRULE_ACTION_SKIPAFTERACTIONARG(self, t):
        r'[^,"]{1,}'
        t.lexer.pop_state()
        return t

    def t_secruleactioninitcolarg_SECRULE_ACTION_INITCOLACTIONARG(self, t):
        r'[^=]{1,}'
        t.lexer.push_state('secruleactioninitcolargparam')
        return t

    def t_secruleactioninitcolargparam_EQUALMARK(self, t):
        r'='
        return t

    def t_secruleactioninitcolargparam_SECRULE_ACTION_INITCOLACTIONARGPARAM(self, t):
        r'[^,"]{1,}'
        t.lexer.pop_state()
        t.lexer.pop_state()
        return t

    def t_secmarker_SECMARKERARG(self, t):
        r'[^"\n]{1,}'
        return t

class MSCParser(object):
    tokens = MSCLexer.tokens

    def __init__(self):
        self.lexer = MSCLexer()
        self.parser = ply.yacc.yacc(module=self)

        self.secrule = {}
        self.secaction = {}
        self.secconfdir = ""
        self.secrule_variable = ""

        self.configlines = []

    def add_comment(self, p):
        self.configlines.insert(p.lineno(1), {'type': "Comment", 'argument': p[1], 'quoted': 'no_quote', 'lineno': p.lineno(1)})

    def add_directive_quoted_argument(self, p):
        self.configlines.insert(p.lineno(1), {'type': p[1], 'argument': p[3], 'quoted': 'quoted', 'lineno': p.lineno(1)})

    def add_directive_noquoted_argument(self, p):
        self.configlines.insert(p.lineno(1), {'type': p[1], 'argument': p[2], 'quoted': 'no_quote', 'lineno': p.lineno(1)})

    def secrule_init(self, p):
        # create a dictionary to hold the current SecRule
        self.secrule = {
            'type': p[1],
            'lineno': p.lineno(1),
            'variables': [],
            'operator': "",
            'operator_argument': "",
            'actions': [],
            'chained': False
        }

    def secaction_init(self, p):
        # create a dictionary to hold the current SecAction
        self.secaction = {
            'type': p[1],
            'lineno': p.lineno(1),
            'actions': []
        }

    def p_config_line(self, p):
        """modsec_config : comment_line
                        | secrule_line
                        | seccompsignature_line
                        | secaction_line
                        | modsec_config secaction_line
                        | secmarker_line
                        | modsec_config secmarker_line
                        | modsec_config seccompsignature_line
                        | modsec_config comment_line
                        | modsec_config secrule_line"""
    def p_comment_line(self, p):
        """comment_line : COMMENT"""
        self.add_comment(p)

    ### SecCompSignature ###
    def p_seccompsignaure_line(self, p):
        """seccompsignature_line : CONFDIR_SECCOMPSIGNATURE QUOTED SECCOMPSIGNARG QUOTED"""
        self.add_directive_quoted_argument(p)

    ### End SecCompSignature ###

    ### SecAction ###

    def p_secaction_line(self, p):
        """secaction_line : tok_confdir_secaction QUOTED secaction_expr_list QUOTED"""
        self.configlines.insert(self.secaction['lineno'], self.secaction)

    def p_tok_confdir_secaction(self, p):
        """tok_confdir_secaction : CONFDIR_SECACTION"""
        self.secaction_init(p)
        self.secconfdir = "secaction"


    ### END SecAction ###

    ### SecMarker ###

    def p_secmarker_line(self, p):
        """secmarker_line  : secmarker_line_quoted
                            | secmarker_line_noquoted"""
        pass

    def p_secmarker_line_quoted(self, p):
        """secmarker_line_quoted  : CONFDIR_SECMARKER QUOTED SECMARKERARG QUOTED"""
        self.add_directive_quoted_argument(p)

    def p_secmarker_line_noquoted(self, p):
        """secmarker_line_noquoted  : CONFDIR_SECMARKER SECMARKERARG"""
        self.add_directive_noquoted_argument(p)

    ### END SecMarker ###

    ### SecRule ###

    def p_secrule_line(self, p):
        """secrule_line  : tok_confdir_secrule secvariable_expr_list QUOTED secoperator_expr QUOTED QUOTED secaction_expr_list QUOTED
                        | tok_confdir_secrule secvariable_expr_list QUOTED secoperator_expr QUOTED
                        | tok_confdir_secrule secvariable_expr_list secoperatorarg_noquote QUOTED secaction_expr_list QUOTED
                        | tok_confdir_secrule secvariable_expr_list secoperatorarg_noquote"""
        self.configlines.insert(self.secrule['lineno'], self.secrule)

    def p_tok_confdir_secrule(self, p):
        """tok_confdir_secrule : CONFDIR_SECRULE"""
        self.secrule_init(p)
        self.secconfdir = "secrule"

    def p_secvariable_expr_list(self, p):
        """secvariable_expr_list  : secvariable_expr
                                | secvariable_expr_list PIPE secvariable_expr
                                | secvariable_expr_list COMMA secvariable_expr"""
        pass

    def p_secvariable_expr(self, p):
        """secvariable_expr  : tok_secrule_variable
                            | tok_secrule_variable_prefix
                            | tok_secrule_variable_with_arg
                            | tok_secrule_variable_prefix_with_arg"""
        self.secrule['variables'].append(self.secrule_variable)
        self.secrule_variable = ""

    def p_tok_secrule_variable(self, p):
        """tok_secrule_variable : SECRULE_VARIABLE"""
        self.secrule_variable += p[1]

    def p_tok_secrule_variable_prefix(self, p):
        """tok_secrule_variable_prefix : secvariable_prefix tok_secrule_variable"""
        pass

    def p_tok_secrule_variable_with_arg(self, p):
        """tok_secrule_variable_with_arg : tok_secrule_variable tok_secrule_variable_colon secvariable_arg"""
        pass

    def p_tok_secrule_variable_prefix_with_arg(self, p):
        """tok_secrule_variable_prefix_with_arg : secvariable_prefix tok_secrule_variable tok_secrule_variable_colon secvariable_arg"""
        pass

    def p_tok_secrule_variable_colon(self, p):
        """tok_secrule_variable_colon : COLON"""
        self.secrule_variable += ":"

    def p_secvariable_prefix(self, p):
        """secvariable_prefix : AND
                              | EXCLAMMARK
                              | EXCLAMMARK AND"""
        self.secrule_variable += p[1]

    def p_secvariable_arg(self, p):
        """secvariable_arg  : tok_secrule_variable_arg
                            | tok_secrule_variable_arg_quotes"""
        pass

    def p_tok_secrule_variable_arg(self, p):
        """tok_secrule_variable_arg : SECRULE_VARIABLE_ARG"""
        self.secrule_variable += p[1]

    def p_tok_secrule_variable_arg_quotes(self, p):
        """tok_secrule_variable_arg_quotes : QUOTES SECRULE_VARIABLE_ARG QUOTES"""
        self.secrule_variable += "'" + p[2] + "'"

    def p_secoperator_expr(self, p):
        """secoperator_expr  : tok_secoperator_group
                             | tok_secoperator_group secoperator_arg_group
                             | secoperator_arg_group"""
        pass

    def p_tok_secoperator_group(self, p):
        """tok_secoperator_group : ATSIGN SECRULE_OPERATOR
                                | EXCLAMMARK ATSIGN SECRULE_OPERATOR
                                | EXCLAMMARK"""
        self.secrule['operator'] = "".join(p[1:])
        self.secrule['oplineno'] = p.lineno(1)

    def p_secoperator_arg_group(self, p):
        """secoperator_arg_group : SECRULE_OPERATOR_ARG
                                | NUMBER"""
        self.secrule['operator_argument'] = p[1]
        self.secrule['oplineno'] = p.lineno(1)

    def p_secoperatorarg_noquote(self, p):
        """secoperatorarg_noquote : SECRULE_OPERATOR_ARG_NOQUOTE"""
        self.secrule['operator_argument'] = p[1]
        self.secrule['oplineno'] = p.lineno(1)

    def p_secaction_expr_list(self, p):
        """secaction_expr_list  : secaction_expr
                                | secaction_expr_list COMMA secaction_expr"""
        pass

    def p_secaction_expr(self, p):
        """secaction_expr       : tok_secrule_action
                                | tok_secrule_action COLON secrule_action_argument
                                | tok_secrule_action COLON QUOTES secrule_action_argument_singlequoted QUOTES
                                | tok_secrule_action COLON secrule_action_argument EQUALMARK tok_secrule_action_ctlactionarg
                                | tok_secrule_action COLON secrule_action_argument EQUALMARK tok_secrule_action_ctlactionarg SEMICOLON tok_secrule_action_ctlactionargparam"""
        pass

    def p_tok_secrule_action(self, p):
        """tok_secrule_action : SECRULE_ACTION"""
        if self.secconfdir == "secrule":
            self.secrule['actions'].append({'act_name': p[1], 'lineno': p.lineno(1), 'act_quote': 'no_quote'})
            if p[1] == "chain":
                self.secrule['chained'] = True
        if self.secconfdir == "secaction":
            self.secaction['actions'].append({'act_name': p[1], 'lineno': p.lineno(1), 'act_quote': 'no_quote'})

    def p_secrule_action_argument(self, p):
        """secrule_action_argument : SECRULE_ACTION_ARG
                                | NUMBER
                                | SECRULE_ACTION_TRANSFORMS
                                | SECRULE_ACTION_CTLACTION
                                | SECRULE_ACTION_SKIPAFTERACTIONARG
                                | SECRULE_ACTION_INITCOLACTIONARG"""
        if self.secconfdir == "secrule":
            self.secrule['actions'][-1]['act_arg'] = p[1]
        if self.secconfdir == "secaction":
            self.secaction['actions'][-1]['act_arg'] = p[1]

    def p_secrule_action_argument_singlequoted(self, p):
        """secrule_action_argument_singlequoted : SECRULE_ACTION_ARG
                                                | EXCLAMMARK SECRULE_ACTION_ARG
                                                | NUMBER"""
        if self.secconfdir == "secrule":
            self.secrule['actions'][-1]['act_arg'] = p[1]
            self.secrule['actions'][-1]['act_quote'] = "quotes"
        if self.secconfdir == "secaction":
            self.secaction['actions'][-1]['act_arg'] = p[1]
            self.secaction['actions'][-1]['act_quote'] = "quotes"

    def p_tok_secrule_action_ctlactionarg(self, p):
        """tok_secrule_action_ctlactionarg : SECRULE_ACTION_CTLACTIONARG
                                        | SECRULE_ACTION_INITCOLACTIONARGPARAM"""
        if self.secconfdir == "secrule":
            self.secrule['actions'][-1]['act_ctl_arg'] = p[1]
        if self.secconfdir == "secaction":
            self.secaction['actions'][-1]['act_ctl_arg'] = p[1]

    def p_tok_secrule_action_ctlactionargparam(self, p):
        """tok_secrule_action_ctlactionargparam  : SECRULE_ACTION_CTLACTIONARGPARAM"""
        if self.secconfdir == "secrule":
            self.secrule['actions'][-1]['act_ctl_argparam'] = p[1]
        if self.secconfdir == "secaction":
            self.secaction['actions'][-1]['act_ctl_argparam'] = p[1]

    ### END SecRule ###

    def p_error(self, p):
        if p:
            act_pos = 0
            a_data = p.lexer.lexdata.split("\n")
            pos_data = {}
            for li in range(len(a_data)):
                pos_data[li] = act_pos
                act_pos += len(a_data[li])+1
                if act_pos > p.lexer.lexpos:
                    break
            aff_line = a_data[li]
            pos = p.lexer.lexpos - pos_data[li]
            output = ("Parser error: syntax error in line %d at pos %d, column %d\n%s\n%s^" % \
                    (li, p.lexer.lexpos, pos, aff_line, (pos * "~")))
            raise Exception(output)
        else:
            secrule = {}

class MSCWriter(object):
    def __init__(self, data):
        self.lineno = 1
        self.output = []
        self.chainlevel = 0
        self.ident = ""
        self.sdata = data

    # builds an action
    def make_action_arg(self, a):
        ret = ""
        if 'act_arg' not in a or a['act_arg'] is None:
            ret = "%s" % (a['act_name'])
        else:
            if a['act_quote'] == "no_quote":
                ret = "%s:%s" % (a['act_name'], str(a['act_arg']))
            elif a['act_quote'] == "quotes":
                ret = "%s:'%s'" % (a['act_name'], str(a['act_arg']))
            elif a['act_quote'] == "quoted":
                ret = "%s:\"%s\"" % (a['act_name'], str(a['act_arg']))
            if 'act_ctl_arg' in a:
                ret += ("=%s" % (a['act_ctl_arg']))
            if 'act_ctl_argparam' in a:
                ret += (";%s" % (a['act_ctl_argparam']))
        return ret

    # iterates the actions list, call the make_action_arg if required
    # set the correct indent with help of current chain level
    def make_actions(self, r):
        if len(r['actions']) == 0:
            self.chainlevel = 0
            self.ident = ""
            return ""
        actionsarr = []
        a = r['actions'][0]

        if self.lineno < a['lineno']:
            self.ident = (self.chainlevel+1)*"    "
            joiner = ",\\\n" + self.ident
            self.lineno = a['lineno']
            actpref = " \\\n" + self.ident + "\""
        else:
            self.ident = ""
            joiner = ","
            actpref = " \""
   
        ai = 0
        currline = []
        lasta = None
        for a in r['actions']:
            actstr = self.make_action_arg(a)
            if ai == 0:
                actstr = actpref + actstr
            if ai == len(r['actions'])-1:
                actstr += "\""
            if lasta is None or lasta['lineno'] < a['lineno']:
                if len(currline) > 0:
                    actionsarr.append(",".join(currline))
                    currline = []
                if lasta is not None and lasta['lineno'] < a['lineno']:
                    self.ident = (self.chainlevel+1)*"    "
                    joiner = ",\\\n" + self.ident
            currline.append(actstr)
            lasta = a.copy()
            self.lineno = a['lineno']
            ai += 1
        if len(currline) > 0:
            actionsarr.append(",".join(currline))

        if 'chained' in r and r['chained'] == True:
            self.chainlevel += 1
        else:
            self.chainlevel = 0
            self.ident = ""

        return joiner.join(actionsarr)

    # create a SecRule block, this calls the make_actions
    def make_secrule(self, r):
        opargs = []
        for o in [r['operator'], r['operator_argument']]:
            if o != "":
                opargs.append(o)
        oppref = " "
        if r['lineno'] < r['oplineno']:
            oppref = " \\\n%s" % ((self.chainlevel+1)*"    ")
        opgroups = "%s\"%s\"" % (oppref, " ".join(opargs))
        secrule = ["%sSecRule %s%s" % ((self.chainlevel)*"    ", "|".join(r['variables']), opgroups)]
        secrule.append(self.make_actions(r))
        self.output.append("".join(secrule))

    def make_secaction(self, r):
        secrule = ["SecAction"]
        secrule.append(self.make_actions(r))
        self.output.append("".join(secrule))

    # the main cycle
    def generate(self):
        for i in self.sdata:
            while self.lineno < i['lineno']:
                self.output.append("")
                self.lineno += 1
            if i['type'] == "Comment":
                self.output.append("%s" % (i['argument']))
                self.lineno = i['lineno']+1
            elif i['type'] == "SecRule":
                self.make_secrule(i)
                self.lineno += 1
            elif i['type'] == "SecAction":
                self.make_secaction(i)
                self.lineno += 1
            elif i['type'] == "SecComponentSignature":
                self.output.append("SecComponentSignature \"%s\"" % (i['argument']))
                self.lineno = i['lineno']+1
            elif i['type'] == "SecMarker":
                self.output.append("SecMarker \"%s\"" % (i['argument']))
                self.lineno = i['lineno']+1

class MSCUtils(object):

    UNKNOWN = -1
    IS_FILE =  1
    IS_DIR  =  2

    def __init__(self):
        pass

    @staticmethod
    def getpathtype(path):
        u = MSCUtils()
        if os.path.isdir(path):
            return u.IS_DIR
        elif os.path.isfile(path):
            return u.IS_FILE
        return u.UNKNOWN
