/*
  To load data, the config file for this database needs to be edited to allow data to be loaded from our
  csv_files directory. You can see what the current privileges are by using
    'show variables like "secure_file_priv"'
  when logged into the mysql connection. We need to edit this variable before starting the connection.
  To resolve this problem, we create a config file for use by mysql in your home directory. You can see
  where options for mysql are found by running
    'mysql -?'
  and looking for the lines that say:
    Default options are read from the following files in the given order:
    /etc/my.cnf /etc/mysql/my.cnf /usr/local/mysql/etc/my.cnf ~/.my.cnf
  We create a .my.cnf file so it is only used for the currently logged in user.
 */

USE city_project;

LOAD DATA INFILE '../csv_files/owner_db.csv' INTO TABLE owner_parcel;

LOAD DATA INFILE '../csv_files/parcel_db.csv' INTO TABLE parcel;

LOAD DATA INFILE '../csv_files/violations_db.csv' INTO TABLE violation;
