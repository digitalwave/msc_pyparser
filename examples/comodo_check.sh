#!/bin/bash

for f in `ls -1 comodo_rules/*.conf`; do echo ${f}; ./test_parser_comodo.py ${f}; if [ $? -ne 0 ]; then break; fi; done
for f in `ls -1 comodo_rules/*.yml`; do echo ${f}; ./test_writer_comodo.py ${f}; if [ $? -ne 0 ]; then break; fi; done
rm -f comodo_rules_out/*.conf
mv comodo_rules/*_out.conf comodo_rules_out/
for f in `ls -1 comodo_rules_out/*.conf`; do n=`basename ${f}`; o=`echo ${n} | sed -e "s/_out//g"`; echo ${o}; diff --strip-trailing-cr -w -B comodo_rules/${o} comodo_rules_out/${n}; done


