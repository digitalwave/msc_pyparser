#!/bin/bash

for f in `ls -1 comodo_nginx/*.conf`; do echo ${f}; ./test_parser_comodo.py ${f}; if [ $? -ne 0 ]; then break; fi; done
for f in `ls -1 comodo_nginx/*.yml`; do echo ${f}; ./test_writer_comodo.py ${f}; if [ $? -ne 0 ]; then break; fi; done
rm -f comodo_nginx_out/*.conf
mv comodo_nginx/*_out.conf comodo_nginx_out/
###for f in `ls -1 comodo_nginx_out/*.conf`; do n=`basename ${f}`; o=`echo ${n} | sed -e "s/_out//g"`; echo ${o}; diff --strip-trailing-cr comodo_nginx/${o} comodo_nginx_out/${n}; done


