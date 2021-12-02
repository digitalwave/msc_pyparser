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

import sys
import ply.lex
import ply.yacc
import re
import os
import os.path
import glob

__version__ = "1.1"

class MSCLexer(object):
    """Lexer class"""

    t_STCOMMENT_ignore = ''
    t_STSECRULEVARIABLE_ignore = ''
    t_ANY_ignore = ' \t'

    tokens = [

        'T_COMMENT',

        'T_EXCLUSION_MARK',

        'T_CONFIG_DIRECTIVE',
        'T_CONFIG_DIRECTIVE_ARGUMENT_NOTQUOTE',
        'T_CONFIG_DIRECTIVE_ARGUMENT_QUOTE_DOUBLE',
        'T_CONFIG_DIRECTIVE_ARGUMENT_QUOTE_SINGLE',
        'T_CONFIG_DIRECTIVE_SECRULE',
        'T_CONFIG_DIRECTIVE_SECACTION',
        'T_INCLUDE_DIRECTIVE',
        'T_INCLUDE_DIRECTIVE_ARGUMENT',
        'T_INCLUDE_DIRECTIVE_ARGUMENT_QUOTED',

        'T_APACHE_LOCATION_DIRECTIVE',

        'T_SECRULE_VARIABLE',
        'T_SECRULE_VARIABLE_COUNTER',
        'T_SECRULE_VARIABLE_SEPARATOR',
        'T_SECRULE_VARIABLE_PART',
        'T_SECRULE_VARIABLE_PART_QUOTED',
        'T_SECRULE_VARIABLE_PART_QUOTED_REGEX',

        'T_SECRULE_OPERATOR',
        'T_SECRULE_OPERATOR_WITH_EXCLAMMARK',
        'T_SECRULE_OPERATOR_ARGUMENT',
        'T_SECRULE_OPERATOR_QUOTE_MARK',

        'T_SECRULE_ACTION_QUOTE_MARK',
        'T_SECRULE_ACTION',
        'T_SECRULE_ACTION_ARGUMENT',
        'T_SECRULE_ACTION_ARGUMENT_VALUE',
        'T_SECRULE_ACTION_ARGUMENT_VALUE_PARAMETER',
        'T_SECRULE_ACTION_ARGUMENT_VALUE_PARAMETER_COLON',
        'T_SECRULE_ACTION_ARGUMENT_VALUE_PARAMETER_ARGUMENT',
        'T_SECRULE_ACTION_ARGUMENT_QUOTE_SINGLE',
        'T_SECRULE_ACTION_SEPARATOR',
        'T_SECRULE_ACTION_COLON',
        'T_SECRULE_ACTION_EQUALMARK',
        'T_SECRULE_ACTION_SEMICOLON',
    ]

    states = (

        ('STCOMMENT',                                       'exclusive'),
        ('STINCLUDEDIRECTIVE',                              'exclusive'),
        ('STINCLUDEDIRECTIVEQUOTED',                        'exclusive'),
        ('STCONFIGDIRECTIVE',                               'exclusive'),
        #('STCONFIGDIRECTIVEQUOTEDARGUMENT',                 'exclusive'),
        ('STSECRULEVARIABLENEXT',                           'exclusive'),
        ('STSECRULEVARIABLE',                               'exclusive'),
        ('STSECRULEOPERATOR',                               'exclusive'),
        ('STSECRULEQUOTEDOPERATOR',                         'exclusive'),
        #('STSECRULEACTIONNEXT',                             'exclusive'),
        ('STSECRULEACTION',                                 'exclusive'),
        ('STSECRULEACTIONARGUMENT',                         'exclusive'),
        ('STSECRULEACTIONARGUMENTQUOTES',                   'exclusive'),
        ('STSECRULEACTIONARGUMENTVALUE',                    'exclusive'),
        ('STSECRULEACTIONARGUMENTVALUEPARAMETER',           'exclusive'),
        ('STSECRULEACTIONARGUMENTVALUEPARAMETERARGUMENT',   'exclusive'),
    )

    def __init__(self, debug = False, reflags = re.IGNORECASE | re.VERBOSE):
        self.lexer = ply.lex.lex(module=self, debug = debug, reflags = reflags)

        self.st_continue = 0
        self.eolcount = 0
        self.st_action_quote = 0

        self.default_config_simple_directives = [
            "SecAction",
            "SecDefaultAction",
            "SecCollectionTimeout",
            "SecComponentSignature",
            "SecContentInjection",
            "SecRequestBodyAccess",
            "SecRequestBodyLimit",
            "SecRequestBodyNoFilesLimit",
            "SecRequestBodyLimitAction",
            "SecPcreMatchLimit",
            "SecPcreMatchLimitRecursion",
            "SecResponseBodyAccess",
            "SecResponseBodyMimeType",
            "SecResponseBodyLimit",
            "SecResponseBodyLimitAction",
            "SecRule",
            "SecRuleEngine",
            "SecRuleRemoveById",
            "SecRuleRemoveByMsg",
            "SecRuleRemoveByTag",
            "SecTmpDir",
            "SecDataDir",
            "SecDebugLog",
            "SecDebugLogLevel",
            "SecAuditEngine",
            "SecAuditLogRelevantStatus",
            "SecAuditLogParts",
            "SecAuditLogType",
            "SecAuditLogFormat",
            "SecAuditLog",
            "SecAuditLogStorageDir",
            "SecArgumentSeparator",
            "SecCookieFormat",
            "SecStatusEngine",
            "SecMarker",
            "SecUnicodeMapFile",
            "SecStreamOutBodyInspection",
            "SecRuleUpdateActionById",
            "SecRuleUpdateTargetById",
            "SecRuleUpdateTargetByMsg",
            "SecRuleUpdateTargetByTag",
        ]

        self.default_secrule_variables = [
            "ARGS",
            "ARGS_COMBINED_SIZE",
            "ARGS_GET",
            "ARGS_GET_NAMES",
            "ARGS_NAMES",
            "ARGS_POST",
            "ARGS_POST_NAMES",
            "AUTH_TYPE",
            "DURATION",
            "ENV",
            "FILES",
            "FILES_COMBINED_SIZE",
            "FILES_NAMES",
            "FULL_REQUEST",
            "FULL_REQUEST_LENGTH",
            "FILES_SIZES",
            "FILES_TMPNAMES",
            "FILES_TMP_CONTENT",
            "GEO",
            "HIGHEST_SEVERITY",
            "INBOUND_DATA_ERROR",
            "MATCHED_VAR",
            "MATCHED_VARS",
            "MATCHED_VAR_NAME",
            "MATCHED_VARS_NAMES",
            "MODSEC_BUILD",
            "MULTIPART_BOUNDARY_QUOTED",
            "MULTIPART_CRLF_LF_LINES",
            "MULTIPART_FILENAME",
            "MULTIPART_NAME",
            "MULTIPART_STRICT_ERROR",
            "MULTIPART_UNMATCHED_BOUNDARY",
            "MULTIPART_BOUNDARY_WHITESPACE",
            "MULTIPART_DATA_BEFORE",
            "MULTIPART_DATA_AFTER",
            "MULTIPART_HEADER_FOLDING",
            "MULTIPART_LF_LINE",
            "MULTIPART_INVALID_QUOTING",
            "MULTIPART_INVALID_HEADER_FOLDING",
            "MULTIPART_INVALID_PART",
            "MULTIPART_FILE_LIMIT_EXCEEDED",
            "OUTBOUND_DATA_ERROR",
            "PATH_INFO",
            "PERF_ALL",
            "PERF_COMBINED",
            "PERF_GC",
            "PERF_LOGGING",
            "PERF_PHASE1",
            "PERF_PHASE2",
            "PERF_PHASE3",
            "PERF_PHASE4",
            "PERF_PHASE5",
            "PERF_RULES",
            "PERF_SREAD",
            "PERF_SWRITE",
            "QUERY_STRING",
            "REMOTE_ADDR",
            "REMOTE_HOST",
            "REMOTE_PORT",
            "REMOTE_USER",
            "REQBODY_ERROR",
            "REQBODY_ERROR_MSG",
            "REQBODY_PROCESSOR",
            "REQBODY_PROCESSOR_ERROR",
            "REQUEST_BASENAME",
            "REQUEST_BODY",
            "REQUEST_BODY_LENGTH",
            "REQUEST_COOKIES",
            "REQUEST_COOKIES_NAMES",
            "REQUEST_FILENAME",
            "REQUEST_HEADERS",
            "REQUEST_HEADERS_NAMES",
            "REQUEST_LINE",
            "REQUEST_METHOD",
            "REQUEST_PROTOCOL",
            "REQUEST_URI",
            "REQUEST_URI_RAW",
            "RESPONSE_BODY",
            "RESPONSE_CONTENT_LENGTH",
            "RESPONSE_CONTENT_TYPE",
            "RESPONSE_HEADERS",
            "RESPONSE_HEADERS_NAMES",
            "RESPONSE_PROTOCOL",
            "RESPONSE_STATUS",
            "RULE",
            "SCRIPT_BASENAME",
            "SCRIPT_FILENAME",
            "SCRIPT_GID",
            "SCRIPT_GROUPNAME",
            "SCRIPT_MODE",
            "SCRIPT_UID",
            "SCRIPT_USERNAME",
            "SDBM_DELETE_ERROR",
            "SERVER_ADDR",
            "SERVER_NAME",
            "SERVER_PORT",
            "SESSION",
            "SESSIONID",
            "STATUS_LINE",
            "STREAM_INPUT_BODY",
            "STREAM_OUTPUT_BODY",
            "TIME",
            "TIME_DAY",
            "TIME_EPOCH",
            "TIME_HOUR",
            "TIME_MIN",
            "TIME_MON",
            "TIME_SEC",
            "TIME_WDAY",
            "TIME_YEAR",
            "TX",
            "UNIQUE_ID",
            "URLENCODED_ERROR",
            "USERID",
            "USERAGENT_IP",
            "WEBAPPID",
            "WEBSERVER_ERROR_LOG",
            "XML"
        ]

        self.default_secrule_storages = [
            "GLOBAL",
            "RESOURCE",
            "IP",
            "SESSION",
            "USER"
        ]

        self.default_secrule_operators = [
            "beginsWith",
            "contains",
            "containsWord",
            "detectSQLi",
            "detectXSS",
            "endsWith",
            "fuzzyHash",
            "eq",
            "ge",
            "geoLookup",
            "gsbLookup",
            "gt",
            "inspectFile",
            "ipMatch",
            "ipMatchF",
            "ipMatchFromFile",
            "le",
            "lt",
            "noMatch",
            "pm",
            "pmf",
            "pmFromFile",
            "rbl",
            "rsub",
            "rx",
            "streq",
            "strmatch",
            "unconditionalMatch",
            "validateByteRange",
            "validateDTD",
            "validateHash",
            "validateSchema",
            "validateUrlEncoding",
            "validateUtf8Encoding",
            "verifyCC",
            "verifyCPF",
            "verifySSN",
            "within"
        ]

        self.default_secrule_actions = [
            "accuracy",
            "allow",
            "append",
            "auditlog",
            "block",
            "capture",
            "chain",
            "ctl",
            "deny",
            "deprecatevar",
            "drop",
            "exec",
            "expirevar",
            "id",
            "initcol",
            "log",
            "logdata",
            "maturity",
            "msg",
            "multiMatch",
            "noauditlog",
            "nolog",
            "pass",
            "pause",
            "phase",
            "prepend",
            "proxy",
            "redirect",
            "rev",
            "sanitiseArg",
            "sanitiseMatched",
            "sanitiseMatchedBytes",
            "sanitiseRequestHeader",
            "sanitiseResponseHeader",
            "severity",
            "setuid",
            "setrsc",
            "setsid",
            "setenv",
            "setvar",
            "skip",
            "skipAfter",
            "status",
            "t",
            "tag",
            "ver",
            "xmlns"
        ]

# Generic error handling

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

# END Generic error handling

# EOL, continue

    # hack for 'unterminated' lines, eg:
    # SecRule ... ... \
    # <EMPTY>
    def t_ANY_T_BACKSLASH_AND_NEWLINE(self, t):
        r'\\[ \t]*(\r|\n)(\r|\n)'
        self.st_continue = 0
        t.lexer.begin('INITIAL')
        self.st_action_quote = 0
        t.lexer.lineno += 1

    def t_ANY_T_BACKSLASH(self, t):
        r'\\[ \t]*(\r|\n)'
        self.st_continue = 1
        t.lexer.lineno += 1

    def t_ANY_newline(self, t):
        r'\n|\r\n'
        # hack for unquoted action list
        if t.lexer.lexstate[0:15] == "STSECRULEACTION": # any kind of action state
            self.st_continue = 0
        if self.st_continue == 0:
            t.lexer.begin('INITIAL')
            self.st_action_quote = 0
        else:
            self.st_continue = 0
        t.lexer.lineno += 1

# END EOL, continue

# Comment

    def t_INITIAL_T_COMMENT(self, t):
        r'\#([^\r\n]+|[\r\n])'
        self.parse_comment(t)
        if t.value[-1] == "\n":
            t.value = t.value.rstrip("\n")
            t.lexer.lineno += 1
        return t

    def t_STCOMMENT_T_COMMENT(self, t):
        r'.*[^\r\n]+'
        self.parse_comment(t)
        return t

# End Comment

# Handle include directive

    def t_INITIAL_T_INCLUDE_DIRECTIVE(self, t):
        r'include'
        t.lexer.begin('STINCLUDEDIRECTIVE')
        return t

    def t_STINCLUDEDIRECTIVE_T_INCLUDE_DIRECTIVE_ARGUMENT(self, t):
        r'[0-9A-Za-z_\/\.\-\*\:]+'
        #self.parse_seclang_config(t)
        t.lexer.begin('INITIAL')
        return t

    def t_STINCLUDEDIRECTIVE_T_INCLUDE_DIRECTIVE_ARGUMENT_QUOTED(self, t):
        r'"[0-9A-Za-z_\/\.\-\*\:]+"'
        #self.parse_seclang_config(t)
        t.value = t.value.strip("\"")
        t.lexer.begin('INITIAL')
        return t

# END Handle include directive

# Simple configuration directives

    def t_INITIAL_T_CONFIG_DIRECTIVE(self, t):
        r'(\s*)Sec[a-zA-Z0-9]+'
        #r'((\s*)Sec[a-zA-Z0-9]+)|\<(/|).*\>'
        t.type = self.parse_config_directive(t)
        return t

    def t_STCONFIGDIRECTIVE_T_CONFIG_DIRECTIVE(self, t):
        r'((?:\\\ |[^\ \t\n])+)'
        t.type = self.parse_config_directive_argument(t)
        return t

# END Simple configuration directives

# Apache Locaition directive

    def t_INITIAL_T_APACHE_LOCATION_DIRECTIVE(self, t):
        r'<(/|)Location.*>'
        return t

# END Apache Locaition directive

# Secrule VARIABLE

    def t_STSECRULEVARIABLENEXT_STSECRULEVARIABLE_T_SECRULE_VARIABLE(self, t):
        r'[A-Za-z0-9_-]+'
        t.type = self.parse_config_secrule_variable(t)
        return t

    def t_STSECRULEVARIABLE_T_SECRULE_VARIABLE_SEPARATOR(self, t):
        r'[,|]'
        return t

    def t_STSECRULEVARIABLENEXT_STSECRULEVARIABLE_T_SECRULE_VARIABLE_COUNTER(self, t):
        r'&'
        return t

    def t_STSECRULEVARIABLENEXT_STSECRULEVARIABLE_T_EXCLUSION_MARK(self, t):
        r'!'
        return t

    def t_STSECRULEVARIABLE_T_SECRULE_VARIABLE_PART_QUOTED_REGEX(self, t):
        r":'/([^'\"\ \t\n])+/'"
        t.value = t.value[1:]
        return t

    def t_STSECRULEVARIABLE_T_SECRULE_VARIABLE_PART_QUOTED(self, t):
        r":'([^'\"\ \t\n])+'"
        t.value = t.value[1:]
        return t

    def t_STSECRULEVARIABLE_T_SECRULE_VARIABLE_PART(self, t):
        r':([^" \t,|\n])+'
        t.value = t.value[1:]
        return t

    def t_STSECRULEVARIABLE_WHITESPACES(self, t):
        r'[ \t\n]+'
        t.lexer.begin('STSECRULEOPERATOR')

# END Secrule VARIABLE

# Secrule operator and operator argument

    def t_STSECRULEOPERATOR_T_SECRULE_OPERATOR_QUOTE_MARK(self, t):
        r'"'
        t.lexer.begin('STSECRULEQUOTEDOPERATOR')
        return t

    def t_STSECRULEOPERATOR_STSECRULEQUOTEDOPERATOR_OP(self, t):
        r'(!|)@[a-zA-Z0-9]+'
        t.type = self.parse_config_secrule_operator(t)
        return t

    def t_STSECRULEOPERATOR_OPARG(self, t):
        r'((?:[^ "\n\\]|\\.)+)'
        t.type = self.parse_config_secrule_operator(t)
        return t

    def t_STSECRULEQUOTEDOPERATOR_OPARG(self, t):
        r'((?:[^"\n\\]|\\.)+)'
        t.type = self.parse_config_secrule_operator(t)
        return t

    def t_STSECRULEQUOTEDOPERATOR_T_SECRULE_OPERATOR_QUOTE_MARK(self, t):
        r'"'
        t.lexer.begin('STSECRULEACTION')
        self.st_action_quote = 0
        return t

# END Secrule operator and operator argument

# Secrule actions and actions arguments

    def t_STSECRULEACTION_T_SECRULE_ACTION_QUOTE_MARK(self, t):
        r'"'
        if self.st_action_quote == 0:
            self.st_action_quote = 1
        else:
            self.st_action_quote = 1
            t.lexer.begin("INITIAL")
        #t.lexer.begin('STSECRULEACTION')
        return t

    def t_STSECRULEACTION_T_SECRULE_ACTION(self, t):
        r'((?:[^ ":,\n\\]|\\.)+)'
        t.type = self.parse_config_secrule_action(t)
        return t

    def t_STSECRULEACTION_T_SECRULE_ACTION_COLON(self, t):
        r':'
        t.lexer.begin('STSECRULEACTIONARGUMENT')
        return t

    def t_STSECRULEACTIONARGUMENT_T_SECRULE_ACTION_ARGUMENT_QUOTE_SINGLE(self, t):
        r"'"
        t.lexer.begin('STSECRULEACTIONARGUMENTQUOTES')
        return t

    def t_STSECRULEACTIONARGUMENTQUOTES_T_SECRULE_ACTION_ARGUMENT(self, t):
        r'((?:[^\\\']|\\(.|\s))+)'
        self.eolcount = len(t.value.split("\n"))-1
        t.lexer.lineno += self.eolcount
        return t

    def t_STSECRULEACTIONARGUMENTQUOTES_T_SECRULE_ACTION_ARGUMENT_QUOTE_SINGLE(self, t):
        r"'"
        t.lexer.begin('STSECRULEACTIONARGUMENT')
        return t

    def t_STSECRULEACTIONARGUMENT_T_SECRULE_ACTION_ARGUMENT(self, t):
        r'((?:[^,\'"=\n\\]|\\.)+)'
        return t

    def t_STSECRULEACTIONARGUMENT_T_SECRULE_ACTION_EQUALMARK(self, t):
        r'='
        t.lexer.begin('STSECRULEACTIONARGUMENTVALUE')
        return t

    def t_STSECRULEACTIONARGUMENTVALUE_T_SECRULE_ACTION_ARGUMENT_VALUE(self, t):
        r'((?:[^;,"]|\\.)+)'
        return t

    def t_STSECRULEACTIONARGUMENTVALUE_T_SECRULE_ACTION_SEMICOLON(self, t):
        r';'
        t.lexer.begin('STSECRULEACTIONARGUMENTVALUEPARAMETER')
        return t

    def t_STSECRULEACTIONARGUMENTVALUEPARAMETER_T_SECRULE_ACTION_ARGUMENT_VALUE_PARAMETER(self, t): 
        r'((?:[^:,"]|\\.)+)'
        return t

    def t_STSECRULEACTIONARGUMENTVALUEPARAMETER_T_SECRULE_ACTION_ARGUMENT_VALUE_PARAMETER_COLON(self, t):
        r':'
        t.lexer.begin('STSECRULEACTIONARGUMENTVALUEPARAMETERARGUMENT')
        return t

    def t_STSECRULEACTIONARGUMENTVALUEPARAMETERARGUMENT_T_SECRULE_ACTION_ARGUMENT_VALUE_PARAMETER_ARGUMENT(self, t):
        r'((?:[^,"]|\\.)+)'
        return t

    def t_STSECRULEACTION_STSECRULEACTIONARGUMENT_STSECRULEACTIONARGUMENTVALUE_STSECRULEACTIONARGUMENTVALUEPARAMETER_STSECRULEACTIONARGUMENTVALUEPARAMETERARGUMENT_T_SECRULE_ACTION_SEPARATOR(self, t):
        r','
        t.lexer.begin('STSECRULEACTION')
        return t

    def t_STSECRULEACTION_STSECRULEACTIONARGUMENT_STSECRULEACTIONARGUMENTVALUE_STSECRULEACTIONARGUMENTVALUEPARAMETER_STSECRULEACTIONARGUMENTVALUEPARAMETERARGUMENT_T_SECRULE_ACTION_QUOTE_MARK(self, t):
        r'"'
        t.lexer.begin('INITIAL')
        return t

# END Secrule actions and actions arguments

# Helper functions for scanner

    def parse_comment(self, t):
        tval = t.value.strip()
        if tval[-1] == "\\":
            self.st_continue = 1
            t.lexer.begin('STCOMMENT')
        else:
            t.lexer.begin('INITIAL')

    def parse_config_directive(self, t):
        for d in self.default_config_simple_directives:
            if d.lower() == t.value.lower():
                if d.lower() == "secrule":
                    t.lexer.begin('STSECRULEVARIABLENEXT')
                    return 'T_CONFIG_DIRECTIVE_SECRULE'
                if d.lower() == "secaction":
                    t.lexer.begin('STSECRULEACTION')
                    self.st_action_quote = 0
                    return 'T_CONFIG_DIRECTIVE_SECACTION'
                t.lexer.begin('STCONFIGDIRECTIVE')
                return 'T_CONFIG_DIRECTIVE'
        return None

    def parse_config_directive_argument(self, t):
        if t.value[0] == '"' and t.value[-1] == '"':
            t.value = t.value.strip("\"")
            return 'T_CONFIG_DIRECTIVE_ARGUMENT_QUOTE_DOUBLE'
        if t.value[0] == '\'' and t.value[-1] == '\'':
            t.value = t.value.strip("'")
            return 'T_CONFIG_DIRECTIVE_ARGUMENT_QUOTE_SINGLE'
        return 'T_CONFIG_DIRECTIVE_ARGUMENT_NOTQUOTE'

    def parse_config_secrule_variable(self, t):
        for d in self.default_secrule_variables:
            if d.lower() == t.value.lower():
                t.lexer.begin('STSECRULEVARIABLE')
                return 'T_SECRULE_VARIABLE'

        for d in self.default_secrule_storages:
            if d.lower() == t.value.lower():
                t.lexer.begin('STSECRULEVARIABLE')
                return 'T_SECRULE_VARIABLE'

        return None

    def parse_config_secrule_operator(self, t):
        if t.value[0] == "!" and t.value[1] == '@':
            operator = t.value[2:]
        elif t.value[0] == '@':
            operator = t.value[1:]
        else:
            operator = t.value

        for d in self.default_secrule_operators:
            if d.lower() == operator.lower():
                if t.value[0] == "!":
                    return 'T_SECRULE_OPERATOR_WITH_EXCLAMMARK'
                else:
                    return 'T_SECRULE_OPERATOR'

        if t.lexer.lexstate == 'STSECRULEOPERATOR':
            t.lexer.begin('STSECRULEACTION')
            self.st_action_quote = 0
        return 'T_SECRULE_OPERATOR_ARGUMENT'

    def parse_config_secrule_action(self, t):
        for d in self.default_secrule_actions:
            if d.lower() == t.value.lower():
                return 'T_SECRULE_ACTION'
        return None

# END Helper functions for scanner
# END Lexer class

# Parser class

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

# Parser helper functions
    def add_comment(self, p):
        self.configlines.insert(p.lineno(1), {'type': "Comment", 'argument': p[1], 'quoted': 'no_quote', 'lineno': p.lineno(1)})

    def add_directive(self, p):
        self.configlines.insert(p.lineno(1), {'type': p[1], 'arguments': [], 'lineno': p.lineno(1)})

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

    def append_action(self, act):
        if self.secconfdir == "secrule":
            self.secrule['actions'].append(act)
            if act['act_name'] == "chain":
                self.secrule['chained'] = True
        if self.secconfdir == "secaction":
            self.secaction['actions'].append(act)

# END Parser helper functions

# Grammar

    def p_config_line(self, p):
        """modsec_config : comment_line
                         | modsec_config comment_line
                         | include_line
                         | modsec_config include_line
                         | directive_line
                         | modsec_config directive_line
                         | secaction_line
                         | modsec_config secaction_line
                         | secrule_line
                         | modsec_config secrule_line"""

    def p_comment_line(self, p):
        """comment_line : T_COMMENT"""
        self.add_comment(p)

    def p_include_line(self, p):
        """include_line : include_line_unquoted_argument
                        | include_line_quoted_argument"""

    def p_include_line_unquoted_argument(self, p):
        """include_line_unquoted_argument : T_INCLUDE_DIRECTIVE T_INCLUDE_DIRECTIVE_ARGUMENT"""
        self.add_directive(p)
        self.configlines[-1]['arguments'].append({'argument': p[2], 'quote_type': 'no_quote'})

    def p_include_line_quoted_argument(self, p):
        """include_line_quoted_argument : T_INCLUDE_DIRECTIVE T_INCLUDE_DIRECTIVE_ARGUMENT_QUOTED"""
        self.add_directive(p)
        self.configlines[-1]['arguments'].append({'argument': p[2], 'quote_type': 'quoted'})

    def p_directive_line(self, p):
        """directive_line : tok_directive
                          | tok_directive tok_directive_argument_list
                          | tok_directive_apache_location"""
        pass

    def p_tok_directive(self, p):
        """tok_directive : T_CONFIG_DIRECTIVE"""
        self.add_directive(p)

    def p_tok_directive_argument_list(self, p):
        """tok_directive_argument_list : tok_directive_argument
                                       | tok_directive_argument_list tok_directive_argument"""
        pass

    def p_tok_directive_argument(self, p):
        """tok_directive_argument : tok_directive_argument_notquoted
                                  | tok_directive_argument_quoted_double
                                  | tok_directive_argument_quoted_single"""
        pass

    def p_tok_directive_argument_notquoted(self, p):
        """tok_directive_argument_notquoted : T_CONFIG_DIRECTIVE_ARGUMENT_NOTQUOTE"""
        self.configlines[-1]['arguments'].append({'argument': p[1], 'quote_type': 'no_quote'})

    def p_tok_directive_argument_quoted_double(self, p):
        """tok_directive_argument_quoted_double : T_CONFIG_DIRECTIVE_ARGUMENT_QUOTE_DOUBLE"""
        self.configlines[-1]['arguments'].append({'argument': p[1], 'quote_type': 'quoted'})

    def p_tok_directive_argument_quoted_single(self, p):
        """tok_directive_argument_quoted_single : T_CONFIG_DIRECTIVE_ARGUMENT_QUOTE_SINGLE"""
        self.configlines[-1]['arguments'].append({'argument': p[1], 'quote_type': 'quotes'})

    def p_tok_directive_apache_location(self, p):
        """tok_directive_apache_location : T_APACHE_LOCATION_DIRECTIVE"""
        self.add_directive(p)

    def p_secaction_line(self, p):
        """secaction_line : tok_confdir_secaction T_SECRULE_ACTION_QUOTE_MARK secaction_expr_list T_SECRULE_ACTION_QUOTE_MARK"""
        self.configlines.insert(self.secaction['lineno'], self.secaction)
        self.secconfdir = ""

    def p_tok_confdir_secaction(self, p):
        """tok_confdir_secaction : T_CONFIG_DIRECTIVE_SECACTION"""
        self.secaction_init(p)
        self.secconfdir = "secaction"

    def p_secrule_line(self, p):
        """secrule_line : secrule_directive secrule_argument_list secrule_operator_expression secrule_actions
                        | secrule_directive secrule_argument_list secrule_operator_expression"""
        self.configlines.insert(self.secrule['lineno'], self.secrule)
        self.secconfdir = ""

    def p_secrule_directive(self, p):
        """secrule_directive : T_CONFIG_DIRECTIVE_SECRULE"""
        self.secrule_init(p)
        self.secconfdir = "secrule"

    def p_secrule_argument_list(self, p):
        """secrule_argument_list : secrule_variable_list"""
        pass

    def p_secrule_variable_list(self, p):
        """secrule_variable_list : secrule_variable
                                 | secrule_variable_exclusion
                                 | secrule_variable_counter
                                 | secrule_variable_with_part
                                 | secrule_variable_exclusion_with_part
                                 | secrule_variable_list secrule_variable_separator secrule_variable
                                 | secrule_variable_list secrule_variable_separator secrule_variable_counter
                                 | secrule_variable_list secrule_variable_separator secrule_variable_with_part
                                 | secrule_variable_list secrule_variable_separator secrule_variable_exclusion
                                 | secrule_variable_list secrule_variable_separator secrule_variable_exclusion_with_part"""
        pass

    def p_secrule_variable(self, p):
        """secrule_variable : T_SECRULE_VARIABLE"""
        self.secrule['variables'].append({'variable': p[1], 'variable_part': "", 'quote_type': 'no_quote', 'negated': False, 'counter': False})

    def p_secrule_variable_exclusion(self, p):
        """secrule_variable_exclusion : T_EXCLUSION_MARK  T_SECRULE_VARIABLE"""
        self.secrule['variables'].append({'variable': p[2], 'variable_part': "", 'quote_type': 'no_quote', 'negated': True, 'counter': False})

    def p_secrule_variable_with_part(self, p):
        """secrule_variable_with_part : T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART
                                      | T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART_QUOTED
                                      | T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART_QUOTED_REGEX"""
        var = p[2]
        qtype = 'no_quote'
        if var[0] == "'" and var[-1] == "'":
            var = var.strip("'")
            qtype = 'quotes'
        self.secrule['variables'].append({'variable': p[1], 'variable_part': var, 'quote_type': qtype, 'negated': False, 'counter': False})

    def p_secrule_variable_exclusion_with_part(self, p):
        """secrule_variable_exclusion_with_part : T_EXCLUSION_MARK T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART
                                                | T_EXCLUSION_MARK T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART_QUOTED
                                                | T_EXCLUSION_MARK T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART_QUOTED_REGEX"""
        var = p[3]
        qtype = 'no_quote'
        if var[0] == "'" and var[-1] == "'":
            var = var.strip("'")
            qtype = 'quotes'
        self.secrule['variables'].append({'variable': p[2], 'variable_part': var, 'quote_type': qtype, 'negated': True, 'counter': False})

    def p_secrule_variable_counter(self, p):
        """secrule_variable_counter : secrule_variable_counter_only
                                    | secrule_variable_counter_with_var"""
        pass

    def p_secrule_variable_counter_only(self, p):
        """secrule_variable_counter_only : T_SECRULE_VARIABLE_COUNTER T_SECRULE_VARIABLE"""
        self.secrule['variables'].append({'variable': p[2], 'variable_part': "", 'quote_type': "no_quote", 'negated': False, 'counter': True})

    def p_secrule_variable_counter_with_var(self, p):
        """secrule_variable_counter_with_var : T_SECRULE_VARIABLE_COUNTER T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART
                                             | T_SECRULE_VARIABLE_COUNTER T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART_QUOTED
                                             | T_SECRULE_VARIABLE_COUNTER T_SECRULE_VARIABLE T_SECRULE_VARIABLE_PART_QUOTED_REGEX"""
        var = p[3]
        qtype = 'no_quote'
        if var != None:
            if var[0] == "'" and var[-1] == "'":
                var = var.strip("'")
                qtype = 'quotes'
        else:
            var = ""
        self.secrule['variables'].append({'variable': p[2], 'variable_part': var, 'quote_type': qtype, 'negated': False, 'counter': True})

    def p_secrule_variable_separator(self, p):
        """secrule_variable_separator : T_SECRULE_VARIABLE_SEPARATOR"""
        pass

    def p_secrule_operator_expression(self, p):
        """secrule_operator_expression : secrule_operator_expression_quoted
                                       | secrule_operator_or_argument
                                       | secrule_operator_and_argument"""
        pass

    def p_secrule_operator_expression_quoted(self, p):
        """secrule_operator_expression_quoted : T_SECRULE_OPERATOR_QUOTE_MARK secrule_operator_or_argument T_SECRULE_OPERATOR_QUOTE_MARK
                                              | T_SECRULE_OPERATOR_QUOTE_MARK secrule_operator_and_argument T_SECRULE_OPERATOR_QUOTE_MARK"""
        pass

    def p_secrule_operator_or_argument(self, p):
        """secrule_operator_or_argument : secrule_operator_only
                                        | secrule_operator_argument_only"""
        pass

    def p_secrule_operator_only(self, p):
        """secrule_operator_only : T_SECRULE_OPERATOR
                                 | T_SECRULE_OPERATOR_WITH_EXCLAMMARK"""
        if p[1][0] == "!":
            self.secrule['operator_negated'] = True
            self.secrule['operator'] = p[1][1:]
            self.secrule['operator_argument'] = ""
            self.secrule['oplineno'] = p.lineno(1)
        else:
            self.secrule['operator_negated'] = False
            self.secrule['operator'] = p[1]
            self.secrule['operator_argument'] = ""
            self.secrule['oplineno'] = p.lineno(1)

    def p_secrule_operator_argument_only(self, p):
        """secrule_operator_argument_only : T_SECRULE_OPERATOR_ARGUMENT"""
        self.secrule['operator_negated'] = False
        self.secrule['operator'] = ""
        self.secrule['operator_argument'] = p[1]
        self.secrule['oplineno'] = p.lineno(1)

    def p_secrule_operator_and_argument(self, p):
        """secrule_operator_and_argument : T_SECRULE_OPERATOR T_SECRULE_OPERATOR_ARGUMENT
                                         | T_SECRULE_OPERATOR_WITH_EXCLAMMARK T_SECRULE_OPERATOR_ARGUMENT"""
        if p[1][0] == "!":
            self.secrule['operator_negated'] = True
            self.secrule['operator'] = p[1][1:]
            self.secrule['oplineno'] = p.lineno(1)
        else:
            self.secrule['operator_negated'] = False
            self.secrule['operator'] = p[1]
            self.secrule['oplineno'] = p.lineno(1)
        self.secrule['operator_argument'] = p[2]

    def p_secrule_actions(self, p):
        """secrule_actions : T_SECRULE_ACTION_QUOTE_MARK secrule_actions_list T_SECRULE_ACTION_QUOTE_MARK
                           | secrule_actions_list"""
        pass

    def p_secrule_actions_list(self, p):
        """secrule_actions_list : secaction_expr
                                | secaction_expr_list secaction_expr"""
        pass

    def p_secaction_expr_list(self, p):
        """secaction_expr_list  : secaction_expr
                                | secaction_expr_list secaction_expr"""
        pass

    def p_secaction_expr(self, p):
        """secaction_expr : secaction_single
                          | secaction_with_argument
                          | secaction_with_quoted_argument
                          | secaction_with_argument_with_value
                          | secaction_with_argument_with_value_and_param
                          | secaction_with_argument_with_value_and_param_paramarg
                          | T_SECRULE_ACTION_SEPARATOR"""
        pass

    def p_secaction_single(self, p):
        """secaction_single : T_SECRULE_ACTION"""
        self.append_action({'act_name': p[1], 'lineno': p.lineno(1), 'act_quote': 'no_quote', 'act_arg': "", 'act_arg_val': "", 'act_arg_val_param': "", 'act_arg_val_param_val': ""})

    def p_secaction_with_argument(self, p):
        """secaction_with_argument : T_SECRULE_ACTION T_SECRULE_ACTION_COLON T_SECRULE_ACTION_ARGUMENT"""
        self.append_action({'act_name': p[1], 'lineno': p.lineno(1), 'act_quote': 'no_quote', 'act_arg': p[3], 'act_arg_val': "", 'act_arg_val_param': "", 'act_arg_val_param_val': ""})

    def p_secaction_with_quoted_argument(self, p):
        """secaction_with_quoted_argument : T_SECRULE_ACTION T_SECRULE_ACTION_COLON T_SECRULE_ACTION_ARGUMENT_QUOTE_SINGLE T_SECRULE_ACTION_ARGUMENT T_SECRULE_ACTION_ARGUMENT_QUOTE_SINGLE"""
        self.append_action({'act_name': p[1], 'lineno': p.lineno(1), 'act_quote': 'quotes', 'act_arg': p[4], 'act_arg_val': "", 'act_arg_val_param': "", 'act_arg_val_param_val': ""})

    def p_secaction_with_argument_with_value(self, p):
        """secaction_with_argument_with_value : T_SECRULE_ACTION T_SECRULE_ACTION_COLON T_SECRULE_ACTION_ARGUMENT T_SECRULE_ACTION_EQUALMARK T_SECRULE_ACTION_ARGUMENT_VALUE"""
        self.append_action({'act_name': p[1], 'lineno': p.lineno(1), 'act_quote': 'no_quote', 'act_arg': p[3], 'act_arg_val': p[5], 'act_arg_val_param': "", 'act_arg_val_param_val': ""})

    def p_secaction_with_argument_with_value_and_param(self, p):
        """secaction_with_argument_with_value_and_param : T_SECRULE_ACTION T_SECRULE_ACTION_COLON T_SECRULE_ACTION_ARGUMENT T_SECRULE_ACTION_EQUALMARK T_SECRULE_ACTION_ARGUMENT_VALUE T_SECRULE_ACTION_SEMICOLON T_SECRULE_ACTION_ARGUMENT_VALUE_PARAMETER"""
        self.append_action({'act_name': p[1], 'lineno': p.lineno(1), 'act_quote': 'no_quote', 'act_arg': p[3], 'act_arg_val': p[5], 'act_arg_val_param': p[7], 'act_arg_val_param_val': ""})

    def p_secaction_with_argument_with_value_and_param_paramarg(self, p):
        """secaction_with_argument_with_value_and_param_paramarg : T_SECRULE_ACTION T_SECRULE_ACTION_COLON T_SECRULE_ACTION_ARGUMENT T_SECRULE_ACTION_EQUALMARK T_SECRULE_ACTION_ARGUMENT_VALUE T_SECRULE_ACTION_SEMICOLON T_SECRULE_ACTION_ARGUMENT_VALUE_PARAMETER T_SECRULE_ACTION_ARGUMENT_VALUE_PARAMETER_COLON T_SECRULE_ACTION_ARGUMENT_VALUE_PARAMETER_ARGUMENT"""
        self.append_action({'act_name': p[1], 'lineno': p.lineno(1), 'act_quote': 'no_quote', 'act_arg': p[3], 'act_arg_val': p[5], 'act_arg_val_param': p[7], 'act_arg_val_param_val': p[9]})

# END Grammar

    # handling parser error
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
                    (li+1, p.lexer.lexpos, pos, aff_line, (pos * "~")))
            raise Exception(output)
        else:
            secrule = {}

# END Parser class



class MSCWriter(object):
    def __init__(self, data, indentstr = "    ", indentchained = True):
        self.lineno = 1
        self.output = []
        self.chainlevel = 0
        self.ident = ""
        self.sdata = data
        self.quote_types = {
            'no_quote': "",
            'quotes': "'",
            'quoted': '"'
        }
        self.indentstr = indentstr
        self.indentchained = indentchained

    # builds an action
    def make_action_arg(self, a):
        ret = ""
        if 'act_arg' not in a or a['act_arg'] == "":
            ret = "%s" % (a['act_name'])
        else:
            ret = "%s:%s%s%s" % (a['act_name'], self.quote_types[a['act_quote']], str(a['act_arg']), self.quote_types[a['act_quote']])
            pref = ["=", ";", ":"]
            akeys = ['act_arg_val', 'act_arg_val_param', 'act_arg_val_param_val']
            for ai in range(len(akeys)):
                if a[akeys[ai]] != "":
                    ret += "%s%s" % (pref[ai], a[akeys[ai]])
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
            if self.indentchained == True:
                self.ident = (self.chainlevel+1)*self.indentstr
            else:
                self.ident = self.indentstr
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
                    if self.indentchained == True:
                        self.ident = (self.chainlevel+1)*self.indentstr
                    else:
                        self.ident = self.indentstr
                    joiner = ",\\\n" + self.ident
            currline.append(actstr)
            lasta = a.copy()
            self.lineno = a['lineno']
            if a['act_arg'] != "":
                self.lineno += len(a['act_arg'].split("\n"))-1
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

        variables = []
        for v in r['variables']:
            _var = ""
            if v['negated'] == True:
                _var += "!" 
            if v['counter'] == True:
                _var += "&"
            _var += v['variable']
            if v['variable_part'] != "":
                _var += ":"
            _var += "%s%s%s" % (self.quote_types[v['quote_type']], v['variable_part'], self.quote_types[v['quote_type']]) if v['variable_part'] != "" else ""
            variables.append(_var)

        opargs = []
        negate = ""
        if r['operator_negated'] == True:
            negate = "!"
        for o in [r['operator'], r['operator_argument']]:
            if o != "":
                opargs.append(o)
        oppref = " "
        if r['lineno'] < r['oplineno']:
            oppref = " \\\n%s" % ((self.chainlevel+1)*self.indentstr)
        opgroups = "%s\"%s\"" % (oppref, negate + " ".join(opargs))

        if self.indentchained == True:
            secrule = ["%sSecRule %s%s" % ((self.chainlevel)*self.indentstr, "|".join(variables), opgroups)]
        else:
            secrule = ["SecRule %s%s" % ("|".join(variables), opgroups)]
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
            if i['type'].lower() == "comment":
                self.output.append("%s" % (i['argument']))
                self.lineno = i['lineno']+1
            elif i['type'].lower() == "secrule":
                self.make_secrule(i)
                self.lineno += 1
            elif i['type'].lower() == "secaction":
                self.make_secaction(i)
                self.lineno += 1
            else:
                line = [i['type']]
                for a in i['arguments']:
                    line.append("%s%s%s" % (self.quote_types[a['quote_type']], a['argument'], self.quote_types[a['quote_type']]))
                self.output.append(" ".join(line))
                self.lineno += 1

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
