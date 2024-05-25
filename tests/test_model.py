import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.models import Base, User, Appeal, Message


@pytest.fixture(scope='function')
def session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


def test_add_user(session):
    new_user = User(name='John', last_name='Doe', username='johndoe')
    session.add(new_user)
    session.commit()

    user_in_db = session.query(User).filter_by(username='johndoe').first()
    assert user_in_db is not None
    print(f"User added: {user_in_db}")


def test_delete_user(session):
    new_user = User(name='John', last_name='Doe', username='johndoe')
    session.add(new_user)
    session.commit()

    session.delete(new_user)
    session.commit()

    user_in_db = session.query(User).filter_by(username='johndoe').first()
    assert user_in_db is None
    print(f"User deleted: {new_user}")


def test_add_user_and_message_without_appeal(session):
    new_user = User(name='John', last_name='Doe', username='johndoe')
    session.add(new_user)
    session.commit()

    new_message = Message(message_text='Test Message')
    session.add(new_message)
    with pytest.raises(Exception):
        session.commit()


def test_add_user_appeal_message_and_delete_them(session):
    new_user = User(name='John', last_name='Doe', username='johndoe')
    session.add(new_user)
    session.commit()

    new_appeal = Appeal(name='Test Appeal')
    new_appeal.users.append(new_user)
    session.add(new_appeal)
    session.commit()

    new_message = Message(message_text='Test Message', appeal=new_appeal)
    new_message.users.append(new_user)
    session.add(new_message)
    session.commit()

    session.delete(new_message)
    session.commit()

    session.delete(new_appeal)
    session.commit()

    session.delete(new_user)
    session.commit()

    message_in_db = session.query(Message).filter_by(
        message_text='Test Message'
        ).first()
    appeal_in_db = session.query(Appeal).filter_by(name='Test Appeal').first()
    user_in_db = session.query(User).filter_by(username='johndoe').first()

    assert message_in_db is None
    assert appeal_in_db is None
    assert user_in_db is None


def test_cascade_delete_message_with_appeal(session):
    new_user = User(name='John', last_name='Doe', username='johndoe')
    session.add(new_user)
    session.commit()

    new_appeal = Appeal(name='Test Appeal')
    new_appeal.users.append(new_user)
    session.add(new_appeal)
    session.commit()

    new_message = Message(message_text='Test Message', appeal=new_appeal)
    new_message.users.append(new_user)
    session.add(new_message)
    session.commit()

    session.delete(new_appeal)
    session.commit()

    appeal_in_db = session.query(Appeal).filter_by(name='Test Appeal').first()
    message_in_db = session.query(Message).filter_by(
        message_text='Test Message'
        ).first()

    assert appeal_in_db is None
    assert message_in_db is None
    print("Cascade delete test passed")
