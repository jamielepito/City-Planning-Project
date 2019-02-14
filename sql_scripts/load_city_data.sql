USE city_project;

LOAD DATA INFILE '../csv_files/owner_db.csv' INTO create_database.owner_parcel;

LOAD DATA INFILE '../csv_files/parcel_db.csv' INTO create_database.parcel;

LOAD DATA INFILE '../csv_files/violations_db.csv' INTO create_database.violation;
