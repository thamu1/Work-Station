
select * from {{ source("create_bronze_table", "vehicle_ext") }}


1C4JJXP66P	Kitsap	Poulsbo	WA	98370	2023	JEEP	WRANGLER	
Plug-in Hybrid Electric Vehicle (PHEV)	Not eligible due to low battery range	21	0	23	258127145	POINT (-122.64681 47.73689)	PUGET SOUND ENERGY INC	53035091100



CREATE TABLE vehicle_poc.vehicle_bronze(               
   `vin` string,        
   `county` string,     
   `city` string,       
   `state` string,      
   `postal_code` string,  
   `model_year` string,  
   `make` string,       
   `model` string,      
   `electric_vehicle_type` string,  
   `clean_alternative_fuel_vehicle` string,  
   `electric_range` string,  
   `base_msrp` string,  
   `legislative_district` string,  
   `dol_vehicle_id` string,  
   `vehicle_location` string,  
   `electric_utility` string,  
   `census_tract` string);

insert into vehicle_poc.vehicle_bronze values
( '5YJ3E1EB0J', 'Thurston', 'Olympia', 'WA', 98501, 2018, 'TESLA', 'MODEL 3', 'Battery Electric Vehicle (BEV)', 'Clean Alternative Fuel Vehicle Eligible', 215, 0, 22, 266755289, 'POINT (-122.89166 47.03956)', 'PUGET SOUND ENERGY INC', '53067010300')
,( '5YJ3E1EB9K', 'Williamson', 'Austin', 'TX', 78717, 2019, 'TESLA', 'MODEL 3', 'Battery Electric Vehicle (BEV)', 'Clean Alternative Fuel Vehicle Eligible', 220, 0, , 250969379, 'POINT (-97.79398 30.49266)', 'NON WASHINGTON STATE ELECTRIC UTILITY', '48491020509')
,( '5YJYGDEE8L', 'Snohomish', 'Edmonds', 'WA', 98020, 2020, 'TESLA', 'MODEL Y', 'Battery Electric Vehicle (BEV)', 'Clean Alternative Fuel Vehicle Eligible', 291, 0, 21, 124585835, 'POINT (-122.37689 47.81116)', 'PUGET SOUND ENERGY INC', '53061050502')
,( '1G1FY6S0XL', 'Snohomish', 'Edmonds', 'WA', 98020, 2020, 'CHEVROLET', 'BOLT EV', 'Battery Electric Vehicle (BEV)', 'Clean Alternative Fuel Vehicle Eligible', 259, 0, 32, 264674931, 'POINT (-122.37689 47.81116)', 'PUGET SOUND ENERGY INC', '53061050700')
,( '1N4AZ1CP3J', 'Snohomish', 'Edmonds', 'WA', 98020, 2018, 'NISSAN', 'LEAF', 'Battery Electric Vehicle (BEV)', 'Clean Alternative Fuel Vehicle Eligible', 151, 0, 21, 304576373, 'POINT (-122.37689 47.81116)', 'PUGET SOUND ENERGY INC', '53061050402')
,( '5YJ3E1EB6K', 'Snohomish', 'Edmonds', 'WA', 98026, 2019, 'TESLA', 'MODEL 3', 'Battery Electric Vehicle (BEV)', 'Clean Alternative Fuel Vehicle Eligible', 220, 0, 32, 120515020, 'POINT (-122.31768 47.87166)', 'PUGET SOUND ENERGY INC', '53061050800')
,( '1N4BZ0CP1G', 'Skagit', 'Concrete', 'WA', 98237, 2016, 'NISSAN', 'LEAF', 'Battery Electric Vehicle (BEV)', 'Clean Alternative Fuel Vehicle Eligible', 84, 0, 39, 155491024, 'POINT (-121.7515 48.53892)', 'PUGET SOUND ENERGY INC', '53057951102')
,( 'WA1E2AFY8M', 'Thurston', 'Olympia', 'WA', 98513, 2021, 'AUDI', 'Q5 E', 'Plug-in Hybrid Electric Vehicle (PHEV)', 'Not eligible due to low battery range', 18, 0, 2, 213605850, 'POINT (-122.81754 46.98876)', 'PUGET SOUND ENERGY INC', '53067012331')
,( '1N4AZ0CP6F', 'Snohomish', 'Bothell', 'WA', 98021, 2015, 'NISSAN', 'LEAF', 'Battery Electric Vehicle (BEV)', 'Clean Alternative Fuel Vehicle Eligible', 84, 0, 1, 126497752, 'POINT (-122.18384 47.8031)', 'PUGET SOUND ENERGY INC', '53061051917')
,( '5YJ3E1ECXL', 'Thurston', 'Yelm', 'WA', 98597, 2020, 'TESLA', 'MODEL 3', 'Battery Electric Vehicle (BEV)', 'Clean Alternative Fuel Vehicle Eligible', 308, 0, 2, 3486507, 'POINT (-122.60735 46.94239)', 'PUGET SOUND ENERGY INC', '53067012421')
,( '1N4AZ0CPXE', 'Thurston', 'Olympia', 'WA', 98513, 2014, 'NISSAN', 'LEAF', 'Battery Electric Vehicle (BEV)', 'Clean Alternative Fuel Vehicle Eligible', 84, 0, 2, 147204424, 'POINT (-122.81754 46.98876)', 'PUGET SOUND ENERGY INC', '53067012332')
,( '5YJ3E1EB7K', 'Grant', 'Quincy', 'WA', 98848, 2019, 'TESLA', 'MODEL 3', 'Battery Electric Vehicle (BEV)', 'Clean Alternative Fuel Vehicle Eligible', 220, 0, 13, 319706103, 'POINT (-119.85338 47.23748)', 'PUD NO 2 OF GRANT COUNTY', '53025010500')
,( 'WA1VABGE2K', 'Snohomish', 'Edmonds', 'WA', 98026, 2019, 'AUDI', 'E-TRON', 'Battery Electric Vehicle (BEV)', 'Clean Alternative Fuel Vehicle Eligible', 204, 0, 32, 251118227, 'POINT (-122.31768 47.87166)', 'PUGET SOUND ENERGY INC', '53061050900')



select electric_utility from vehicle_bronze;
select split(electric_utility, "|") from vehicle_bronze;






