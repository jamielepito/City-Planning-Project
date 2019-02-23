USE city_project;

-- Number of violations per census tract.
SELECT ROUND(parcel.census_tract, 0) as census_tract, COUNT(v.parcel_id) AS number_of_violations
FROM parcel
LEFT JOIN violation v ON parcel.parcel_id = v.parcel_id
GROUP BY ROUND(parcel.census_tract, 0)
ORDER BY ROUND(parcel.census_tract, 0);

-- Number of violations per segment per census tract.
SELECT parcel.census_tract, COUNT(v.parcel_id) AS number_of_violations
FROM parcel
  LEFT JOIN violation v ON parcel.parcel_id = v.parcel_id
GROUP BY parcel.census_tract
ORDER BY parcel.census_tract;
