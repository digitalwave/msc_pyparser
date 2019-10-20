modsec_parser
=============

Welcome to the `modsec_parser` documentation.

Prerequisites
=============

`modsec_parser` was written in Python 3 and has not been tested with Python 2.

To run the parser, you need:

+ a **Python 3** interpreter
+ **YAML** and/or **JSON** for **Python 3**
+ **Ply** - the Python Ley Yacc library

You can install these packages on Debian with this command:

```
sudo apt install python3-ply python3-yaml python3-ubjson
```

Install the module
==================

After you download the source, you can either install dependencies system-wide or in a virtual environment.

To install this module and its dependencies system-wide, run the following command:

```
sudo python3 setup.py install
```

🎉 That's it!

If you'd like to use a virtual environment for the dependencies, first make sure you have `virtualenv` installed:

```bash
pip3 install virtualenv
```

Then create the virtual environment and install dependencies:
```bash
cd msc_pyparser
mkdir ~/virtualenvs
virtualenv ~/virtualenvs/msc_pyparser
source ~/virtualenvs/msc_pyparser/bin/activate
python3 setup.py install
```

Module Contents
===============

`modsec_parser` contains these classes:

* MSCLexer
* MSCParser
* MSCWriter
* MSCUtils

### Module version

Before you start to work with `msc_pyparser`, please check the version to make sure you have the current one (`0.2`):

```
$ python3
...
>>> import msc_pyparser
>>> print(msc_pyparser.__version__)
0.2
>>> 

```

### MSCLexer

The `MSCLexer` class is a wrapper for Ply's `lexer` object. You can use it independently, to **check** and **see** what tokens are in your `ModSecurity` ruleset.

Here is a simple example:

```
$ python3
Python 3.7.4 (default, Jul 11 2019, 10:43:21) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import msc_pyparser
>>> rule = """SecRule TX:EXECUTING_PARANOIA_LEVEL "@lt 1" "id:920011,phase:1,pass,nolog,skipAfter:END-REQUEST-920-PROTOCOL-ENFORCEMENT" """
>>> mlexer = msc_pyparser.MSCLexer()
>>> mlexer.lexer.input(rule)
>>> while True:
...     tok = mlexer.lexer.token()
...     if not tok:
...         break
...     print(tok)
... 
LexToken(CONFDIR_SECRULE,'SecRule',1,0)
LexToken(SECRULE_VARIABLE,'TX',1,8)
LexToken(COLON,':',1,10)
LexToken(SECRULE_VARIABLE_ARG,'EXECUTING_PARANOIA_LEVEL',1,11)
LexToken(QUOTED,'"',1,36)
LexToken(ATSIGN,'@',1,37)
LexToken(SECRULE_OPERATOR,'lt',1,38)
LexToken(SECRULE_OPERATOR_ARG,'1',1,41)
LexToken(QUOTED,'"',1,42)
LexToken(QUOTED,'"',1,44)
LexToken(SECRULE_ACTION,'id',1,45)
LexToken(COLON,':',1,47)
LexToken(SECRULE_ACTION_ARG,'920011',1,48)
LexToken(COMMA,',',1,54)
LexToken(SECRULE_ACTION,'phase',1,55)
LexToken(COLON,':',1,60)
LexToken(SECRULE_ACTION_ARG,'1',1,61)
LexToken(COMMA,',',1,62)
LexToken(SECRULE_ACTION,'pass',1,63)
LexToken(COMMA,',',1,67)
LexToken(SECRULE_ACTION,'nolog',1,68)
LexToken(COMMA,',',1,73)
LexToken(SECRULE_ACTION,'skipAfter',1,74)
LexToken(COLON,':',1,83)
LexToken(SECRULE_ACTION_SKIPAFTERACTIONARG,'END-REQUEST-920-PROTOCOL-ENFORCEMENT',1,84)
LexToken(QUOTED,'"',1,120)

```

For a more detailed example, see `test_lexer.py` in the `examples` directory.

### MSCParser

The `MSCParser` class is a wrapper for Ply's `parser` object. The parser object needs a lexer, but `MSCParser` invokes `MSCLexer` and sets it up.

Here is a simple example:

```
$ python3
Python 3.7.4 (default, Jul 11 2019, 10:43:21) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import msc_pyparser
>>> rule = """SecRule TX:EXECUTING_PARANOIA_LEVEL "@lt 1" "id:920011,phase:1,pass,nolog,skipAfter:END-REQUEST-920-PROTOCOL-ENFORCEMENT" """
>>> mparser = msc_pyparser.MSCParser()
>>> mparser.parser.parse(rule, debug = True)
PLY: PARSE DEBUG START

State  : 0
Stack  : . LexToken(CONFDIR_SECRULE,'SecRule',1,0)
Action : Shift and goto state 13

...
State  : 1
Stack  : modsec_config . $end
Done   : Returning <NoneType @ 0x82a6b0> (None)
PLY: PARSE DEBUG END
>>>>
>>> print(mparser.configlines)
[{'type': 'SecRule', 'lineno': 1, 'variables': ['TX:EXECUTING_PARANOIA_LEVEL'], 'operator': '@lt', 'operator_argument': '1', 'actions': [{'act_name': 'id', 'lineno': 1, 'act_quote': 'no_quote', 'act_arg': '920011'}, {'act_name': 'phase', 'lineno': 1, 'act_quote': 'no_quote', 'act_arg': '1'}, {'act_name': 'pass', 'lineno': 1, 'act_quote': 'no_quote'}, {'act_name': 'nolog', 'lineno': 1, 'act_quote': 'no_quote'}, {'act_name': 'skipAfter', 'lineno': 1, 'act_quote': 'no_quote', 'act_arg': 'END-REQUEST-920-PROTOCOL-ENFORCEMENT'}], 'chained': False, 'oplineno': 1}]

```

For a detailed example, see `test_parser.py` program in the `examples` directory.

### MSCWriter

This class transforms the inside structure to the string. You can save the result to a file. This class converts YAML, JSON, etc, to a config file. See the example file `crs_writer.py` for how it works.

Here is a simple example:

```
$ python3
Python 3.7.4 (default, Jul 11 2019, 10:43:21) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import msc_pyparser
>>> data = [{'type': 'SecRule', 'lineno': 1, 'variables': ['TX:EXECUTING_PARANOIA_LEVEL'], 'operator': '@lt', 'operator_argument': '1', 'actions': [{'act_name': 'id', 'lineno': 1, 'act_quote': 'no_quote', 'act_arg': '920011'}, {'act_name': 'phase', 'lineno': 1, 'act_quote': 'no_quote', 'act_arg': '1'}, {'act_name': 'pass', 'lineno': 1, 'act_quote': 'no_quote'}, {'act_name': 'nolog', 'lineno': 1, 'act_quote': 'no_quote'}, {'act_name': 'skipAfter', 'lineno': 1, 'act_quote': 'no_quote', 'act_arg': 'END-REQUEST-920-PROTOCOL-ENFORCEMENT'}], 'chained': False, 'oplineno': 1}]
>>> mwriter = msc_pyparser.MSCWriter(data)
>>> mwriter.generate()
>>> print(mwriter.output)
['SecRule TX:EXECUTING_PARANOIA_LEVEL "@lt 1" "id:920011,phase:1,pass,nolog,skipAfter:END-REQUEST-920-PROTOCOL-ENFORCEMENT"']
```

### MSCUtils

This class contains IO helper functions (currently only one function).

Inside of structure
===================

The `MSCParser` class reads the `ModSecurity` rulesets, and transforms them into a Python `list`. Every item in this list is a `dictionary`. Every dictionary item has the keys `type` and `lineno`. Depending on the `type` there might be additional keys.

These are the supported types:

* Comment
* SecRule
* SecAction
* SecComponentSignature
* SecMarker

There are two types of dictionary objects:

```
{
  'type': <class 'str'>
  'lineno': <class 'int'>,
  'argument': "<class 'str'>",
  'quoted': "<class 'str'>",
}
```
and

```
{
  'type': <class 'str'>,
  'lineno': <class 'int'>,
  'chained': <class 'bool'>,
  'variables': <class 'list'> of <class 'str'>,
  'operator': <class 'str'>,
  'operator_argument': <class 'str'>,
  'oplineno': <class 'int'>,
  'actions': <class 'list'> of <class 'dict'>
}
```

and the dict of `actions`:
```
{
  'act_name': <class 'str'>,
  'act_arg': <class 'str'>,
  'act_quote': <class 'str'>,
  'lineno': <class 'int'>,
  'act_ctl_arg': <class 'str'>,
  'act_ctl_argparam': <class 'str'>
}

```

type
----
**Description**: type of the configuration directive

**Syntax:** `'type': <class 'str'>`

**Example Usage:** `'type': "SecRule"`

**Default Value:** no default value

**Possible value:** `Comment`, `SecComponentsSignature`, `SecMarker`, `SecAction`, `SecRule`

**Scope:** every item in the list

**Added Version:** 0.1


lineno
------
**Description**: number of line in the original file

**Syntax:** `'lineno': <class 'int'>`

**Example Usage:** `'lineno': 10`

**Default Value:** no default value

**Possible value:** a positive integer

**Scope:** every item in the list

**Added Version:** 0.1


argument
--------
**Description**: the string next to the directive

**Syntax:** `'argument': <class 'str'>`

**Example Usage:** `'argument': '# this is a comment'`

**Default Value:** no default value

**Possible value:** no restrictions

**Scope:** `Comment`, `SecComponentsSignature`, `SecMarker`

**Added Version:** 0.1


quoted
------
**Description**: indicates if the argument was quoted or not

**Syntax:** `'quoted': <class 'str'>`

**Example Usage:** `'quoted': quotes`

**Default Value:** `no_quoted`

**Possible value:** `no_quoted`, `quoted` (quoted with DOUBLE quotes `"`), `quotes` (quoted with SINGLE quotes `'`)

**Scope:** `Comment`, `SecComponentsSignature`, `SecMarker`

**Added Version:** 0.1


variables
---------
**Description**: list of variables in `SecRule` and `SecAction`

**Syntax:** `'variables': <class 'list'>`

**Example Usage:** `'variabes': ['&TX:crs_exclusions_xenforo', 'TX:crs_exclusions_xenforo']`

*Note, that this converted from config:* `&TX:crs_exclusions_xenforo|TX:crs_exclusions_xenforo`

**Default Value:** no default value

**Possible value:** list with strings, no other restrictions

**Scope:** `SecAction`, `SecRule`

**Added Version:** 0.1

operator
--------
**Description**: operator of `SecAction` or `SecRule`

**Syntax:** `'operator': <class 'str'>`

**Example Usage:** `'operator': '@eq'`

**Default Value:** no default value

**Possible value:** could be empty (means `@rx`, or any valid operator - see the ModSecurity [reference](https://github.com/SpiderLabs/ModSecurity/wiki/Reference-Manual-(v2.x)#Operators))

**Scope:** `SecAction`, `SecRule`

**Added Version:** 0.1


oplineno
--------
**Description**: number of lines in the original file of operator of `SecAction` or `SecRule` if that's different than the config directive

**Syntax:** `'oplineno': <class 'int'>`

**Example Usage:** `'opelineno': 10`

**Default Value:** any positive integer

**Possible value:** could be empty (which means the operator is in the same line as the configuration keyword)

**Scope:** `SecAction`, `SecRule`

**Added Version:** 0.1

operator_argument
-----------------
**Description**: argument of operator if given

**Syntax:** `'operator_argument': <class 'str'>`

**Example Usage:** `'operator_argument': ^.*$`

**Default Value:** no default value

**Possible value:** no restrictions, it could be empty if operator not expects

**Scope:** `SecAction`, `SecRule`

**Added Version:** 0.1


actions
-------
**Description**: list of actions of `SecRule` or `SecAction`

**Syntax:** `'actions': <class 'list'>`

**Example Usage:** `'actions': [<action1>, <action2>, ...]`

**Default Value:** no default value

**Possible value:** dictionaries of `action` items

**Scope:** `SecAction`, `SecRule`

**Added Version:** 0.1


act_name
--------
**Description**: action name in item of list of actions of `SecRule` or `SecAction`

**Syntax:** `'act_name': <class 'str'>`

**Example Usage:** `'act_name': id`

**Default Value:** no default value

**Possible value:** can be any valid action see the ModSecurity [reference](https://github.com/SpiderLabs/ModSecurity/wiki/Reference-Manual-(v2.x)#Actions))

**Scope:** `actions` list of `SecAction`, `SecRule`

**Added Version:** 0.1


act_arg
-------
**Description**: action argument in item of list of actions of `SecRule` or `SecAction`

**Syntax:** `'act_arg': <class 'str'>`

**Example Usage:** `'act_name': 910001`

**Default Value:** no default value

**Possible value:** depends on the type of arg_name - see reference

**Scope:** `actions` list of `SecAction`, `SecRule`

**Added Version:** 0.1


act_quote
---------
**Description**: holds the information about the quoted state of the action argument in the list of actions in `SecRule` or `SecAction`, e.g., the argument of `msg` actions is typically quoted with `'`

**Syntax:** `'act_quote': <class 'str'>`

**Example Usage:** `'act_quote': no_quoted`

**Default Value:** `no_quoted`

**Possible value:** `no_quoted`, `quotes`, `quoted`

**Scope:** `actions` list of `SecAction`, `SecRule`

**Added Version:** 0.1


lineno
------
**Description**: the action line number from a `SecRule` or `SecAction`

**Syntax:** `'lineno': <class 'int'>`

**Example Usage:** `'lineno': 11`

**Default Value:** no default value

**Possible value:** any positive integer

**Scope:** `actions` list of `SecAction`, `SecRule`

**Added Version:** 0.1


act_ctl_arg
-----------
**Description**: holds the argument of the action item in actions of `SecRule` or `SecAction` contains arguments (e.g.: `ctl:ruleRemovebyId=1234`)

**Syntax:** `'act_ctl_arg': <class 'str'>`

**Example Usage:** `'act_ctl_arg': 1234` - from the example above description

**Default Value:** no default value

**Possible value:** no restriction

**Scope:** `actions` list of `SecAction`, `SecRule`

**Added Version:** 0.1


act_ctl_argparam
----------------
**Description**: holds the parameter of the argument of the action item in actions of `SecRule` or `SecAction` contains arguments (e.g.: `ctl:ruleRemovebyTargetById=1234;ARGS:form_build_id`)

**Syntax:** `'act_ctl_argparam': <class 'str'>`

**Example Usage:** `'act_ctl_argparam': ARGS:form_build_id` - from the example above description

**Default Value:** no default value

**Possible value:** no restriction

**Scope:** `actions` list of `SecAction`, `SecRule`

**Added Version:** 0.1

Examples
========

There is the `examples/` subdirectory with some examples, data, and descriptions in the code.

After you installed the module with `sudo python3 setup.py install`, your first steps could be:

```
mkdir export
./crs_read.py /path/to/owasp-modsecurity-crs/rules export
```

This command will read your rulesets and convert all of them to the directory `export`. Note that the ruleset names are the same as the original and now the extension is `.yaml`. To change the extension from `yaml` to `json`, see the source.

Now you can write the parsed rules from `yaml` (or `json`) to ModSecurity:

```
mkdir import
./crs_write.py export import
```

Now look at the differences between the original and converted versions:
```
for f in `ls -1 import/*.conf`; do f=`basename ${f}`; diff import/${f} ~/src/owasp-modsecurity-crs/rules/${f}; done
```

If there are no differences, then the rulesets are the same.

### Module Tests

The test files also show how this module works, and are a helpful reference if you wish to extend this module.

Looking at `examples/test_lexer.py`, the following command will show you how and what tokens are found in your config:

```
./examples/test_lexer.py /path/to/owasp-modsecurity-crs/rules/REQUEST-920-PROTOCOL-ENFORCEMENT.conf debug
```

Run the following command to see how the parser applies language rules to the tokens:

```
./examples/test_parser.py /path/to/owasp-modsecurity-crs/rules/REQUEST-920-PROTOCOL-ENFORCEMENT.conf debug
```

The output from the above commands will be in the `examples/` directory.

Reporting issues
================

If you run into unexpected behavior, found a bug, or have a feature request, just open an issue here, or drop an e-mail to us: modsecurity at digitalwave dot hu.

Todo
====

See the TODO.txt file.
