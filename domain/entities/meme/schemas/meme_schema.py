import json
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, model_validator
from typing import Optional




class MemeInSchema(BaseModel):
    text: str
    photo: Optional[str | None] = None

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class MemeDeleteMethodSchema(BaseModel):
    id: uuid.UUID

class MemeOutSchema(BaseModel):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]
    text: str
    photo: str

    model_config = ConfigDict(from_attributes=True)