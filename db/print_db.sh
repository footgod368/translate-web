#!/bin/bash

echo "SELECT * FROM query_log" | sqlite3 query_history.db 