FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-openbsd

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY run_mqtt_consumer.py ./ 
COPY run_mqtt_webhook.py ./ 

COPY ./wait-for-postgres.sh ./wait-for-postgres.sh
RUN chmod +x ./wait-for-postgres.sh

CMD ["/bin/sh", "-c", "./wait-for-postgres.sh && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
