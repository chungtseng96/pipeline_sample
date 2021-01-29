# Objective: To create a DAG template for Airflow
# Step 1: Import Packages (Airflow, DAG, operators, trigger rules)
# Step 2: Define arguements 
    # 1. Default Arguments - Start_date, email_on_failure, email_on_retry, retries, etc.
    # 2. DAG Specific - Define any variables that the DAG will reference 
# Step 3: Set up 
    # Give DAG a name
    # configure the schedule - SET SCHEDULE INTERVAL HERE 
    # Set SAG settings 
# Step 4: Tasks - Actually coding out the DAG
    # Use google operator catalog to understand how to perform tasks in Airflow
# Step 5: Ordering - Ordering the task in logical order 

# Step 1: Import Packages 
from datetime import timedelta
import os 

import airflow
from airflow import DAG
from airflow import models
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateEmptyDatasetOperator,
    BigQueryDeleteDatasetOperator
)
from airflow.operators.python_operator import PythonOperator
from google.cloud import bigquery
from google.cloud import storage
import airflow.contrib.operators.bigquery_operator 
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.contrib.operators.dataflow_operator import DataflowTemplateOperator
from airflow.utils.dates import days_ago

# Step 2: Define arguments

default_args = {
    'owner': 'James',
    'depends_on_past': False,
    'email': ['chungtseng96@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay':timedelta(minutes=5),
    'start_date': airflow.utils.dates.days_ago(5)
}

CONNECTION_ID = 'lunar-airport-298818'
with models.DAG(
    dag_id='Sample_v2',
    default_args = default_args,
    start_date=days_ago(2),
    # Can either set schdule or external trigger
    schedule_interval='0 * * * *',
    tags=['example'],
    # Need to set path for where the SQL file will be
    template_searchpath=['/home/airflow/gcs/dags/']) as dag:
    
    # Must be in DAG folder
    query_path = '/SQL/testing.sql'

    big_query_transform = airflow.contrib.operators.bigquery_operator.BigQueryOperator(
        task_id='query_fam',
        sql= query_path,
        destination_dataset_table= 'lunar-airport-298818:sample.fam_testing_v2',
        # Analyze which options makes the most sense. Can use DDL with Write_truncate
        write_disposition='WRITE_TRUNCATE',
        bigquery_conn_id='google_cloud_default',
        use_legacy_sql=False,
        dag=dag
    )
    
    big_query_transform

