from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow import DAG
from datetime import datetime
import mysql.connector 
from airflow.providers.mysql.hooks.mysql import MySqlHook

from airflow.models.dagrun import DagRun
from airflow.models.taskinstance import TaskInstance

# Define your DAG

conn_id = conn_id = 'airflow_mysql'
db = 'air'
table = 'task_instance'


    

def task_status(dag_name, task_name):
    # con = mysql.connector.connect(
    # host='127.0.0.1',
    # user='root',
    # password='Mysql.08',
    # database='world'
    # )
    # cursor = con.cursor()
    
    sql = str(f"SELECT * FROM {db}.{table} where dag_id='{dag_name}' and task_id='{task_name}' order by job_id desc limit 1;")
    mysql_hook = MySqlHook(mysql_conn_id=conn_id)

    results = mysql_hook.get_records(sql)
    return(results)

# def get_task_status(dag_id, task_id):
    
#     last_dag_run = DagRun.find(dag_id=dag_id)
#     last_dag_run.sort(key=lambda x: x.execution_date, reverse=True)
    
#     return last_dag_run[0].get_task_instance(task_id).state
    


dag = DAG(
    dag_id='job_status_check',
    schedule_interval=None,  # Set the appropriate schedule interval
    start_date=datetime(2023, 8, 11),  # Set the appropriate start date
    catchup=False,
)

# Define the first task
task1 = BashOperator(
    task_id="task1",
    bash_command='echo "Task 1"',
    dag=dag
)

last_dag_run = DagRun.find(dag_id="job_status_check")
last_dag_run.sort(key=lambda x: x.execution_date, reverse=True)

sta = last_dag_run[0].get_task_instance("task1").state


# Define the second task
task2 = BashOperator(
    task_id="task2",
    bash_command='echo "{{ params.end2 }}"',
    params={'end2': sta},
    dag=dag
)



task2_state = task_status('job_status_check','task2')

task3 = BashOperator(
    task_id="task3",
    bash_command=f'echo "{task2_state}"',
    dag=dag
)



# t3 = PythonOperator(
#     task_id = 'get_task_status',
#     python_callable = get_task_status,
#     op_args = ['job_status_check', 'task2'],
#     do_xcom_push = False
#   )



task1 >> task2   >> task3 
