-- CTE to calculate the average trip distance for every hour 
WITH avg_distance_per_hour AS (
    SELECT 
        EXTRACT(HOUR FROM pickup_datetime) AS hour_of_day,  
        ROUND(AVG(trip_distance) OVER (PARTITION BY EXTRACT(HOUR FROM pickup_datetime)), 2) AS avg_trip_distance  -- Window function to calculate the average
    FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2022`
)

-- Select the hour and its average distance, ordered by the hour
SELECT DISTINCT 
    hour_of_day,
    avg_trip_distance
FROM avg_distance_per_hour
ORDER BY hour_of_day;
