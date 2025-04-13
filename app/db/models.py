from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.database import Base

class Device(Base):
    __tablename__ = "tb_device"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    auth_token = Column(String)
    active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
    deleted_at = Column(TIMESTAMP)

class Message(Base):
    __tablename__ = "tb_message"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("tb_device.id"), nullable=False)
    data = Column(JSON, default={})
    message_read_date = Column(TIMESTAMP, nullable=False)
    is_synced_remotely = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
    deleted_at = Column(TIMESTAMP)
