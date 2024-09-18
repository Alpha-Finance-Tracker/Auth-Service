import pytest

from login_app.api.services.auth_service import AuthService
from login_app.utils.responses import *
from tests.mocked_data import *


@pytest.mark.asyncio
async def test_authenticate_user_when_email_does_not_exist(mocker):
    mocker.patch('login_app.database.models.user.User.get_user',
                 mocker.AsyncMock(return_value=None))

    with pytest.raises(NotFound) as e:
        await AuthService(mock_login['username'], mock_login['password']).authenticate()

    assert isinstance(e.value, NotFound)


@pytest.mark.asyncio
async def test_authenticate_user_when_password_is_wrong(mocker):
    user = MockUserFromDBData()
    mocker.patch('login_app.database.models.user.User.get_user',
                 mocker.AsyncMock(return_value=user))

    mocker.patch('login_app.api.services.auth_service.bcrypt.checkpw',
                 mocker.MagicMock(return_value=False))

    with pytest.raises(NotFound) as e:
        await AuthService(mock_login['username'], mock_login['password']).authenticate()

    assert isinstance(e.value, NotFound)


@pytest.mark.asyncio
async def test_authenticate_user_when_password_is_correct(mocker):
    user = MockUserFromDBData()
    mocker.patch('login_app.database.models.user.User.get_user',
                 mocker.AsyncMock(return_value=user))

    mocker.patch('login_app.api.services.auth_service.bcrypt.checkpw',
                 mocker.MagicMock(return_value=True))

    result = await AuthService(mock_login['username'], mock_login['password']).authenticate()
    assert result == user


@pytest.mark.asyncio
async def test_register_user_when_email_already_exists(mocker):
    user = MockUserFromDBData()
    mocker.patch('login_app.database.models.user.User.get_user',
                 mocker.AsyncMock(return_value=user))

    with pytest.raises(EmailExists) as e:
        await AuthService(mock_login['username'], mock_login['password']).register()

    assert isinstance(e.value, EmailExists)


@pytest.mark.asyncio
async def test_register_user_when_email_does_not_exist(mocker):
    mocker.patch('login_app.database.models.user.User.get_user',
                 mocker.AsyncMock(return_value=None))

    mocker.patch('login_app.api.services.auth_service.bcrypt.checkpw')

    mocker.patch('login_app.database.models.user.User.register',
                 mocker.AsyncMock(return_value={"message": "User registered successfully!"}))

    result = await AuthService(mock_login['username'], mock_login['password']).register()
    assert isinstance(result, dict)
