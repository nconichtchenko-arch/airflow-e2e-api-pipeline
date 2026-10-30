# Airflow E2E Pipeline: Currency Rates API → PostgreSQL → Email

Этот проект демонстрирует end-to-end (E2E) пайплайн оркестрации данных с использованием **Apache Airflow**. 

DAG автоматически запускается по расписанию (ежедневно), забирает актуальные курсы валют через внешний REST API, сохраняет их в реляционную базу данных (PostgreSQL) и отправляет уведомление на Email.

## 🏗 Архитектура

```text
[open.er-api.com] (REST API)
       │
       │ HTTP GET
       ▼
[PythonOperator: fetch_currency_rates]
       │
       ├──▶ [PostgreSQL: currency_rates] (INSERT)
       │
       └──▶ [EmailOperator: send_email] ──(SMTP SSL)──▶ [Mail.ru Email]
```
🛠 Стек технологий
Оркестрация: Apache Airflow 2.8.1 (развернут в Docker, LocalExecutor)

Язык: Python 3.11

База данных: PostgreSQL 15

Библиотеки: requests (API), psycopg2 (PostgreSQL), airflow.providers.smtp (Email)

✨ Особенности реализации
Docker: Стек Airflow (webserver, scheduler, postgres) развернут через docker-compose.

Сетевое взаимодействие: Поскольку Airflow запущен в контейнере внутри VM, а PostgreSQL — на хосте Windows, для подключения используется IP-адрес 10.0.2.2 (VirtualBox NAT).

SMTP: Для отправки писем через Mail.ru настроен неявный SSL (порт 465), а STARTTLS отключен (STARTTLS=False), так как сервер его не поддерживает.

📂 Структура репозитория
dags/currency_rates_dag.py — код DAG (PythonOperator + EmailOperator).

docs/ — скриншоты работы пайплайна.

📸 Скриншоты работы
1. Успешное выполнение DAG в Airflow (Graph View):
https://01_dag_graph_success.png/

2. Лог выполнения задачи fetch_currency_rates:
https://04_task_log.png/

3. Данные, сохраненные в PostgreSQL (pgAdmin):
https://05_postgres_data.png/

4. Результат отправки Email (Mail.ru):
https://07_email_result.png/

🚀 Как запустить локально
Установите Docker и Docker Compose.

Клонируйте репозиторий.

Выполните docker compose up -d.

Откройте Airflow UI по адресу http://localhost:8080, включите DAG currency_rates_pipeline и нажмите Trigger DAG.

text
