import json
import time
import logging
from datetime import datetime
import paho.mqtt.client as mqtt
from sqlalchemy.orm import Session

from app.core.logs import setup_logger
from app.db.database import SessionLocal
from app.db import models


logger = setup_logger(__name__)

MQTT_BROKER = "mosquitto"   # nome do serviço no docker-compose
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/data"  # ou outro tópico de sua escolha


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("✅ Conectado ao broker MQTT com sucesso.")
        client.subscribe(MQTT_TOPIC)
    else:
        logger.error(f"❌ Falha na conexão, código de retorno: {rc}")


def on_message(client, userdata, msg):
    logger.info(f"📩 Mensagem recebida em {msg.topic}: {msg.payload.decode()}")
    try:
        payload = json.loads(msg.payload.decode())
        device_id = int(payload["device_id"])
        data = payload["data"]

        db: Session = SessionLocal()
        message = models.Message(
            device_id=device_id,
            data=data,
            message_read_date=datetime.now(),
        )
        db.add(message)
        db.commit()
        logger.info("💾 Mensagem persistida com sucesso.")
    except Exception as e:
        logger.exception(f"❌ Erro ao processar mensagem: {e}")
    finally:
        if 'db' in locals():
            db.close()


def start_mqtt_consumer():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    while True:
        try:
            logger.info("🔌 Tentando conectar ao broker MQTT...")
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            client.loop_forever()
        except Exception as e:
            logger.warning(f"🔁 Reconnectando em 5s... Erro: {e}")
            time.sleep(5)
