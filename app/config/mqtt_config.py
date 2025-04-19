from paho.mqtt import client as mqtt_client

MQTT_BROKER = "mosquitto"  # Docker service name
MQTT_PORT = 1883
SENSOR_MQTT_TOPIC = "sensor/data"
ACTIVATION_MQTT_TOPIC = "sensor/activation"


def get_mqtt_client():
    """
    Initialize and return an MQTT client instance.
    """
    client = mqtt_client.Client()
    try:
        client.connect(MQTT_BROKER, MQTT_PORT)
    except Exception as e:
        raise RuntimeError(f"Failed to connect to MQTT broker: {e}")
    return client