from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

class MessageBase(BaseModel):
    device_id: int
    data: Dict[str, Any]
    message_read_date: datetime
    is_synced_remotely: Optional[bool] = False
    active: Optional[bool] = True

class MessageCreate(MessageBase):
    pass

class MessageRead(MessageBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
