from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.operators.bash import BashOperator
import pandas as pd
import json
from airflow.operators.python import PythonOperator
import subprocess

# from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

from pyspark.sql import SparkSession

def readFromSpark():

    # Use bash operator instead od using python operator , if result needed then go for python operator.
    cmd = "/usr/lib/spark/bin/spark-submit --master local[*] '/usr/lib/spark/python/pyspark/Pyspark Practice/sparkTry.py'"

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

    # # Print the output and errors if any
    # print("Spark job output:")
    # print(stdout.decode())
    # print("Spark job errors:")
    # print(stderr.decode())

    print(" thambi onu ila pa correct ah tha iruku......")

args = {
    'owner': 'tha',
    'retry_delay': timedelta(seconds=5),
}

dag = DAG(
    dag_id='SparkMysql',
    default_args=args,
    schedule_interval='@once',
    start_date=datetime(2023, 7, 25),
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
    description='connect with mysql using Spark and Airflow',
    tags=['Spark', 'Mysql']
)

start = BashOperator(
    task_id='start',
    bash_command=f'echo "start"',
    dag=dag
)

cre_db = PythonOperator(
    task_id='run_spark',
    python_callable=readFromSpark,
    dag=dag
)


# cre_db = SparkSubmitOperator(
#     task_id='submit_spark_job_task',
#     application="/usr/lib/spark/python/pyspark/Pyspark Practice/sparkTry.py",  # Path to your Spark job script or JAR file
#     conn_id='spark_local',  # Connection ID for your Spark cluster (configured in Airflow)
#     conf={
#         'spark.master': 'spark://172.31.0.1:50727',  # The Spark master URL (e.g., yarn, local, spark://host:port)
#         'spark.app.name': 'MySparkJob',  # Name of your Spark application
#         'spark.executor.memory': '2g',  # Memory per executor
#         # Add any additional Spark configuration properties as needed
#     },
#     dag=dag,
# )

stop = BashOperator(
    task_id='stop',
    bash_command='echo "Hiii chelm mudinju"',
    dag=dag
)

start >> cre_db >> stop
