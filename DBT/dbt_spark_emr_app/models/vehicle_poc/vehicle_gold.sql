

select model_year, state, count(1) as count_of_vehicle 
from {{source("create_gold_table", "vehicle_silver")}}
group by model_year, state