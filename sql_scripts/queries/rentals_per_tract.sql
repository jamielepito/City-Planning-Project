USE city_project;

-- Number of rentals and percent rentals per tract.
SELECT ROUND(parcel.census_tract, 0) as census_tract,
  COUNT(IF(rental = 1, 1, NULL)) as number_of_rentals,
  (COUNT(IF(rental = 1, 1, NULL))/COUNT(DISTINCT IF(rental = 1, parcel.parcel_id, NULL))) as avg_violations_per_rental,
  COUNT(IF(rental = 0, 1, NULL)) as number_of_owned,
  (COUNT(IF(rental = 0, 1, NULL))/COUNT(DISTINCT IF(rental = 0, parcel.parcel_id, NULL))) as avg_violations_per_owned
FROM parcel
  LEFT JOIN violation v ON parcel.parcel_id = v.parcel_id
GROUP BY ROUND(parcel.census_tract, 0)
ORDER BY ROUND(parcel.census_tract, 0);

