import json
import time
import logging
from datetime import datetime
import paho.mqtt.client as mqtt
from sqlalchemy.orm import Session

from app.config.mqtt_config import MQTT_BROKER, MQTT_PORT, SENSOR_MQTT_TOPIC
from app.core.logs import setup_logger
from app.db.database import SessionLocal
from app.db import models

logger = setup_logger(__name__)

def create_db_session():
    """Create and return a new database session."""
    return SessionLocal()


def process_message(payload):
    """
    Process the received MQTT message payload and persist it to the database.

    Args:
        payload (dict): The decoded JSON payload from the MQTT message.
    """
    try:
        device_id = int(payload["device_id"])
        data = payload["data"]

        db: Session = create_db_session()
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


def on_connect(client, userdata, flags, rc):
    """
    Callback triggered when the MQTT client connects to the broker.

    Args:
        client: The MQTT client instance.
        userdata: User-defined data of any type.
        flags: Response flags sent by the broker.
        rc: The connection result.
    """
    if rc == 0:
        logger.info("✅ Conectado ao broker MQTT com sucesso.")
        client.subscribe(SENSOR_MQTT_TOPIC)
    else:
        logger.error(f"❌ Falha na conexão, código de retorno: {rc}")


def on_message(client, userdata, msg):
    """
    Callback triggered when a message is received on a subscribed topic.

    Args:
        client: The MQTT client instance.
        userdata: User-defined data of any type.
        msg: The MQTT message received.
    """
    logger.info(f"📩 Mensagem recebida em {msg.topic}: {msg.payload.decode()}")
    try:
        payload = json.loads(msg.payload.decode())
        process_message(payload)
    except json.JSONDecodeError as e:
        logger.error(f"❌ Erro ao decodificar JSON: {e}")


def start_mqtt_consumer():
    """
    Start the MQTT consumer to connect to the broker and listen for messages.
    """
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