from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta


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
    # 'conn_id' : 'airflow_mysql',
    'retry_delay': timedelta(seconds=5),
    }

dag = DAG(
    dag_id='hive_execute',
    default_args=args,
    schedule_interval='@once',
    start_date=datetime(2023,8,7),
    # dagrun_timeout=timedelta(minutes=60),
    tags= ['hive execution','monthly 2nd'],
    description='run test',
)

start = BashOperator(
    task_id='start',
    bash_command=f'echo "start"',
    dag=dag
)

h1 = BashOperator(
    task_id = 'hive1',
    bash_command=f'select * from uat_logging.tablesmappinginfo limit 10;',
    dag = dag
)

# h2 = BashOperator(
#     task_id = 'hive2',
#     bash_command=f'echo "query 2"',
#     dag = dag
# )

# h3 = BashOperator(
#     task_id = 'hive3',
#     bash_command=f'echo "query 3"',
#     dag = dag
# )

stop = BashOperator(
    task_id='stop',
    bash_command='echo "end"',
    dag=dag
)
