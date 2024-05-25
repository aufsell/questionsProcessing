from datetime import datetime
from pydantic import BaseModel, field_validator, Field


class MessageValidator(BaseModel):
    # Fields of the Message model
    appeal_id: int
    sender_id: int
    sender_is_admin: bool
    message_text: str
    created_at: datetime = Field(default_factory=datetime.now)

    # Check that the message is not empty
    @field_validator('message_text')
    def validate_message_text(cls, v):
        if not v.strip():
            raise ValueError('Сообщение не может быть пустым')
        return v
