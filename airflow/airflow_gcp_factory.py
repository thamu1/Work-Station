"""
Code Author: Prashant Basa
Code Developed Date: 2021-08-03
Code Modified Date : 2021-09-30

This file has the list of all the functions used in the dag compute process

If any custom function if you feel is used in many places, we can have it placed here
"""

from airflow import macros
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from airflow.contrib.operators.ssh_operator import SSHOperator
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.contrib.operators.bigquery_to_bigquery import BigQueryToBigQueryOperator
from airflow.contrib.operators.gcs_to_gcs import GoogleCloudStorageToGoogleCloudStorageOperator
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.contrib.operators.gcs_delete_operator import GoogleCloudStorageDeleteOperator
from airflow.contrib.operators.bigquery_operator import BigQueryCreateExternalTableOperator

from airflow.exceptions import AirflowException
from airflow.models import Variable

from bigdata_plugins.operators import BigDataCountCheckOperator
from bigdata_plugins.operators import BigDataCountFailureOperator
from bigdata_plugins.operators import BQViewCreateAuthorizeOperator
from bigdata_plugins.operators import BQPartitionCountValidateOperator
from bigdata_plugins.operators import BQOnlinePartitionCountValidateOperator
from bigdata_plugins.operators import BQOnlineCountValidateOperator
from airflow.models import DAG
from datetime import timedelta
from datetime import date
from airflow.operators.mysql_operator import MySqlOperator
import mysql.connector
import os

def mysql_select_exec(query, host_name, usr, pwd, db_name):
    try:
        con = mysql.connector.connect(user=str(usr), password=str(pwd), host=host_name, database=str(db_name))
        cursor = con.cursor()
    except mysql.connector.Error as err:
        raise Exception
    else:
        query = cursor.execute(f"{query}")
        return cursor.fetchall()
    finally:
        cursor.close()
        con.close()

def mysql_update_insert_exec(query, host_name, usr, pwd, db_name):
    try:
        con = mysql.connector.connect(user=str(usr), password=str(pwd), host=host_name, database=str(db_name))
        cursor = con.cursor()
    except mysql.connector.Error as err:
        raise Exception
    else:
        query = cursor.execute(f"{query}")
        con.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        con.close()

def gcp_bq_to_bq_load_sqltask(exec_order_task, gcp_conn_var, gcp_schema_initial, bq_initial_tblname,
                           gcp_schema_target, bq_target_tblname, gcp_partition_cols, gcp_cluster_cols,
                           dag,write_disposition="WRITE_TRUNCATE",create_disposition="CREATE_IF_NEEDED"):
    task_id = exec_order_task + "_" + bq_target_tblname + '_' + "gcp_BqToBqLoadSQLTask"
    return BigQueryOperator(
        task_id=task_id,
        bigquery_conn_id=gcp_conn_var,
        destination_dataset_table=gcp_schema_target + '.' + bq_target_tblname,
        use_legacy_sql=False,
        sql=f"select * from {gcp_schema_initial}.{bq_initial_tblname}",
        time_partitioning=gcp_partition_cols,
        cluster_fields=gcp_cluster_cols,
        write_disposition=write_disposition,
        create_disposition=create_disposition,
        retries=1,
        retry_delay=timedelta(seconds=10),
        dag=dag
    )


def gcp_bq_obj_count_check(exec_order_task, gcp_svc_account_json_path, gcp_schema_target, object_name, dag ):
    task_id = exec_order_task + "_" + object_name + '_' + "gcp_BQObjCountCheck"
    return BQOnlineCountValidateOperator(
        task_id=task_id,
        svc_account_json_path=Variable.get(gcp_svc_account_json_path),
        dataset_table_name=gcp_schema_target + "." + object_name,
        retries=1,
        retry_delay=timedelta(seconds=10),
        dag=dag
    )


def gcp_bq_to_bq_load(exec_order_task, gcp_conn_var, gcp_schema_initial, bq_initial_tblname
                      , gcp_schema_target, bq_target_tblname, dag, write_disposition="WRITE_TRUNCATE"):
    task_id = exec_order_task + "_" + bq_target_tblname + '_' + "gcp_BQToBQLoad"
    return BigQueryToBigQueryOperator(
        task_id=task_id,
        bigquery_conn_id=gcp_conn_var,
        source_project_dataset_tables=gcp_schema_initial + "." + bq_initial_tblname,
        destination_project_dataset_table=gcp_schema_target + "." + bq_target_tblname,
        write_disposition=write_disposition,
        retries=1,
        retry_delay=timedelta(seconds=10),
        dag=dag
    )


def gcp_mysqlDMLOperator(exec_order_task, object_name, dml_sql, gcp_mysql_conn, dag):
    task_id = exec_order_task + "_" + object_name + '_' + "gcp_MySQLInsertTask"
    return MySqlOperator(
        task_id=task_id,
        sql=dml_sql,
        mysql_conn_id=gcp_mysql_conn,
        autocommit=True,
        dag=dag
    )

def gcp_FromExtSQLFileToBQObj(exec_order_task, object_name, gcp_conn_var, project_name, dest_tbl_schema, dest_tbl_name
                              , partitionedCols, clusterFields, sql_loc, dag, write_disposition="WRITE_TRUNCATE"
                              , create_disposition="CREATE_IF_NEEDED"):
    task_id = exec_order_task + "_" + object_name + '_' + "gcp_FinalObjectLoad"
    return BigQueryOperator(
        task_id=task_id,
        bigquery_conn_id=gcp_conn_var,
        destination_dataset_table=project_name + ":" + dest_tbl_schema + "." + dest_tbl_name,
        use_legacy_sql=False,
        sql=sql_loc+".sql",
        write_disposition=write_disposition,
        create_disposition=create_disposition,
        time_partitioning=partitionedCols,
        cluster_fields=clusterFields,
        retries=1,
        retry_delay=timedelta(seconds=10),
        dag=dag
    )


def gcp_FromExtSQLFileExecQuery(exec_order_task, object_name, sql_loc, gcp_conn_var, dag):
    task_id = exec_order_task + "_" + object_name + '_' + "gcp_FinalObjectLoad"
    return BigQueryOperator(
        task_id=task_id,
        bigquery_conn_id=gcp_conn_var,
        use_legacy_sql=False,
        sql=sql_loc+".sql"
        , retries=1
        , retry_delay=timedelta(seconds=10)
        ,dag=dag
    )


def gcp_FromExtSQLFileToBQObj_Append(exec_order_task, object_name, gcp_conn_var, project_name, dest_tbl_schema, dest_tbl_name
                              , partitionedCols, clusterFields, sql_loc, dag, write_disposition="WRITE_APPEND"):
    task_id = exec_order_task + "_" + object_name + '_' + "gcp_FinalObjectLoad"
    return BigQueryOperator(
        task_id=task_id,
        bigquery_conn_id=gcp_conn_var,
        destination_dataset_table=project_name + ":" + dest_tbl_schema + "." + dest_tbl_name,
        use_legacy_sql=False,
        sql=sql_loc+".sql",
        write_disposition=write_disposition,
        time_partitioning=partitionedCols,
        cluster_fields=clusterFields,
        retries=1,
        retry_delay=timedelta(seconds=10),
        dag=dag
    )


def gcp_bq_to_bq_load_append(exec_order_task, gcp_conn_var, gcp_schema_initial, bq_initial_tblname
                      , gcp_schema_target, bq_target_tblname, dag, write_disposition="WRITE_APPEND"):
    task_id = exec_order_task + "_" + bq_target_tblname + '_' + "gcp_BQToBQLoad"
    return BigQueryToBigQueryOperator(
        task_id=task_id,
        bigquery_conn_id=gcp_conn_var,
        source_project_dataset_tables=gcp_schema_initial + "." + bq_initial_tblname,
        destination_project_dataset_table=gcp_schema_target + "." + bq_target_tblname,
        write_disposition=write_disposition,
        retries=1,
        retry_delay=timedelta(seconds=10),
        dag=dag
    )

def gcp_bq_to_bq_copy_partition(exec_order_task, gcp_conn_var, gcp_schema_initial, bq_initial_tblname
                                , gcp_schema_target, bq_target_tblname, partition_value, dag):
    return BigQueryToBigQueryOperator(
        task_id = exec_order_task + "_" + bq_target_tblname + '_' + "gcp_BQToBQCopyPartitions",
        bigquery_conn_id=gcp_conn_var,
        source_project_dataset_tables= gcp_schema_initial + "." + bq_initial_tblname + '$' + partition_value,
        destination_project_dataset_table= gcp_schema_target + "." + bq_target_tblname + '$' + partition_value,
        write_disposition="WRITE_TRUNCATE",
        dag=dag
    )

def gcp_bq_to_bq_copy_entire_table(exec_order_task, gcp_conn_var, gcp_schema_initial, bq_initial_tblname
                                , gcp_schema_target, bq_target_tblname, dag):
    return BigQueryToBigQueryOperator(
        task_id = exec_order_task + "_" + bq_target_tblname + '_' + "gcp_BQToBQCopyPartitions",
        bigquery_conn_id=gcp_conn_var,
        source_project_dataset_tables= gcp_schema_initial + "." + bq_initial_tblname,
        destination_project_dataset_table= gcp_schema_target + "." + bq_target_tblname,
        write_disposition="WRITE_TRUNCATE",
        dag=dag
    )

def gcp_sql_exec_bq_append(exec_order_task, object_name, gcp_conn_var, project_name, dest_tbl_schema,
                           dest_tbl_name, sql_exec, dag, write_disposition="WRITE_APPEND",
                           create_disposition="CREATE_IF_NEEDED"):
    return BigQueryOperator(
        task_id=exec_order_task + "_" + object_name + "_bq_success_entry",
        sql=sql_exec,
        bigquery_conn_id=gcp_conn_var,
        destination_dataset_table=project_name + ":" + dest_tbl_schema + "." + dest_tbl_name,
        use_legacy_sql=False,
        write_disposition=write_disposition,
        create_disposition=create_disposition,
        retries=1,
        retry_delay=timedelta(seconds=10),
        dag=dag
    )

def gcsCleanupTask(objectName,GCP_CONN,gcp_sa_bucket, obj_bucket_path, subdag):
    task_id = objectName + '_' + "gcsCleanup_task"
    return GoogleCloudStorageDeleteOperator(
        task_id=task_id,
        google_cloud_storage_conn_id=GCP_CONN,
        bucket_name=gcp_sa_bucket,
        prefix=obj_bucket_path,
        dag=subdag,
        retries=1,
        retry_delay=timedelta(seconds=10)
    )

def distcpTask(objectName, source_path,destination_path,distcp_params, subdag):
    task_id = objectName + '_' + "distcp_task"
    cmd = "hadoop distcp {0} {1} {2}".format(distcp_params, source_path,destination_path)
    return BashOperator(
        task_id = task_id,
        bash_command=cmd,
        xcom_push=False,
        dag=subdag
    )
