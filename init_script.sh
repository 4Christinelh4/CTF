#!/bin/bash 
service postgresql start
psql -U postgres -d comp6841db -a -f init_table.sql