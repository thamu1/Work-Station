from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# Define the parent DAG
dag_id = 'parent_dag'
dag = DAG(
    dag_id=dag_id,
    schedule_interval=None,  # Set to None to disable automatic scheduling
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

# Define tasks in the parent DAG
task_to_wait_for = BashOperator(task_id='task_to_wait_for', bash_command= "echo 'thamu' " , dag=dag)
task_after_external_marker = BashOperator(task_id='task_after_external_marker', bash_command= "echo 'thamu' ", dag=dag)

# Set up the task dependencies
task_to_wait_for >> task_after_external_marker
