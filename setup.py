from setuptools import setup, find_packages

setup(name = "msc_pyparser",
            description="A ModSecurity config parser in Python3",
            long_description = """
msc_pymodsecurity is a parser, which uses PLY (Python Lex and Yacc). It
tokenizes the given text, and applies the language rules. If it's done, then
builds an own structure: a list of dictionary items.

The items contains the configuration directives from the original files, and
the number of lines where it founded. Also the items contains other datas about
the configuration line and structure.

Therefore, you can make many transformations on the structured data, and can
write back the modified config.
""",
            license="""GPLv3""",
            version = "0.1",
            author = "Ervin Hegedus",
            author_email = "airween@digitalwave.hu",
            maintainer = "Ervin Hegedus",
            maintainer_email = "airween@digitalwave.hu",
            url = "",
#            packages = ,
#            scripts = ['msc_pyparser.py'],
            py_modules = ['msc_pyparser'],
            install_requires=[
              "ply >= 3.0"
            ],
            classifiers = [
              'Topic :: Text Processing'
            ],
            #packages = ["msc_pyparser"],
            #package_dir = {'msc_pyparser': 'msc_pyparser'},
            #py_modules = ["msc_pyparser"],
            #packages = find_packages(),
#            package_data = {
#              'msc_pyparser': ['parsetab.py', 'parser.out']
#            },
            data_files = [
              ('', ['parsetab.py', 'parser.out'])
            ],
            include_package_data = True,
            zip_safe = False
)
