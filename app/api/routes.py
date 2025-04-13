from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services import device as device_crud, message as message_crud
from app.schemas import device as device_schema, message as message_schema
from app.api.deps import get_db

router = APIRouter()

@router.post("/devices/", response_model=device_schema.DeviceRead)
def create_device(device: device_schema.DeviceCreate, db: Session = Depends(get_db)):
    return device_crud.create_device(db, device)

@router.get("/devices/", response_model=list[device_schema.DeviceRead])
def read_devices(db: Session = Depends(get_db)):
    return device_crud.get_devices(db)

@router.post("/messages/", response_model=message_schema.MessageRead)
def create_message(message: message_schema.MessageCreate, db: Session = Depends(get_db)):
    return message_crud.create_message(db, message)

@router.get("/messages/", response_model=list[message_schema.MessageRead])
def read_messages(db: Session = Depends(get_db)):
    return message_crud.get_messages(db)
