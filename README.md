# Airflow E2E Pipeline: Currency Rates API → PostgreSQL → Email

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

Этот проект демонстрирует E2E-пайплайн оркестрации данных с использованием Apache Airflow. DAG автоматически забирает курсы валют через REST API, сохраняет их в PostgreSQL и отправляет уведомление на Email.

## Архитектура

Текстовое описание пайплайна:

- REST API (open.er-api.com) -> PythonOperator (fetch_currency_rates)
- PythonOperator -> PostgreSQL (таблица currency_rates)
- PythonOperator -> EmailOperator (send_email) -> SMTP Mail.ru

## Стек технологий

- Оркестрация: Apache Airflow 2.8.1 (Docker)
- Язык: Python 3.11
- База данных: PostgreSQL 15
- Библиотеки: requests, psycopg2, airflow.providers.smtp

## Скриншоты работы

**1. Успешное выполнение DAG в Airflow:**
![Graph](01_dag_graph_success.png)

**2. Лог выполнения задачи fetch_currency_rates:**
![Task Log](04_task_log.png)

**3. Данные в PostgreSQL (pgAdmin):**
![PostgreSQL](05_postgres_data.png)

**4. Результат отправки Email:**

![Email](07_email_result.png)

## Как запустить локально

1. Установите Docker и Docker Compose.
2. Выполните `docker compose up -d`.
3. Откройте Airflow UI по адресу http://localhost:8080, включите DAG и нажмите Trigger DAG.
