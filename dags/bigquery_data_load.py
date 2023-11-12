from airflow import DAG
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from datetime import timedelta
import yaml

# Load default_args from config.yml
with open("dags/config.yml", "r") as config_file:
    config = yaml.safe_load(config_file)

project_id = ''

# Instantiate the DAG
with DAG(
    'bigquery_data_load',
    default_args=config.get('default_args', {}),
    description='A DAG for bigquery data load',
    schedule_interval=timedelta(days=1),  # Set the frequency at which the DAG should run
) as dag:
    load_data = GoogleCloudStorageToBigQueryOperator(
        task_id='load_data',
        bucket='rh-airflow-landing-bucket',
        source_objects=['*'],
        source_format='CSV',
        skip_leading_rows=1,
        field_delimiter=',',
        destination_project_dataset_table=f'{project_id}.vehicle_analytics.history',
        create_disposition='CREATE_IF_NEEDED',
        write_disposition='WRITE_APPEND',
        bigquery_conn_id='google_cloud_default',
        google_cloud_storage_conn_id='google_cloud_default'
    )

    query = '''
        SELECT * except(rank)
        FROM (
            SELECT *, ROW_NUMBER() OVER (
                PARTITION BY vehicle_id ORDER BY DATETIME(date, TIME(hour, minute,0))
            ) as rank
            FROM
                `{project_id}.vehicle_analytics.history`
        ) as latest
        WHERE rank=1;
    '''

    create_table = BigQueryOperator(
        task_id='create_table',
        sql=query,
        destination_dataset_table=f'{project_id}.vehicle_analytics.latest',
        write_disposition='WRITE_TRUNCATE',
        create_disposition='CREATE_IF_NEEDED',
        use_legacy_sql=False,
        location='asia-south2',
        bigquery_conn_id='google_cloud_default'

    )


    load_data >> create_table