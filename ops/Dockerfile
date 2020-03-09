FROM python:3.7-alpine
LABEL authors="Jayanta Kurumathur"

WORKDIR /app

RUN pip install --upgrade --user \
    PyYAML==5.1.1 \
    Jinja2==2.10.1 \
    google-cloud-bigquery==1.24.0

COPY python/generate_sql.py /app
COPY python/consolidated_events.sql.j2 /app

ENTRYPOINT ["python3.7", "/app/generate_sql.py"]
