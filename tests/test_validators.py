from datetime import datetime

import pytest

from app.models_validators.appeal_validator import AppealValidator
from app.models_validators.message_validator import MessageValidator
from app.models_validators.users_validator import UserValidator


@pytest.fixture
def valid_appeal_data():
    return {
        "name": "Test Appeal",
        "created_at": datetime.now(),
        "status": "Open",
        "responded_admins": [1, 2, 3]
    }


@pytest.fixture
def valid_user_data():
    return {
        "name": "John",
        "last_name": "Doe",
        "phone_number": "79123456789",
        "username": "johndoe",
        "is_admin": False,
        "is_active": True,
        "is_banned": False
    }


def test_valid_appeal(valid_appeal_data):
    assert AppealValidator(**valid_appeal_data)


def test_invalid_responded_admins():
    with pytest.raises(ValueError):
        appeal_data = {
            "name": "Test Appeal",
            "created_at": datetime.now(),
            "status": "Open",
            "responded_admins": [1, "invalid_id", 3]
        }
        AppealValidator(**appeal_data)


def test_invalid_status_with_closed_at():
    with pytest.raises(ValueError):
        appeal_data = {
            "name": "Test Appeal",
            "created_at": datetime.now(),
            "status": "Open",
            "closed_at": datetime.now()
        }
        AppealValidator(**appeal_data)


def test_invalid_created_at_type():
    with pytest.raises(ValueError):
        appeal_data = {
            "name": "Test Appeal",
            "created_at": "invalid_datetime",
            "status": "Open",
            "responded_admins": [1, 2, 3]
        }
        AppealValidator(**appeal_data)


def test_invalid_closed_at_type():
    with pytest.raises(ValueError):
        appeal_data = {
            "name": "Test Appeal",
            "created_at": datetime.now(),
            "status": "CLOSED",
            "closed_at": "invalid_datetime"
        }
        AppealValidator(**appeal_data)


def test_valid_user(valid_user_data):
    assert UserValidator(**valid_user_data)


def test_invalid_phone_number():
    with pytest.raises(ValueError):
        user_data = {
            "name": "John",
            "last_name": "Doe",
            "phone_number": "invalid_number",
            "username": "johndoe",
            "is_admin": False,
            "is_active": True,
            "is_banned": False
        }
        UserValidator(**user_data)


def test_invalid_name_length():
    with pytest.raises(ValueError):
        user_data = {
            "name": "A" * 40,
            "last_name": "Doe",
            "phone_number": "79123456789",
            "username": "johndoe",
            "is_admin": False,
            "is_active": True,
            "is_banned": False
        }
        UserValidator(**user_data)


def test_valid_message():
    message = MessageValidator(
        appeal_id=1,
        sender_id=1,
        sender_is_admin=False,
        message_text="Test message"
    )
    assert message


def test_invalid_empty_message():
    with pytest.raises(ValueError):
        message = MessageValidator(
            appeal_id=1,
            sender_id=1,
            sender_is_admin=False,
            message_text=""
        )
        assert message


def test_invalid_empty_message_with_whitespace():
    with pytest.raises(ValueError):
        message = MessageValidator(
            appeal_id=1,
            sender_id=1,
            sender_is_admin=False,
            message_text="   "
        )
        assert message
