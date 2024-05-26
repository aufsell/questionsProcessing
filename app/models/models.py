from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.types import JSON, Boolean, Text
from sqlalchemy import ForeignKey, Table


Base = declarative_base()

users_appeals_association = Table(
    'users_appeals', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('appeal_id', Integer, ForeignKey('appeals.id'))
    )

users_messages_association = Table(
    'users_messages', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('message_id', Integer, ForeignKey('messages.id'))
    )


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(63), nullable=False)
    last_name = Column(String(63), nullable=False)
    phone_number = Column(String(15), default='')
    username = Column(String(63), default='')
    user_id = Column(String(63), default=0)
    password = Column(String(127), default='')
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_banned = Column(Boolean, default=False)

    appeals = relationship(
        "Appeal",
        secondary=users_appeals_association,
        back_populates="users"
        )
    messages = relationship(
        "Message",
        secondary=users_messages_association,
        back_populates="users"
        )

    def __str__(self):
        return (
            f"ID: {self.id},\n "
            f"Name: {self.name},\n "
            f"Last Name: {self.last_name},\n "
            f"Phone Number: {self.phone_number},\n "
            f"Username: {self.username},\n "
            f"Password: {self.password},\n "
            f"Is Admin: {self.is_admin},\n "
            f"Is Active: {self.is_active},\n "
            f"Is Banned: {self.is_banned},\n "
        )


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    message_text = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    users = relationship(
        "User",
        secondary=users_messages_association,
        back_populates="messages"
        )
    appeal_id = Column(Integer, ForeignKey('appeals.id'), nullable=False)
    appeal = relationship("Appeal", back_populates="messages")

    def __str__(self):
        return (
            f"ID: {self.id},\n "
            f"Message Text: {self.message_text},\n "
            f"Created At: {self.created_at},\n "
            f"Users: {self.users},\n "
            f"Appeal ID: {self.appeal_id},\n "
            f"Appeal: {self.appeal}"
        )


class Appeal(Base):
    __tablename__ = 'appeals'

    id = Column(Integer, primary_key=True)
    name = Column(String(127), default='Без темы')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    closed_at = Column(DateTime)
    status = Column(String(127), default='Open')
    responded_admins = Column(JSON, default=list)
    users = relationship(
        "User",
        secondary=users_appeals_association,
        back_populates="appeals"
        )
    messages = relationship(
        "Message",
        back_populates="appeal",
        cascade="all, delete-orphan"
        )

    def __str__(self):
        return (
            f"ID: {self.id},\n "
            f"Name: {self.name},\n "
            f"Created At: {self.created_at},\n "
            f"Updated At: {self.updated_at},\n "
            f"Closed At: {self.closed_at},\n "
            f"Status: {self.status},\n "
            f"Responded Admins: {self.responded_admins},\n "
            f"Users: {self.users},\n "
            f"Messages: {self.messages}"
        )
