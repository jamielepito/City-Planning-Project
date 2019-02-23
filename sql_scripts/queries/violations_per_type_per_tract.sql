USE city_project;

SELECT parcel.census_tract, COUNT(IF(rental = 1, 1, NULL)) AS number_of_violations
FROM parcel
  LEFT JOIN violation v ON parcel.parcel_id = v.parcel_id
GROUP BY parcel.census_tract
ORDER BY parcel.census_tract;
