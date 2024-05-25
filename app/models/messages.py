from tortoise import fields

from base_model import BaseModel


class Message(BaseModel):
    appeal = fields.ForeignKeyField(
        'models.Appeals',
        related_name='messages_appels'
        )
    sender = fields.ForeignKeyField(
        'models.Users',
        related_name='messages_user'
        )
    sender_is_admin = fields.BooleanField(default=False)
    message_text = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} in Appeal {self.inquiry.id}"
