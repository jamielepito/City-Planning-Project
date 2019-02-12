create table parcel (
    parcel_id smallint unsigned primary key,
	owner_id smallint unsigned,
    foreign key(owner_id) references owner_parcel(owner_id),
    zipcode smallint unsigned,
    rental boolean,
    census_tracts numeric(10,1)
);

create table owner_parcel (
	 owner_id smallint unsigned primary key,
	 owner_zipcode smallint unsigned
);

create table violation (
	 id smallint unsigned primary key,
     parcel_id varchar(20),
     foreign key(parcel_id) references parcel(parcel_id),
     violation_code smallint unsigned,
     violation_id smallint unsigned
);