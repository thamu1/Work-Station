

# SSH_USER="p_bd_ms_etl_svc"
# SSH_HOST="JMAPREDGE4.classic.pchad.com"

# ssh "${SSH_USER}"@"${SSH_HOST}" "/mapr/JMAPRCLUP01.CLASSIC.PCHAD.COM/codebase/bigdata/prod/thahive/hive.py"

# ssh "p_bd_ms_etl_svc"@"JMAPREDGE4.classic.pchad.com" "/mapr/JMAPRCLUP01.CLASSIC.PCHAD.COM/codebase/bigdata/prod/thahive/hive.py"
# no_of_retries="1 2 3"

# #Triggering the DAG
# ssh "${SSH_USER}"@"${SSH_HOST}"

import subprocess
ssh_user = "p_bd_ms_etl_svc"
shh_host = "JMAPREDGE4.classic.pchad.com"
cmd = f'ssh {ssh_user}@{shh_host} hive-bigdata'

process = subprocess.Popen("python3 --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
stdout, stderr = process.communicate()

if process.returncode == 0:
    print("Execution successful!")
    print("Output:")
    print(stdout)
else:
    print("Execution failed!")
    print("Error message:")
    print(stderr)
    
cmd = "/mapr/JMAPRCLUP01.CLASSIC.PCHAD.COM/codebase/bigdata/prod/thahive/hive1.hql"

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
    
print("executed successfully..")