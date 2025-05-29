#!/bin/bash

cd $(dirname $0)

echo "SELECT * FROM query_log" | sqlite3 query_history.db 