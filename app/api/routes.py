import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.mqtt_config import get_mqtt_client
from app.schemas.mqtt import PublishPayload
from app.services import device as device_crud, message as message_crud
from app.schemas import device as device_schema, message as message_schema
from app.api.deps import get_db
from app.services.mttp_publisher import publish_message

router = APIRouter()
mqtt_client = get_mqtt_client()

@router.post("/devices/", response_model=device_schema.DeviceRead)
def create_device(device: device_schema.DeviceCreate, db: Session = Depends(get_db)):
    """
    Create a new device.
    Args:
        device (DeviceCreate): The device data to be created.
        db (Session): The database session.
    Returns:
        DeviceRead: The created device data.
    """ 
    return device_crud.create_device(db, device)

@router.get("/devices/", response_model=list[device_schema.DeviceRead])
def read_devices(db: Session = Depends(get_db)):
    """
    Get a list of all devices.
    Args:
        db (Session): The database session.
    Returns:
        list[DeviceRead]: A list of devices.
    """
    # Fetch all devices from the database
    # and return them as a list of DeviceRead schemas.
    return device_crud.get_devices(db)

@router.post("/messages/", response_model=message_schema.MessageRead)
def create_message(message: message_schema.MessageCreate, db: Session = Depends(get_db)):
    """
    Create a new message.
    Args:
        message (MessageCreate): The message data to be created.
        db (Session): The database session.
    Returns:
        MessageRead: The created message data.
    """
    return message_crud.create_message(db, message)

@router.get("/messages/", response_model=list[message_schema.MessageRead])
def read_messages(db: Session = Depends(get_db)):
    """
    Get a list of all messages.
    Args:
        db (Session): The database session.
    Returns:
        list[MessageRead]: A list of messages.
    """
    return message_crud.get_messages(db)

@router.post("/publish")
async def publish(payload: PublishPayload):
    """
    Endpoint to receive a payload and publish it to an MQTT topic.

    Args:
        payload (PublishPayload): The JSON payload to be published.

    Returns:
        dict: A response indicating success or failure.
    """
    try:
        success = publish_message(mqtt_client, payload.model_dump())
        if not success:
            logging.error("Failed to publish message to MQTT topic")
            raise HTTPException(status_code=500, detail="Failed to publish message to MQTT topic")
        return {"message": "Message published successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error publishing message: {e}")