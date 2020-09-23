#!/bin/bash

for f in `ls -1 coreruleset/*.conf`; do echo ${f}; ./test_parser.py ${f}; if [ $? -ne 0 ]; then break; fi; done
for f in `ls -1 coreruleset/*.yml`; do echo ${f}; ./test_writer.py ${f}; if [ $? -ne 0 ]; then break; fi; done
rm -f coreruleset_out/*.conf
mv coreruleset/*_crs.conf coreruleset_out/
for f in `ls -1 coreruleset_out/*.conf`; do n=`basename ${f}`; o=`echo ${n} | sed -e "s/_out//g"`; echo ${o}; diff coreruleset/${o} coreruleset_out/${n}; done


