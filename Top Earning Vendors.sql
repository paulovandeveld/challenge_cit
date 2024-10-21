-- CTE to calculate total earning for every vendor 
WITH vendor_earnings AS (
    SELECT 
        vendor_id,
        SUM(fare_amount) AS total_amount  -- Agreggates total amount for each vendor
    FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2022`
    GROUP BY vendor_id  -- Groups by vendor ID
)

-- Select top 10 vendors 
SELECT 
    vendor_id, 
    total_amount,
    RANK() OVER (ORDER BY total_amount DESC) AS rank  -- Window function to rank vendors by total_amount 
FROM vendor_earnings
ORDER BY total_amount DESC  
LIMIT 10;  
