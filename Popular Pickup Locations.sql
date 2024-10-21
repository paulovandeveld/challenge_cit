SELECT *
FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2022`
LIMIT 10;

-- CTE to calculate the total number of trips for every pickup location
WITH trip_counts AS (
    SELECT 
        pickup_location_id, 
        COUNT(*) AS total_trips
    FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2022`
    GROUP BY pickup_location_id
)

-- Select only top 5 pickup locations 
SELECT 
    pickup_location_id, 
    total_trips
FROM trip_counts
ORDER BY total_trips DESC
LIMIT 5;
