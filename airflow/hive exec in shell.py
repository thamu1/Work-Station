import subprocess

print("start")

cmd = 'hive -e "select * from uat_im_crossref.cust_id_current limit 10;" '

#process = subprocess.Popen("hive -f /mapr/JMAPRCLUP01.CLASSIC.PCHAD.COM/codebase/bigdata/prod/thahive/h.hql", 
#	shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
#stdout, stderr = process.communicate()

process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
stdout, stderr = process.communicate()


if process.returncode == 0:
    print("Execution successful!")
    print("Output:")
    print(stdout)
else:
    print("Execution failed!")
    print("Error message:")
    print(stderr)
    
print("end")
