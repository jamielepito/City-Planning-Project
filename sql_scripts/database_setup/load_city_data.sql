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
  We create a .my.cnf file so it is only used for the currently logged in user. Make sure that your mysql is pointing
  to this file as the config file. If you are using a mac, you can look in your system preferences, go to MySQL, and
  under 'Configuration' you can set the correct thing. You should hopefully be able to restart the server just from
  there and get the settings imported. If this does not work, good luck.
  Inside the config file it should look something like:
    [mysqld]
    secure_file_priv = ""

  Local must also be activated so that this script can work. This is needed for MySQL 8. Your total config should now
  look like:
    [mysqld]
    secure_file_priv = ""
    local_infile = 1

    [mysql]
    local-infile = 1
 */

USE city_project;

-- We can not use variables as paths so concatenation is not possible so this is nice and general.
-- Instead, just edit each path to point to the correct place or you can edit the config file and change the data dir.
LOAD DATA LOCAL INFILE "/Users/cameronkuchta/Documents/GitHub/City-Planning-Project/csv_files/owner_db.csv"
INTO TABLE owner_parcel
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE "/Users/cameronkuchta/Documents/GitHub/City-Planning-Project/csv_files/parcel_db.csv"
INTO TABLE parcel
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(parcel_id, owner_id, zipcode, @is_rental, census_tract)
SET rental = IF(@is_rental = 'Y', TRUE, FALSE);

LOAD DATA LOCAL INFILE "/Users/cameronkuchta/Documents/GitHub/City-Planning-Project/csv_files/violations_db.csv"
INTO TABLE violation
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
