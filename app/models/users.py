from tortoise import fields

from base_model import BaseModel


class User(BaseModel):
    # User model for Database
    name = fields.CharField(max_length=63, null=False)
    last_name = fields.CharField(max_length=63, null=False)
    phone_number = fields.CharField(default='')
    username = fields.CharField(max_length=63, default=None)
    password = fields.CharField(default='', max_length=127)
    is_admin = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=True)
    is_banned = fields.BooleanField(default=False)

    def __str__(self):
        return self.username
