import json
import logging
from paho.mqtt import client as mqtt_client

from app.config.mqtt_config import ACTIVATION_MQTT_TOPIC, MQTT_BROKER, MQTT_PORT

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def on_connect(client, userdata, flags, rc):
    """
    Callback executado quando o cliente conecta ao broker MQTT.

    Args:
        client: Instância do cliente MQTT.
        userdata: Dados definidos pelo usuário.
        flags: Flags de resposta enviadas pelo broker.
        rc: Código de resultado da conexão.
    """
    if rc == 0:
        logger.info("✅ Conectado ao broker MQTT com sucesso.")
        client.subscribe(ACTIVATION_MQTT_TOPIC)
    else:
        logger.error(f"❌ Falha na conexão, código de retorno: {rc}")


def on_message(client, userdata, msg):
    """
    Callback executado quando uma mensagem é recebida no tópico inscrito.

    Args:
        client: Instância do cliente MQTT.
        userdata: Dados definidos pelo usuário.
        msg: Mensagem MQTT recebida.
    """
    try:
        payload = json.loads(msg.payload.decode())
        logger.info(f"📩 Mensagem recebida no tópico {msg.topic}: {payload}")
        # Aqui você pode processar a mensagem recebida
    except json.JSONDecodeError as e:
        logger.error(f"❌ Erro ao decodificar JSON: {e}")


def start_mqtt_webhook():
    """
    Inicia o consumidor MQTT para se conectar ao broker e ouvir mensagens.
    """
    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_log = lambda client, userdata, level, buf: logger.debug(f"Log: {buf}")

    try:
        logger.info("🔌 Tentando conectar ao broker MQTT...")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_forever()
    except Exception as e:
        logger.error(f"❌ Erro ao conectar ao broker MQTT: {e}")


if __name__ == "__main__":
    start_mqtt_webhook()