
select * from {{source("create_silver_table", "vehicle_bronze")}}
where electric_range > 200