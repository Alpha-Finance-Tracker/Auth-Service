import pytest


from login_app.utils.responses import *
from tests.mocked_data import *


@pytest.mark.asyncio
async def test_authenticate_user_when_email_does_not_exist(mocker):
    mocker.patch('login_app.models.user.read_query', mocker.AsyncMock(return_value=[]))

    with pytest.raises(NotFound) as e:
        await User(mock_login['username'], mock_login['password']).authenticate()

    assert isinstance(e.value, NotFound)


@pytest.mark.asyncio
async def test_authenticate_user_when_password_is_wrong(mocker):
    mocker.patch('login_app.models.user.read_query', mocker.AsyncMock(return_value=[]))
    mocker.patch('login_app.models.user.bcrypt.checkpw', mocker.MagicMock(return_value=False))

    with pytest.raises(NotFound) as e:
        await User(mock_login['username'], mock_login['password']).authenticate()

    assert isinstance(e.value, NotFound)


@pytest.mark.asyncio
async def test_authenticate_user_when_password_is_correct(mocker):
    mocker.patch('login_app.models.user.read_query', mocker.AsyncMock(return_value=mock_authentication_db_user_info))
    mocker.patch('login_app.models.user.bcrypt.checkpw', mocker.MagicMock(return_value=True))

    result = await User(mock_login['username'], mock_login['password']).authenticate()

    assert result == 1


@pytest.mark.asyncio
async def test_register_user_when_email_already_exists(mocker):
    mocker.patch('login_app.models.user.read_query', mocker.AsyncMock(return_value=True))

    with pytest.raises(EmailExists) as e:
        await User(mock_login['username'], mock_login['password']).register()

    assert isinstance(e.value, EmailExists)


@pytest.mark.asyncio
async def test_register_user_when_email_does_not_exist(mocker):
    mocker.patch('login_app.models.user.read_query', mocker.AsyncMock(return_value=None))
    mocker.patch('login_app.models.user.bcrypt.checkpw')
    mocker.patch('login_app.models.user.update_query')

    result = await User(mock_login['username'], mock_login['password']).register()
    assert isinstance(result, dict)
