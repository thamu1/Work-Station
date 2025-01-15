from datetime import datetime,timedelta
from airflow import DAG
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.operators.bash import BashOperator
import pandas as pd
import json
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook

db = 'world'
tab = 'table_name' 
conn_id = 'airflow_mysql'


def select():
    mysql_hook = MySqlHook(mysql_conn_id=conn_id)  
    sql_query = f"SELECT * FROM {db}.city where ID=2;"
    results = mysql_hook.get_records(sql_query)
    for row in results:
        print(row)
    dic = {"value":results}
    df = pd.DataFrame(dic)
    df.to_json(f'/home/thamu/airflow/json_file/j.json')
    print(df)
    
    # file = open(f'/home/thamu/airflow/dags/json/j.json')
    # jfile = json.loads(file.read())
    # print(jfile['value']['0'])


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
    dag_id='airflow_select',
    default_args=args,
    schedule_interval='@once',
    start_date=datetime(2023,5,22),
    dagrun_timeout=timedelta(minutes=60),
    description='use case of mysql operator in airflow',
)

start = BashOperator(
    task_id='start',
    bash_command=f'echo "start"',
    dag=dag
)

cre_db = PythonOperator(
    task_id = 'select_val',
    python_callable=select,
    dag=dag
)


stop = BashOperator(
    task_id='stop',
    bash_command='echo "end"',
    dag=dag
)

start >> cre_db >> stop
 


# conn = mysql.connector.connect(
#     host='127.0.0.1',
#     user='root',
#     password='Mysql.08',
#     database='world'
# )

# cursor = conn.cursor()
# sql_query = f'select * from city where ID=1;'
# cursor.execute(sql_query)
# result = cursor.fetchall()
# df = pd.DataFrame(result)


# df.to_json(f'//wsl.localhost/Ubuntu/home/thamu/airflow/dags/json/j.json')


# cre_db = MySqlOperator(
#             task_id = 'create_database',
#             mysql_conn_id = conn_id,
#             database=db,
#             sql = sql_query,
#             dag = dag, 
#         )