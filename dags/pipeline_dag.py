from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="olist_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,  # manual trigger for now
    catchup=False,
    tags=["olist", "de-portfolio"],
) as dag:

    load_raw_data = BashOperator(
        task_id="load_raw_data",
        bash_command="python /opt/airflow/scripts/load_to_postgres.py",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/airflow/dbt_project/olist_analytics && dbt run --profiles-dir /opt/airflow/dbt_project",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/airflow/dbt_project/olist_analytics && dbt test --profiles-dir /opt/airflow/dbt_project",
    )

    load_raw_data >> dbt_run >> dbt_test