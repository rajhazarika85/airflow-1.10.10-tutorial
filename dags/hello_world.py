from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import timedelta
import yaml

# Load default_args from config.yml
with open("dags/config.yml", "r") as config_file:
    config = yaml.safe_load(config_file)

# Instantiate the DAG
dag = DAG(
    'hello_world_dag',
    default_args=config.get('default_args', {}),
    description='A simple DAG for Airflow 1.10.10',
    schedule_interval=timedelta(days=1),  # Set the frequency at which the DAG should run
)

# Define the Python function that will be executed by the task
def hello_world():
    print("Hello, World!")

# Instantiate the PythonOperator and specify the function to run
hello_world_task = PythonOperator(
    task_id='hello_world_task',
    python_callable=hello_world,
    dag=dag,
)

# Set the task dependency; the hello_world_task should run after the DAG is triggered
hello_world_task

