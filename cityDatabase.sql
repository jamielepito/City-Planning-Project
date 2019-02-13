CREATE TABLE parcel (
  parcel_id SMALLINT UNSIGNED PRIMARY KEY,
  wner_id SMALLINT UNSIGNED,
  FOREIGN KEY(owner_id) REFERENCES owner_parcel(owner_id),
  zipcode SMALLINT UNSIGNED,
  rental BOOLEAN,
  census_tracts NUMERIC(10,1)
);

CREATE TABLE owner_parcel (
	owner_id SMALLINT UNSIGNED PRIMARY KEY,
	owner_zipcode SMALLINT UNSIGNED
);

CREATE TABLE violation (
  id SMALLINT UNSIGNED PRIMARY KEY,
  parcel_id VARCHAR(20),
  FOREIGN KEY(parcel_id) REFERENCES parcel(parcel_id),
  violation_code SMALLINT UNSIGNED,
  violation_id SMALLINT UNSIGNED
);