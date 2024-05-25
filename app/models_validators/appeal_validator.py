from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, field_validator


class AppealStatus(str, Enum):
    OPEN = 'open'
    PENDING = 'pending'
    CLOSED = 'closed'


class AppealValidator(BaseModel):
    # Fields of the Appeal model
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    status: AppealStatus
    responded_admins: List[int] = []

    # Set to the current default time if not specified
    @field_validator(
            'created_at', 'updated_at', 'closed_at',
            pre=True, always=True
            )
    def set_default_datetime(cls, v):
        return v or datetime.now()

    # List responded_admins must be a list of integers
    @field_validator('responded_admins', each_item=True)
    def check_responded_admins(cls, v):
        if not isinstance(v, int):
            raise ValueError('Each responded admin ID must be an integer.')
        return v

    # Closed_at can only be set if status is CLOSED
    @field_validator('closed_at')
    def validate_closed_at(cls, v, values):
        if v and values.get('status') != AppealStatus.CLOSED:
            raise ValueError('closed_at can only be set if status is CLOSED.')
        return v
    