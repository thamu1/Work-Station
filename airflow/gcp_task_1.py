from airflow import DAG
from airflow.contrib.operators.bigquery_to_gcs import BigQueryToGoogleCloudStorageOperator
from airflow.operators.bigquery import BigQueryExecuteQueryOperator
from airflow.operators.python import PythonOperator
from airflow.utils import apply_defaults
from datetime import datetime , timedelta

def extract_data_from_bigquery(**kwargs):
    # Extract data from BigQuery and save it to a local file
    pass

def upload_data_to_gcs(**kwargs):
    # Upload the data from the local file to Google Cloud Storage
    pass

# Define the default_args dictionary for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Instantiate the DAG object
dag = DAG(
    'bigquery_to_gcs',
    default_args=default_args,
    description='Transfer data from BigQuery to Google Cloud Storage',
    schedule_interval=timedelta(hours=1)
)



# Define the BigQueryToGoogleCloudStorageOperator
extract_data = BigQueryToGoogleCloudStorageOperator(
    task_id='extract_data',
    source_project_dataset_table='your-project.your-dataset.your-table',
    destination_cloud_storage_uris=['gs://your-bucket/your-file.csv'],
    export_format='CSV',
    dag=dag
)

# Define the PythonOperator
upload_data = PythonOperator(
    task_id='upload_data',
    python_callable=upload_data_to_gcs,
    dag=dag
)

# Set the task dependencies
extract_data >> upload_data
