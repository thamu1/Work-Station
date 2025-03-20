select model_year, state, count(1) as count_of_vehicle 
from vehicle_poc.vehicle_silver
group by model_year, state