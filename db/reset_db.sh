#!/bin/bash

cd $(dirname $0)

rm -rf query_history.db

sqlite3 query_history.db <schema.sql
