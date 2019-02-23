USE city_project;

CREATE OR REPLACE VIEW city_project.violations_per_parcel (parcel_id, violation_count) AS
  SELECT p.parcel_id, COUNT(v.parcel_id)
FROM parcel p
  LEFT JOIN violation v ON p.parcel_id = v.parcel_id
GROUP BY p.parcel_id;

