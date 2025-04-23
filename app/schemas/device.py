from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class DeviceBase(BaseModel):
    name: str
    auth_token: Optional[str] = None
    active: Optional[bool] = True

class DeviceCreate(DeviceBase):
    pass

class DeviceRead(DeviceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
