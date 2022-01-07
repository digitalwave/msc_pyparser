[![Latest Version](https://img.shields.io/pypi/v/msc-pyparser.svg)](https://pypi.python.org/pypi/msc-pyparser)
[![License](https://img.shields.io/badge/License-GPLv3-green.svg)](https://pypi.python.org/pypi/msc-pyparser)

# modsec_parser

Welcome to the `modsec_parser` documentation.

The parser runs under Python 3.6+ on Linux, Windows and Mac.

Installation
============

The parser relies on *Ply* as its underlying parsing library.

Therefore, to run it you will need:

* a **Python 3** interpreter
* **Ply** - the Python Ley Yacc library
* **YAML** and/or **JSON** it you want your output to be either of those

### Debian install

You can install these packages on Debian with this command:

```bash
sudo apt install python3-ply python3-yaml python3-ubjson
```

### Installing using pip3

The module is published as a pip3 module.

**Method 1** You can install it using:

```
pip3 install msc-pyparser>=1.2.0
```

That will install it system-wide.

**Method 2** If you want to use a virtualenv:

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

**Method 3** Another option is to use [pipenv](https://pipenv.org) that will give you isolation and dependency management:

```
pip3 install pipenv
pipenv install msc-pyparser
```

That will create the proper virtual environment and you can now switch to it using `pipenv shell`.

#### :point_right: Important notes after 1.0 :point_left:

After v1.0 the inside API has changed. The parser has extended with new capabilities, and the inside structure was aligned.

#### :point_right: Important notes after 1.2.0 :point_left:

After v1.2.0 the versioning structure has changed: from two digits (eg. 1.1) we have switched to three digits (1.2.0). The other important change is the lexer and parser exceptions contain extra information about the exception cause and position.

🎉 That's it!

Try to keep the module updated, because it is under heavy development now.

New features and changes in 1.0
===============================

* `msc_pyparser` can parse the whole ModSecurity config, not just the CRS rules
    * this means that you can pass the root configuration file to the parser, which contains the `include /path/to/coreruleset/*.conf` directive, and you will get the `include` directives and its arguments (path to files). So you can walk those files and you will get your whole config. **This is the most important new feature.**

    * **please note, that the parser doesn't parses the files as recursively, you need to handle this directive**
* You can extend the parser (basically the scanner). If there is a token which missing (eg. you have any Apache directive in the config (see Comodo rules below), then you can add them. These tokens will handled as directives. Also you can extend the variables (see Comodo rules), operators, and actions.
* the API has changed. the new structure stores the necessary data in much more detail.
    * there are four different structure, the previous versions had two:
        * Comment - it's simple, the comments
        * Directive - everythng which isn't comment, SecRule or SecAction
        * SecRule - the SecRule entity from config
        * SecAction - the SecAction entity from config
    * the structures stores more detailed info:
        * Directive stores the keyword, and the variable length argument list. Every item in list contains info about the quoted status of value
        * SecRule:
            * the variables expanded into more detailed structure: it contains the info about variable name, negated flag (`!`), counter flag (`&`), variable subpart and its quoted status
            * operator structure also has a new flag about its negated status
            * action structure got a new member: in the previous versions, for eg. the `ctl` actions last part (consider `ctl:ruleRemoveTargetById=1234;ARGS:passwd` - the `ARGS:passed`) now splitted into two member. Now the new keys are:
              * `act_name` (eg. `ctl`)
              * `lineno` (number of the line)
              * `act_quote` (arg. val is quoted - it isn't in the given example)
              * `act_arg` (eg. `ruleRemoveTargetById`)
              * `act_arg_val` (`1234`)
              * `act_arg_val_param` (`ARGS`)
              * `act_arg_val_param_val` (`passwd`)
        * SecAction - the action list is same as at SecRule
* MSCWriter has two option argument: `indentstr` and `indentchained` - see below the details
* in `examples` directory you don't need to create a loop to run for list of files anymore; just create the output directory, and run the script:
`mkdir crsmod; ./example3_addtag.py crsyaml/*.yaml crsmod`
but of course, it works for a single file too:
`./example3_addtag.py crsyaml/specific_ruleset.yml mod_specific_ruleset.yml`

New features and changes in 1.2.0
=================================

* `msc_pyparser` has a new version format with three digits `1.2.0`:
* the exceptions of MSCLexer and MSCParser modules have an extra argument in their exceptions. It's a dictionary:

```
{
  'cause': <class 'str'> one of the "lexer" or "parser",
  'line': <class 'int'>,
  'column': <class 'int'>,
  'position': <class 'int'>
}
```

Module Contents
===============

`modsec_parser` contains these classes:

* MSCLexer
* MSCParser
* MSCWriter
* MSCUtils

## Module version

Before you start to work with `msc_pyparser`, please check the version to make sure you have the current one (`1.1`):

```python
$ python3
...
>>> import msc_pyparser
>>> print(msc_pyparser.__version__)
1.2.0
>>>

```

MSCLexer
========

The `MSCLexer` class is a wrapper for Ply's `lexer` object. You can use it independently, to **check** and **see** what tokens are in your `ModSecurity` ruleset.

Here is a simple example:

```python
$ python3
Python 3.8.5 (default, Aug  2 2020, 15:09:07)
[GCC 10.2.0] on linux
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
LexToken(T_CONFIG_DIRECTIVE_SECRULE,'SecRule',1,0)
LexToken(T_SECRULE_VARIABLE,'TX',1,8)
LexToken(T_SECRULE_VARIABLE_PART,'EXECUTING_PARANOIA_LEVEL',1,10)
LexToken(T_SECRULE_OPERATOR_QUOTE_MARK,'"',1,36)
LexToken(T_SECRULE_OPERATOR,'@lt',1,37)
LexToken(T_SECRULE_OPERATOR_ARGUMENT,'1',1,41)
LexToken(T_SECRULE_OPERATOR_QUOTE_MARK,'"',1,42)
LexToken(T_SECRULE_ACTION_QUOTE_MARK,'"',1,44)
LexToken(T_SECRULE_ACTION,'id',1,45)
LexToken(T_SECRULE_ACTION_COLON,':',1,47)
LexToken(T_SECRULE_ACTION_ARGUMENT,'920011',1,48)
LexToken(T_SECRULE_ACTION_SEPARATOR,',',1,54)
LexToken(T_SECRULE_ACTION,'phase',1,55)
LexToken(T_SECRULE_ACTION_COLON,':',1,60)
LexToken(T_SECRULE_ACTION_ARGUMENT,'1',1,61)
LexToken(T_SECRULE_ACTION_SEPARATOR,',',1,62)
LexToken(T_SECRULE_ACTION,'pass',1,63)
LexToken(T_SECRULE_ACTION_SEPARATOR,',',1,67)
LexToken(T_SECRULE_ACTION,'nolog',1,68)
LexToken(T_SECRULE_ACTION_SEPARATOR,',',1,73)
LexToken(T_SECRULE_ACTION,'skipAfter',1,74)
LexToken(T_SECRULE_ACTION_COLON,':',1,83)
LexToken(T_SECRULE_ACTION_ARGUMENT,'END-REQUEST-920-PROTOCOL-ENFORCEMENT',1,84)
LexToken(T_SECRULE_ACTION_QUOTE_MARK,'"',1,120)

```

**Note**: the token list has changed in version 1.0.

Now see the exception:

```python
>>> import msc_pyparser
>>>
>>> rule = """\nSecRule ARGS1 "@rx foo" "phase:1,id:1,block" """
>>> mlexer = msc_pyparser.MSCLexer()
>>> mlexer.lexer.input(rule)
>>> while True:
...     try:
...         tok = mlexer.lexer.token()
...         if not tok:
...             break
...         print(tok)
...     except Exception as e:
...         print(e.args[0])
...         print(e.args[1])
...         break
...
LexToken(T_CONFIG_DIRECTIVE_SECRULE,'SecRule',2,1)
Lexer error: illegal token found in line 2 at pos 14, column 13
SecRule ARGS1 "@rx foo" "phase:1,id:1,block"
~~~~~~~~~~~~~^
{'cause': 'lexer', 'line': 2, 'position': 14, 'column': 13}
```
Please note, that the given target does not exist.

For a more detailed example, see `test_lexer.py` in the `examples` directory.

MSCParser
=========

The `MSCParser` class is a wrapper for Ply's `parser` object. The parser object needs a lexer, but `MSCParser` invokes `MSCLexer` and sets it up.

Here is a simple example:

```python
$ python3
Python 3.8.5 (default, Aug  2 2020, 15:09:07) 
[GCC 10.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import msc_pyparser
>>> rule = """SecRule TX:EXECUTING_PARANOIA_LEVEL "@lt 1" "id:920011,phase:1,pass,nolog,skipAfter:END-REQUEST-920-PROTOCOL-ENFORCEMENT" """
>>> mparser = msc_pyparser.MSCParser()
Generating LALR tables
>>> mparser.parser.parse(rule, debug = True)
PLY: PARSE DEBUG START

State  : 0
Stack  : . LexToken(T_CONFIG_DIRECTIVE_SECRULE,'SecRule',1,0)
Action : Shift and goto state 18


python
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
PLY: PARSE DEBUG END
>>> print(mparser.configlines)
[{'type': 'SecRule', 'lineno': 1, 'variables': [{'variable': 'TX', 'variable_part': 'EXECUTING_PARANOIA_LEVEL', 'quote_type': 'no_quote', 'negated': False, 'counter': False}], 'operator': '@lt', 'operator_argument': '1', 'actions': [{'act_name': 'id', 'lineno': 1, 'act_quote': 'no_quote', 'act_arg': '920011', 'act_arg_val': '', 'act_arg_val_param': '', 'act_arg_val_param_val': ''}, {'act_name': 'phase', 'lineno': 1, 'act_quote': 'no_quote', 'act_arg': '1', 'act_arg_val': '', 'act_arg_val_param': '', 'act_arg_val_param_val': ''}, {'act_name': 'pass', 'lineno': 1, 'act_quote': 'no_quote', 'act_arg': '', 'act_arg_val': '', 'act_arg_val_param': '', 'act_arg_val_param_val': ''}, {'act_name': 'nolog', 'lineno': 1, 'act_quote': 'no_quote', 'act_arg': '', 'act_arg_val': '', 'act_arg_val_param': '', 'act_arg_val_param_val': ''}, {'act_name': 'skipAfter', 'lineno': 1, 'act_quote': 'no_quote', 'act_arg': 'END-REQUEST-920-PROTOCOL-ENFORCEMENT', 'act_arg_val': '', 'act_arg_val_param': '', 'act_arg_val_param_val': ''}], 'chained': False, 'operator_negated': False, 'oplineno': 1}]

```

**Note**: the list of grammar rules has changed in version 1.0.

Now let's see an example for the exception:

```python
>>> import msc_pyparser
>>> rule = """\nSecRule ARGS "@rx foo "phase:1,id:1,block" """
>>> mparser = msc_pyparser.MSCParser()
>>> try:
...     mparser.parser.parse(rule, debug = False)
... except Exception as e:
...     print(e.args[0])
...     print(e.args[1])
...
Parser error: syntax error in line 2 at pos 43, column 42
SecRule ARGS "@rx foo "phase:1,id:1,block"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
{'cause': 'parser', 'line': 2, 'position': 43, 'column': 42}
```

For a detailed example, see `test_parser.py` program in the `examples` directory.

### MSCWriter

This class transforms the inside structure to the string. You can save the result to a file. This class converts YAML, JSON, etc, to a config file. See the example file `crs_writer.py` for how it works.

Here is a simple example:

```python
$ python3
Python 3.8.5 (default, Aug  2 2020, 15:09:07) 
[GCC 10.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import msc_pyparser
>>> data = [{'type': 'SecRule', 'lineno': 1, 'variables': [{'variable': 'TX', 'variable_part': 'EXECUTING_PARANOIA_LEVEL', 'quote_type': 'no_quote', 'negated': False, 'counter': False}], 'operator': '@lt', 'operator_argument': '1', 'actions': [{'act_name': 'id', 'lineno': 1, 'act_quote': 'no_quote', 'act_arg': '920011', 'act_arg_val': '', 'act_arg_val_param': '', 'act_arg_val_param_val': ''}, {'act_name': 'phase', 'lineno': 1, 'act_quote': 'no_quote', 'act_arg': '1', 'act_arg_val': '', 'act_arg_val_param': '', 'act_arg_val_param_val': ''}, {'act_name': 'pass', 'lineno': 1, 'act_quote': 'no_quote', 'act_arg': '', 'act_arg_val': '', 'act_arg_val_param': '', 'act_arg_val_param_val': ''}, {'act_name': 'nolog', 'lineno': 1, 'act_quote': 'no_quote', 'act_arg': '', 'act_arg_val': '', 'act_arg_val_param': '', 'act_arg_val_param_val': ''}, {'act_name': 'skipAfter', 'lineno': 1, 'act_quote': 'no_quote', 'act_arg': 'END-REQUEST-920-PROTOCOL-ENFORCEMENT', 'act_arg_val': '', 'act_arg_val_param': '', 'act_arg_val_param_val': ''}], 'chained': False, 'operator_negated': False, 'oplineno': 1}]
>>> mwriter = msc_pyparser.MSCWriter(data)
>>> mwriter.generate()
>>> print(mwriter.output)
['SecRule TX:EXECUTING_PARANOIA_LEVEL "@lt 1" "id:920011,phase:1,pass,nolog,skipAfter:END-REQUEST-920-PROTOCOL-ENFORCEMENT"']
```

**Note**: the writer class has aligned to the modified structure in version 1.0.

### MSCUtils

This class contains IO helper functions (currently only one function).

Inside of structure
===================

The `MSCParser` class reads the `ModSecurity` rulesets, and transforms them into a Python `list`. Every item in this list is a `dictionary`. Every dictionary item has the keys `type` and `lineno`. Depending on the `type` there might be additional keys.

These are the supported types:

* Comment
* Directive
* SecRule
* SecAction

**Note**: the types has changed in version 1.0.

There are four types of dictionary objects for types above:

```python
{
  'type': "Comment",
  'argument': <class 'str'>,
  'quoted': 'no_quote',
  'lineno': <class 'int'>
}

{
  'type': <class 'str'>,
  'arguments': <class 'list' of 'argument'>,
  'lineno': <class 'int'>
}

{
  'type': "SecRule",
  'lineno': <class 'int'>,
  'variables': <class 'list' of 'variable'>,
  'operator': <class 'str'>,
  'operator_argument': <class 'str'>,
  'operator_negated': <class 'bool'>,
  'oplineno': <clas 'int'>,
  'actions': <class 'list' of 'action'>,
  'chained': False
}

{
  'type': "SecAction",
  'lineno': <class 'int'>,
  'actions': <class 'list' of 'action'>
}
```

Here are the types of each list above:

```python

"arguments" list:

{
  'argument': <class 'str'>,
  'quote_type': QUOTE_TYPE
}

"variables" list:

{
  'variable': <class 'str'>,
  'variable_part': <class 'str'>,
  'quote_type': QUOTE_TYPE,
  'negated': <class 'bool'>,
  'counter': <class 'bool'>
}

"actions" list:

{
  'act_name': <class 'str'>,
  'lineno': <class 'int'>,
  'act_quote': QUOTE_TYPE,
  'act_arg': <class 'str'>,
  'act_arg_val': <class 'str'>,
  'act_arg_val_param': <class 'str'>,
  'act_arg_val_param_val': <class 'str'>
}
```

Quote type:
```python
'QUOTE_TYPE' could be item from set('no_quote', 'quotes', 'quoted')
```

where
* `no_quote` - there isn't any quote mark
* `quotes` - means **S**ingle quote (`'`)
* `quoted` - means **D**double quote (`"`)


type
----
**Description:** type of the configuration directive

**Used at:** Comment, Directive

**Syntax:** `'type': <class 'str'>`

**Example Usage:** `'type': "SecRuleEngine"`

**Default Value:** no default value

**Possible value:** `Comment`, or any possible directive in ModSecurity (except `Secrule` and `SecAction`)

**Scope:** Comment or Directive dictionary

**Added Version:** 0.1

**Changed in:** 1.0


lineno
------
**Description**: line number in the original file

**Syntax:** `'lineno': <class 'int'>`

**Example Usage:** `'lineno': 10`

**Default Value:** no default value

**Possible value:** a positive integer

**Scope:** every item in the list

**Added Version:** 0.1


argument
--------
**Description**: the dictionary next to the directive

**Syntax:** `{'argument': <class 'str'>, 'quote_type': QUOTE_TYPE}`

**Example Usage:** `{'argument': '# this is a comment', 'quote_type': 'no_quote'}`

**Default Value:** no default value

**Possible value:** no restrictions

**Scope:** Comment or Directive dictionary

**Added Version:** 0.1

**Changd in:** 1.0


quoted
------
**Description**: indicates if the argument was quoted or not

**Syntax:** `'quoted': <class 'str'>`

**Example Usage:** `'quoted': quotes`

**Default Value:** `no_quoted`

**Possible value:** `no_quoted`, `quoted` (quoted with DOUBLE quotes `"`), `quotes` (quoted with SINGLE quotes `'`)

**Scope:** Dictionary key in Comment, Directive types, and used list: variables, actions and arguments.

**Added Version:** 0.1


variables
---------
**Description**: dictionary of variables in `SecRule`

**Syntax:** `'variables': <class 'list'>`

**Example Usage:** `'variabes': {'variable': 'TX', 'variable_part': 'crs_exclusions_xenforo', 'quote_type': 'no_quote', 'negated': False, 'counter': True}`

*Note, that this converted from config:* `&TX:crs_exclusions_xenforo`

**Default Value:** no default value

**Possible value:** list with variables, no other restrictions

**Scope:** `SecRule`

**Added Version:** 0.1

**Changed in:** 1.0

variables.variable
------------------

**Description:** name of variable

**Example usage:** `'variable':'COOKIES'`

**Added Version:** 1.0

variables.variable_part
-----------------------

**Description:** name of variable key

**Example usage:** `'variable_part':'/__utm/'`

**Added Version:** 1.0

variables.quote_type
--------------------

**Description:** quote type of variable part

**Example usage:** `'quote_type': 'no_quote'`

**Added Version:** 1.0

variables.negated
-----------------

**Description:** store the information of variable has a `!` prefix

**Example usage:** `'negated': False`

**Added Version:** 1.0

variables.counter
-----------------

**Description:** store the information of variable has a `&` prefix

**Example usage:** `'counter': False`

**Added Version:** 1.0

operator
--------
**Description**: operator of `SecRule`

**Syntax:** `'operator': <class 'str'>`

**Example Usage:** `'operator': '@eq'`

**Default Value:** no default value

**Possible value:** could be empty (means `@rx`, or any valid operator - see the ModSecurity [reference](https://github.com/SpiderLabs/ModSecurity/wiki/Reference-Manual-(v2.x)#Operators))

**Scope:** `SecAction`, `SecRule`

**Added Version:** 0.1

oplineno
--------
**Description**: number of lines in the original file of operator of `SecRule` if that's different than the config directive

**Syntax:** `'oplineno': <class 'int'>`

**Example Usage:** `'opelineno': 10`

**Default Value:** any positive integer

**Possible value:** could be empty (which means the operator is in the same line as the configuration keyword)

**Scope:** `SecRule`

**Added Version:** 0.1

operator_argument
-----------------
**Description**: argument of operator if given

**Syntax:** `'operator_argument': <class 'str'>`

**Example Usage:** `'operator_argument': ^.*$`

**Default Value:** no default value

**Possible value:** no restrictions, it could be empty if operator not expects

**Scope:** `SecRule`

**Added Version:** 0.1

operator_negated
----------------
**Description**: store the information of operator has a `!` prefix

**Syntax:** `'operator_negated': <class 'bool'>`

**Example Usage:** `'operator_negated': False`

**Default Value:** no default value

**Possible value:** `True`, `False`

**Scope:** `SecRule`

**Added Version:** 1.0

actions
-------
**Description**: list of actions of `SecRule` or `SecAction`

**Syntax:** `'actions': <class 'list'>`

**Example Usage:** `'actions': [<action1>, <action2>, ...]`

**Default Value:** no default value

**Possible value:** dictionaries of `action` items

**Scope:** `SecAction`, `SecRule`

**Added Version:** 0.1


actions.act_name
----------------
**Description**: action name in item of list of actions of `SecRule` or `SecAction`

**Syntax:** `'act_name': <class 'str'>`

**Example Usage:** `'act_name': 'id'`

**Default Value:** no default value

**Possible value:** can be any valid action see the ModSecurity [reference](https://github.com/SpiderLabs/ModSecurity/wiki/Reference-Manual-(v2.x)#Actions))

**Scope:** `actions` list of `SecAction`, `SecRule`

**Added Version:** 0.1


actions.act_arg
---------------
**Description**: action argument in item of list of actions of `SecRule` or `SecAction`

**Syntax:** `'act_arg': <class 'str'>`

**Example Usage:** `'act_name': '910001'`

**Default Value:** no default value

**Possible value:** depends on the type of arg_name - see reference

**Scope:** `actions` list of `SecAction`, `SecRule`

**Added Version:** 0.1


actions.act_quote
-----------------
**Description**: holds the information about the quoted state of action argument for the list of actions of `SecRule` or `SecAction`, e.g., the argument of `msg` actions is typically quoted with `'`

**Syntax:** `'act_quote': <class 'str'>`

**Example Usage:** `'act_quote': 'no_quoted'`

**Default Value:** `no_quoted`

**Possible value:** `no_quoted`, `quotes`, `quoted`

**Scope:** `actions` list of `SecAction`, `SecRule`

**Added Version:** 0.1

actions.lineno
--------------
**Description**: Same as previous `lineno`.

**Syntax:** `'lineno': <class 'int'>`

**Example Usage:** `'lineno': 11`

**Default Value:** no default value

**Possible value:** any positive integer

**Scope:** `actions` list of `SecAction`, `SecRule`

**Added Version:** 0.1

actions.act_arg_val
-------------------
**Description**: holds the argument of the action item in actions of `SecRule` or `SecAction` contains arguments (e.g.: `ctl:ruleRemovebyId=1234`)

**Syntax:** `'act_arg_val': <class 'str'>`

**Example Usage:** `'act_arg_val': 1234` - from the example above description

**Default Value:** no default value

**Possible value:** no restriction

**Scope:** `actions` list of `SecAction`, `SecRule`

**Added Version:** 1.0

**Changed in:** 1.0 - this is replaced the old `act_ctl_arg` key in previous versions


actions.act_arg_val_param
-------------------------
**Description**: holds the parameter of the argument of the action item in actions of `SecRule` or `SecAction` contains arguments (e.g.: `ctl:ruleRemoveById=1234`)

**Syntax:** `'act_arg_val_param': <class 'str'>`

**Example Usage:** `'act_arg_val_param': '1234'` - from the example above description

**Default Value:** no default value

**Possible value:** no restriction

**Scope:** `actions` list of `SecAction`, `SecRule`

**Added Version:** 1.0

**Changed in:** 1.0 - this is replaced the old `act_arg_valparam` key in previous versions, which was splitted by two parts

actions.act_arg_val_param_val
-----------------------------
**Description**: holds the parameter of the argument of the action item in actions of `SecRule` or `SecAction` contains arguments (e.g.: `ctl:ruleRemoveTargetById=1234;ARGS=passwd`)

**Syntax:** `'act_arg_val_param': <class 'str'>`

**Example Usage:** `'act_arg_val_param': 'passwd'` - from the example above description

**Default Value:** no default value

**Possible value:** no restriction

**Scope:** `actions` list of `SecAction`, `SecRule`

**Added Version:** 1.0

**Changed in:** 1.0 - this is replaced the old `act_arg_valparam` key in previous versions, which was splitted by two parts

Examples
========

There is the `examples/` subdirectory with some examples, data, and descriptions in the code.

To execute the examples:

```bash
mkdir crsyaml
./crs_read.py /path/to/coreruleset/rules crsyaml
```

This command will read your rulesets and convert all of them to the directory `crsyaml`. Note that the ruleset names are the same as the original and now the extension is `.yaml`. To change the extension from `yaml` to `json`, see the source.

Now you can write the parsed rules from `yaml` (or `json`) to ModSecurity:

```bash
mkdir crschanged
./crs_write.py crsyaml crschanged
```

Now look at the differences between the original and converted versions:
```
for f in `ls -1 crschanged/*.conf`; do f=`basename ${f}`; diff crschanged/${f} ~/src/coreruleset/rules/${f}; done
```

If there are no other differences, then the rulesets are the same.

NEW in 1.0
==========

From the release 1.0, `msc_pyparser` can parses several type of rule sets, eg. Comodo rule set. This rule set uses few "old" variable, like `HTTP_User-Agent` or `HTTP_REFERER`. While the parser is extendable, you can append any tokes to any default list - see the source of `examples/comodo_read.py`:

```python
        mparser.lexer.default_secrule_variables.append("HTTP_User-Agent")
        mparser.lexer.default_secrule_variables.append("HTTP_REFERER")
        mparser.lexer.default_config_simple_directives.append("<LocationMatch /options-general\.php>")
        mparser.lexer.default_config_simple_directives.append("<LocationMatch /sql\.php>")
        mparser.lexer.default_config_simple_directives.append("<LocationMatch /lib/exe/ajax\.php>")
        mparser.lexer.default_config_simple_directives.append("<LocationMatch /export\.php>")
        mparser.lexer.default_config_simple_directives.append("</LocationMatch>")
```
Whit this hack, the parser can recognize the non-standard variables (`default_secrule_variables.append()`), and can handle Apache's `<Location...>` directives as directives. Just run the example, if you have Comodo rule set:

```shell
mkdir comodoyaml
./comodo_read.py ~/src/comodo_rules/ comodoyaml/
```

The given example `comodo_write.py` also has some modification: you can set the indent string and indentation rule in the constructior of `MSCWriter` - see the source:

```python
    mwriter = msc_pyparser.MSCWriter(data, indentstr = "\t", indentchained = False)
```

Note, the `indentstr` is four space by default, but Comodo uses tabulator. The `indentnchained` argument means every chained part of the whole rule is indented or not. CRS uses this feature, Comodo does not, so the default is `True`.

Run the write command:
```shell
mkdir comodochanged
./comodo_write.py comodoyaml/ comodochanged/
```

and compare the source and generated rules:

```shell
for f in `ls -1 comodochanged/*.conf`; do f=`basename ${f}`; diff --strip-trailing-cr comodochanged/${f} ~/src/comodo_rules/${f}; done
```

Notes: this command uses the `--strip-trailing-cr` option, because some lines are terminated by `\r\n`, which was dropped by the parser. The output of `diff` will show few differences, eg:

```diff
65a66
> 
25a26
> 
```
These are here because some files has few extra empy lines at the end of files, after the last rule.

There are more differences:
```diff
100c100
< SecRule REQUEST_BASENAME "@within index.php" \
---
> SecRule REQUEST_BASENAME "@within   index.php" \
114c114
< SecRule ARGS_GET:option "@streq com_users" \
---
> SecRule ARGS_GET:option "@streq  com_users" \
116c116
< SecRule ARGS_GET:view "@streq notes" \
---
> SecRule ARGS_GET:view "@streq  notes" \
```

I think I don't need to explain these. :)


If there are no other differences here, then the rulesets are the same.

### Module Examples

The examples files also show how this module works, and are a helpful reference if you wish to extend this module.

Looking at `examples/test_lexer_crs.py`, the following command will show you how and what tokens are found in your config:

```bash
./examples/test_lexer_crs.py /path/to/coreruleset/rules/REQUEST-920-PROTOCOL-ENFORCEMENT.conf debug
```

Run the following command to see how the parser applies language rules to the tokens:

```bash
./examples/test_parser_crs.py /path/to/coreruleset/rules/REQUEST-920-PROTOCOL-ENFORCEMENT.conf debug
```

There are also a modified version for Comodo rule set, see `test_lexer_comodo.py` and `test_parser_comodo.py`. I think the set with name `30_Apps_OtherApps.conf` is a good example, it contains the "strange" variables and Apache directives too. Use the commands with `debug` option.

The output from the above commands will be in the `examples/` directory.

### Development

If you are using pipenv, just install development modules by running `pipenv install --dev`.  Tests were written using `pytest`.
Just execute `pytest -v tests` in the top directory and tests will be run.

Reporting issues
================

If you run into unexpected behavior, found a bug, or have a feature request, just [create a new issue](https://github.com/digitalwave/msc_pyparser/issues/new), or drop an e-mail to us: **modsecurity** at **digitalwave** dot **hu**.

Known bugs
==========

Actually, there isn't any know bug.

Testing rulesets
================

There are four set which has tested: CRS (of course), Comodo WAF rules and Atomicorp sets. All of them are parsable, but the comparison is a bit difficult. The reason is simple: `msc_pyparser` drops the control tokens and identations. Eg. if the rule uses mixed indentations, that will be replaced by a fix indent string (can be passed to writer class). Or if the rule uses `,` as variable separator, eg `ARGS,ARGS_NAMES`, then the written rules will have `|`. Action list will always quoted, eg: ` ...t:none` will be `... "t:none"`.

There are four script in the `examples/` directory to help the reading and writing of each set:

```bash
examples/atomicorp_check.sh
examples/comodo_check.sh
examples/comodo_check_nginx.sh
examples/crs_check.sh
```
For more details, see the options for used `diff` command. Also a good idea to check the scrips, and the called Python programs.

To run the tests, please make a copy of the affected ruleset into the source directory which placed in test file, eg:
```bash
mkdir coreruleset coreruleset_out
cp -Rp /path/to/coreruleset/rules/*.conf coreruleset/
./crs_check.sh
```

If everything is fine, don't forget to remote these directories.


