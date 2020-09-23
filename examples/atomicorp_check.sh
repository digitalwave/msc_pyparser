#!/bin/bash

for f in `ls -1 atomicorp_rules/*.conf`; do echo ${f}; ./test_parser_comodo.py ${f}; if [ $? -ne 0 ]; then break; fi; done
for f in `ls -1 atomicorp_rules/*.yml`; do echo ${f}; ./test_writer_comodo.py ${f}; if [ $? -ne 0 ]; then break; fi; done
rm -f atomicorp_rules_out/*.conf
mv atomicorp_rules/*_out.conf atomicorp_rules_out/
for f in `ls -1 atomicorp_rules_out/*.conf`; do n=`basename ${f}`; o=`echo ${n} | sed -e "s/_out//g"`; echo ${o}; diff -B -w atomicorp_rules/${o} atomicorp_rules_out/${n}; done


