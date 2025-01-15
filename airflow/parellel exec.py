from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.models.baseoperator import chain


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 8, 16),
    'retries': 1,
}

dag = DAG(
    'parallel_tasks_example',
    default_args=default_args,
    schedule_interval=None,  # Set your desired schedule interval
    catchup=False,
)

start_task = BashOperator(
    task_id="start",
    bash_command='echo "started"',
    dag=dag
)

end_task = BashOperator(
    task_id='endtask',
    bash_command = 'echo "end"',
    dag=dag)



p1 = BashOperator(
    task_id="p1",
    bash_command='echo "para1"',
    dag=dag
)

p2 = BashOperator(
    task_id='p2',
    bash_command = 'echo "para2"',
    dag=dag)

pp1 = BashOperator(
    task_id="pp1",
    bash_command='echo "pp1"',
    dag=dag
)

if(1 == 1):
    pp2 = BashOperator(
        task_id='pp2',
        bash_command = 'echo "pp2"',
        dag=dag)


first = [p1, p2]
sec = [pp1, pp2]
# start_task >> p1 >> p2 >> end_task
# start_task >> pp1 >> pp2 >> end_task

chain(start_task, first, sec, end_task)