from sqlalchemy.orm import Session
from app.db import models
from app.schemas import message

def create_message(db: Session, msg_data: message.MessageCreate):
    db_message = models.Message(**msg_data.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages(db: Session):
    return db.query(models.Message).filter(models.Message.deleted_at == None).all()

def get_message(db: Session, message_id: int):
    return db.query(models.Message).filter(models.Message.id == message_id).first()
