# app/tests/crud/test_user.py

import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.crud.user import (
    get_user_by_username,
    get_user_by_id,
    get_user_by_email,
    get_all_users,
    create_user,
    delete_user
)
from app.db.models.user import User
from app.schemas.user import UserCreate

@pytest.fixture
def mock_user():
    return User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password="hashedpassword",
        full_name="Test User",
        is_active=True,
        is_superuser=False,
        created_at=datetime.utcnow()
    )

@pytest.fixture
def mock_user_create():
    return UserCreate(
        username="newuser",
        email="new@example.com",
        password="secret",
        full_name="New User"
    )

def test_get_user_by_username(mock_user):
    db = MagicMock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = mock_user
    
    result = get_user_by_username(db, "testuser")
    assert result == mock_user

def test_get_user_by_username_not_found():
    db = MagicMock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = None
    
    result = get_user_by_username(db, "nonexistent")
    assert result is None

def test_get_user_by_id(mock_user):
    db = MagicMock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = mock_user
    
    result = get_user_by_id(db, 1)
    assert result == mock_user

def test_get_user_by_email(mock_user):
    db = MagicMock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = mock_user
    
    result = get_user_by_email(db, "test@example.com")
    assert result == mock_user

def test_get_all_users(mock_user):
    db = MagicMock(spec=Session)
    db.query.return_value.all.return_value = [mock_user]
    
    result = get_all_users(db)
    assert len(result) == 1
    assert result[0] == mock_user

def test_create_user_success(mock_user_create):
    db = MagicMock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = None
    
    result = create_user(db, mock_user_create)
    assert result.username == mock_user_create.username
    assert result.email == mock_user_create.email
    assert result.full_name == mock_user_create.full_name
    assert result.is_active is True
    assert result.is_superuser is False
    assert db.add.called
    assert db.commit.called
    assert db.refresh.called

def test_create_user_username_exists(mock_user, mock_user_create):
    db = MagicMock(spec=Session)
    db.query.return_value.filter.return_value.first.side_effect = [mock_user, None]
    
    with pytest.raises(ValueError) as excinfo:
        create_user(db, mock_user_create)
    assert "Username already registered" in str(excinfo.value)

def test_create_user_email_exists(mock_user, mock_user_create):
    db = MagicMock(spec=Session)
    db.query.return_value.filter.return_value.first.side_effect = [None, mock_user]
    
    with pytest.raises(ValueError) as excinfo:
        create_user(db, mock_user_create)
    assert "Email already registered" in str(excinfo.value)

def test_delete_user_success(mock_user):
    db = MagicMock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = mock_user
    mock_current_user = MagicMock()
    mock_current_user.is_superuser = True
    
    result = delete_user(db, 1, mock_current_user)
    assert result is True
    assert db.delete.called
    assert db.commit.called

def test_delete_user_not_found():
    db = MagicMock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = None
    mock_current_user = MagicMock()
    mock_current_user.is_superuser = True
    
    result = delete_user(db, 999, mock_current_user)
    assert result is False

def test_delete_user_not_admin(mock_user):
    db = MagicMock(spec=Session)
    mock_current_user = MagicMock()
    mock_current_user.is_superuser = False
    
    with pytest.raises(HTTPException) as excinfo:
        delete_user(db, 1, mock_current_user)
    assert excinfo.value.status_code == status.HTTP_403_FORBIDDEN
    assert "Only admin users can delete accounts" in str(excinfo.value.detail)