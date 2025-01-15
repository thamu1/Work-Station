from datetime import datetime,timedelta
from airflow import DAG
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.operators.bash import BashOperator
import pandas as pd
import json
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook

def read_json():
    file = open('/home/thamu/airflow/json_file/j.json')
    jfile = json.loads(file.read())
    print(jfile['value']['0'])


args = {
    'owner': 'tha',  
    # 'retries' : 1,  
    #'start_date': airflow.utils.dates.days_ago(2),
    # 'end_date': datetime(),
    # 'depends_on_past': True,
    # 'email': ['test@example.com'],
    #'email_on_failure': False,
    #'email_on_retry': False,
    # If a task fails, retry it once after waiting
    # at least 5 minutes
    #'retries': 1,
    'conn_id' : 'airflow_mysql',
    'retry_delay': timedelta(seconds=5),
    }



dag = DAG(
    dag_id='airflow_json_read',
    default_args=args,
    schedule_interval='@once',
    start_date=datetime(2023,5,31),
    dagrun_timeout=timedelta(minutes=60),
    description='use case of mysql operator in airflow',
)


start = BashOperator(
    task_id="start",
    bash_command='echo "started"',
    dag=dag
)

# read = PythonOperator(
#     task_id = 'read_json_file',
#     python_callable=read_json,
#     dag=dag
# )

val = 'fail'

end = BashOperator(
    task_id="end",
    bash_command='echo "{{params.end}}"',
    params={'end':val},
    do_xcom_push = True,
    dag=dag
)


if end:
    var = "pass"
else:
    var = "fail"

end2 = BashOperator(
    task_id="end2",
    bash_command='echo "{{params.end2}}"',
    params={'end2':var},
    dag=dag
)



start >>  end >> end2


