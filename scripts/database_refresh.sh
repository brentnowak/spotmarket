#!/bin/bash
cd /home/ubuntu/spotmarket
wget https://www.fuzzwork.co.uk/dump/postgres-latest.dmp.bz2
bzip2 -d postgres-latest.dmp.bz2
pg_restore h localhost -p 5432 -U spotmarketadmin -d spotmarket -v "postgres-latest.dmp"
rm postgres-latest.dmp