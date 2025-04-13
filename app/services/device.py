from sqlalchemy.orm import Session
from app.db import models
from app.schemas import device

def create_device(db: Session, device_data: device.DeviceCreate):
    db_device = models.Device(**device_data.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def get_devices(db: Session):
    return db.query(models.Device).filter(models.Device.deleted_at == None).all()

def get_device(db: Session, device_id: int):
    return db.query(models.Device).filter(models.Device.id == device_id).first()
