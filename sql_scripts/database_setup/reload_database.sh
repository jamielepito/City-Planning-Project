#!/usr/bin/env bash
mysql -u "root" -ppassword --verbose --show-warnings < drop_tables.sql > reload_output.txt
mysql -u "root" -ppassword --verbose --show-warnings < create_database.sql >> reload_output.txt
mysql -u "root" -ppassword --verbose --show-warnings < load_city_data.sql >> reload_output.txt
