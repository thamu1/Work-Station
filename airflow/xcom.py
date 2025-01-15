from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow import DAG 

from airflow.models.taskinstance import TaskInstance as ti
from airflow.models.dagrun import DagRun



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
    # 'conn_id' : 'airflow_mysql',
    'retry_delay': timedelta(seconds=5),
    }



dag = DAG(
    dag_id='airflow_xcom',
    default_args=args,
    schedule_interval='@once',
    start_date=datetime(2023,5,31),
    dagrun_timeout=timedelta(minutes=60),
    description='use case of mysql operator in airflow',
)

def call():
    return "thamu result from python"




# Define the second BashOperator task
task2 = BashOperator(
    task_id='task2',
    bash_command='echo "fuck 2"',
    dag=dag,
)

task3 = PythonOperator(
    task_id = "task3",
    python_callable= call,
    dag = dag,
)


# Define the fourth BashOperator task which uses XCom to pull data from task2
task4 = BashOperator(
    task_id='task4',
    bash_command='echo "Received: {{ ti.xcom_pull(task_ids=\'task2\') }}"',
    dag=dag,
)

task5 = BashOperator(
    task_id = "task5",
    bash_command= "echo 'call : {{ti.xcom_pull(task_ids = \'task3\')}}'",
    dag = dag,
)


# Set task dependencies
task2 >> task3 >>  task4 >> task5







