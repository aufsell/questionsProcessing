from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class AppealValidator(BaseModel):
    # Fields of the Appeal model
    name: str = 'Без темы'
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    status: str = 'Open'
    responded_admins: List[int] = []

    # Set to the current default time if not specified
    @field_validator('created_at', 'updated_at', 'closed_at')
    def set_default_datetime(cls, v):
        return v or datetime.now()

    # List responded_admins must be a list of integers
    @field_validator('responded_admins')
    def check_responded_admins(cls, v):
        for admin_id in v:
            if not isinstance(admin_id, int):
                raise ValueError('Each responded admin ID must be an integer.')
        return v

    # Closed_at can only be set if status is CLOSED
    @field_validator('closed_at')
    def validate_closed_at(cls, v, values):
        if v and getattr(values, 'status', '') != 'CLOSED':
            raise ValueError('closed_at can only be set if status is CLOSED.')
        return v
