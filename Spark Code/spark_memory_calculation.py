# 1 Partition == 1 Core

file_size_GB = 100

file_size_MB = file_size_GB * 1024

default_partition_size = 128

avg_partition_per_exec = 4

tot_no_partition = file_size_MB // default_partition_size 

print("total number of partition : ", tot_no_partition)

tot_no_executor = tot_no_partition // avg_partition_per_exec

print("total number of executor : ", tot_no_executor)

memory_for_1_exec = ((avg_partition_per_exec ** 2) * default_partition_size)

print(f"Executor memory for 1 executor in MB : {memory_for_1_exec} MB" )

tot_exec_memory = tot_no_executor * memory_for_1_exec

print(f"Total executor memory in GB : {(tot_exec_memory // 1024)} GB" )