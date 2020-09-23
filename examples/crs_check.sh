#!/bin/bash

for f in `ls -1 tmp/*.conf`; do echo ${f}; ./test_parser.py ${f}; if [ $? -ne 0 ]; then break; fi; done
for f in `ls -1 tmp/*.yml`; do echo ${f}; ./test_writer.py ${f}; if [ $? -ne 0 ]; then break; fi; done
rm -f tmp_out/*.conf
mv tmp/*_out.conf tmp_out/
for f in `ls -1 tmp_out/*.conf`; do n=`basename ${f}`; o=`echo ${n} | sed -e "s/_out//g"`; echo ${o}; diff tmp/${o} tmp_out/${n}; done


