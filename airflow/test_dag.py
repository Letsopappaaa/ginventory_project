import datetime
from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.postgres_operator import PostgresOperator

dag = DAG(
    "create_simple_table",
    catchup=False,
    start_date=datetime.datetime.utcnow())

create_table = PostgresOperator(
    task_id="create_table",
    dag=dag,
    sql="""CREATE TABLE IF NOT EXISTS perfect_garnishes (id INTEGER,perfect_garnish_id INTEGER);""",
    postgres_conn_id="redshift")

create_table