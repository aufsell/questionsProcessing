from enum import Enum

from tortoise import fields

from base_model import BaseModel


class AppealStatus(Enum):
    OPEN = 'open'
    PENDING = 'pendind'
    CLOSED = 'closed'


class Appeal(BaseModel):
    # Appeal Model for DataBase
    # The request is linked to the user
    user = fields.ForeignKeyField('models.User', related_name='appeals_user')
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True, default=None)
    closed_at = fields.DatetimeField(auto_now=False)
    status = fields.CharEnumField(AppealStatus, default=AppealStatus.OPEN)
    # Field for storing the IDs of the administrators who responded to request
    responded_admins = fields.JSONField(default=list)

    def __str__(self):
        return f"Inquiry {self.id} by {self.user.username}"
