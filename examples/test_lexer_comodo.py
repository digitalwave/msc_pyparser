#!/usr/bin/env python3

import sys
import msc_pyparser

if len(sys.argv) < 2:
    print("Argument missing!")
    print("%s /path/to/config for tokenize the config!")
    sys.exit(-1)

conffile = sys.argv[1]
debug = False

if len(sys.argv) > 2 and sys.argv[2] == "debug":
    debug = True

with open(conffile) as file:
   data = file.read()

mlexer = msc_pyparser.MSCLexer(debug = debug)

mlexer.default_secrule_variables.append("HTTP_User-Agent")
mlexer.default_secrule_variables.append("HTTP_REFERER")
mlexer.default_config_simple_directives.append("<LocationMatch /options-general\.php>")
mlexer.default_config_simple_directives.append("<LocationMatch /sql\.php>")
mlexer.default_config_simple_directives.append("<LocationMatch /lib/exe/ajax\.php>")
mlexer.default_config_simple_directives.append("<LocationMatch /export\.php>")
mlexer.default_config_simple_directives.append("</LocationMatch>")

mlexer.lexer.input(data)

while True:
    try:
        tok = mlexer.lexer.token()
        if not tok: 
            break
        print(tok)
        if debug == True:
            print(mlexer.lexer.lexstate, mlexer.lexer.lexstatestack)
            print("==")
    except:
        print(sys.exc_info()[1])
        sys.exit(-1)
