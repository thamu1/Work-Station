
  
    
        create table vehicle_poc.vehicle_silver
      
      
      
      
      
      
      
      

      as
      select * from vehicle_poc.vehicle_bronze
where electric_range > 200
  