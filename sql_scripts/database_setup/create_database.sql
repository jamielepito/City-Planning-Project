CREATE DATABASE IF NOT EXISTS city_project;

USE city_project;

CREATE TABLE IF NOT EXISTS owner_parcel (
  owner_id INT UNSIGNED PRIMARY KEY,
  owner_zipcode INT UNSIGNED
);

CREATE TABLE IF NOT EXISTS parcel (
  parcel_id VARCHAR(20) PRIMARY KEY,
  owner_id INT UNSIGNED,
  FOREIGN KEY(owner_id) REFERENCES owner_parcel(owner_id),
  zipcode SMALLINT UNSIGNED,
  rental BOOLEAN,
  census_tract NUMERIC(5,1)
);

CREATE TABLE IF NOT EXISTS violation (
  violation_id INT UNSIGNED,
  parcel_id VARCHAR(20) NOT NULL,
  FOREIGN KEY (parcel_id) REFERENCES parcel(parcel_id),
  violation_code VARCHAR(6)
);