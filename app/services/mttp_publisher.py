import json
from paho.mqtt.client import Client

from app.config.mqtt_config import ACTIVATION_MQTT_TOPIC

def publish_message(client: Client, payload: dict):
    """
    Publish a message to the MQTT topic.

    Args:
        client (Client): The MQTT client instance.
        payload (dict): The JSON payload to be published.

    Returns:
        bool: True if the message was published successfully, False otherwise.
    """
    try:
        message = json.dumps(payload)
        result = client.publish(ACTIVATION_MQTT_TOPIC, message)
        return result.rc == 0
    except Exception as e:
        raise RuntimeError(f"Error publishing message: {e}")