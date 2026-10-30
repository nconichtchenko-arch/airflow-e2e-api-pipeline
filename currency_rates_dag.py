from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
import requests
import psycopg2
from psycopg2.extras import execute_values

API_URL = "https://open.er-api.com/v6/latest/USD"
# ВАЖНО: из контейнера Airflow PostgreSQL на Windows доступен по IP хоста (10.0.2.2)
DB_HOST = "10.0.2.2"
DB_PORT = "5432"
DB_NAME = "dwh_marketplace"
DB_USER = "dwh_user"
DB_PASSWORD = "dwh_password"
TARGET_CURRENCIES = ["RUB", "EUR", "CNY"]

def fetch_currency_rates():
    response = requests.get(API_URL, timeout=10)
    data = response.json()
    if data.get("result") != "success":
        raise Exception(f"API error: {data}")
    rates = data.get("rates", {})
    base = data.get("base_code", "USD")
    fetched_at = datetime.now()

    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD
    )
    conn.autocommit = True
    cur = conn.cursor()
    rows = []
    for curr in TARGET_CURRENCIES:
        rate = rates.get(curr)
        if rate:
            rows.append((base, curr, rate, fetched_at))
    execute_values(
        cur,
        "INSERT INTO currency_rates (base_currency, target_currency, rate, fetched_at) VALUES %s",
        rows
    )
    cur.close()
    conn.close()
    result_str = "\n".join([f"{r[0]}/{r[1]}: {r[2]}" for r in rows])
    print(f"Saved rates:\n{result_str}")
    return result_str

default_args = {
    'owner': 'pavel',
    'depends_on_past': False,
    'email': ['pavloni@mail.ru'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='currency_rates_pipeline',
    default_args=default_args,
    description='Загружает курсы валют и отправляет Email',
    schedule_interval='@daily',
    start_date=datetime(2026, 10, 30),
    catchup=False,
    tags=['currency', 'api', 'email'],
) as dag:
    fetch_task = PythonOperator(
        task_id='fetch_currency_rates',
        python_callable=fetch_currency_rates,
    )
    email_task = EmailOperator(
        task_id='send_email',
        to='pavloni@mail.ru',
        subject='Курсы валют (USD) на {{ ds }}',
        html_content="""
            <h3>Курсы валют на {{ ds }}</h3>
            <p><b>Данные из API:</b></p>
            <pre>{{ ti.xcom_pull(task_ids='fetch_currency_rates') }}</pre>
        """,
    )
    fetch_task >> email_task