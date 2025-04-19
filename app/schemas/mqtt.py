from pydantic import BaseModel, Field

class PublishPayload(BaseModel):
    """
    Schema para validar o payload recebido no endpoint de publicação MQTT.
    """
    device_id: int = Field(..., description="ID do dispositivo que está enviando os dados")
    data: dict = Field(..., description="Dados enviados pelo dispositivo")

    class Config:
        schema_extra = {
            "example": {
                "device_id": 1,
                "data": {"irrigation_pump": True}
            }
        }