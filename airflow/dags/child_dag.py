from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.sensors.external_task import ExternalTaskSensor, ExternalTaskMarker

# Define the child DAG
dag_id = 'child_dag'
dag = DAG(
    dag_id=dag_id,
    schedule_interval=None,  # Set to None to disable automatic scheduling
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

# Define tasks in the child DAG
task1 = BashOperator(task_id='task1', bash_command= "echo 'thamu' " , dag=dag)
task2 = BashOperator(task_id='task2', bash_command= "echo 'thamu' " , dag=dag)

# Use ExternalTaskMarker to create a task that marks external tasks as done
external_task_marker = ExternalTaskSensor(
    task_id='mark_external_task',
    external_dag_id='parent_dag',  # Specify the parent DAG ID
    external_task_id='task_to_wait_for',  # Specify the task in the parent DAG
    check_existence=True,
    execution_delta=timedelta(seconds=10),
    dag=dag,
)

# Set up the task dependencies
task1 >> external_task_marker >> task2
