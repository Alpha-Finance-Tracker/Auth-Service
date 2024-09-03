import pytest
from login_app.api.auth_services import *
from login_app.utils.responses import *
from tests.mocked_data import *


@pytest.mark.asyncio
async def test_authenticate_user_when_email_does_not_exist(mocker):
    mocker.patch('login_app.api.auth_services.read_query', mocker.AsyncMock(return_value=[]))

    with pytest.raises(NotFound) as e:
        await authenticate_user(mock_login['username'], mock_login['password'])

    assert isinstance(e.value, NotFound)


@pytest.mark.asyncio
async def test_authenticate_user_when_password_is_wrong(mocker):
    mocker.patch('login_app.api.auth_services.read_query', mocker.AsyncMock(return_value=[]))
    mocker.patch('login_app.api.auth_services.bcrypt.checkpw', mocker.MagicMock(return_value=False))

    with pytest.raises(NotFound) as e:
        await authenticate_user(mock_login['username'], mock_login['password'])

    assert isinstance(e.value, NotFound)


@pytest.mark.asyncio
async def test_authenticate_user_when_correct_password(mocker):
    mocker.patch('login_app.api.auth_services.read_query',
                 mocker.AsyncMock(return_value=mock_authentication_db_user_info))
    mocker.patch('login_app.api.auth_services.bcrypt.checkpw', mocker.MagicMock(return_value=True))

    result = await authenticate_user(mock_login['username'], mock_login['password'])

    assert result == mock_authentication_db_user_info


@pytest.mark.asyncio
async def test_register_user_when_email_already_exists(mocker):
    mocker.patch('login_app.api.auth_services.read_query', mocker.AsyncMock(return_value=True))

    with pytest.raises(EmailExists) as e:
        await register_user(mock_login['username'], mock_login['password'])

    assert isinstance(e.value, EmailExists)


@pytest.mark.asyncio
async def test_register_user_when_email_does_not_exist(mocker):
    mocker.patch('login_app.api.auth_services.read_query', mocker.AsyncMock(return_value=None))
    mocker.patch('login_app.api.auth_services.bcrypt.checkpw')
    mocker.patch('login_app.api.auth_services.update_query')

    result = await register_user(mock_login['username'], mock_login['password'])
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_verify_absent_access_token():
    with pytest.raises(Unauthorized) as e:
        await verify_access_token_service(None)

    assert isinstance(e.value, Unauthorized)


@pytest.mark.asyncio
async def test_verify_expired_access_token(mocker):
    mocker.patch('login_app.api.auth_services.jwt.decode', mocker.MagicMock(side_effect=JWTError("Token is invalid")))

    with pytest.raises(Unauthorized) as e:
        await verify_access_token_service(invalid_token)

    assert isinstance(e.value, Unauthorized)


@pytest.mark.asyncio
async def test_verify_valid_access_token():
    result = await verify_access_token_service(valid_mock_access_token)
    assert result == valid_mock_access_token


@pytest.mark.asyncio
async def test_verify_absent_refresh_token():
    with pytest.raises(Unauthorized) as e:
        await verify_refresh_token_service(None)

    assert isinstance(e.value, Unauthorized)


@pytest.mark.asyncio
async def test_verify_invalid_refresh_token(mocker):
    mocker.patch('login_app.api.auth_services.jwt.decode', mocker.MagicMock(side_effect=JWTError("Token is invalid")))

    with pytest.raises(Unauthorized) as e:
        await verify_refresh_token_service(invalid_token)

    assert isinstance(e.value, Unauthorized)


@pytest.mark.asyncio
async def test_verify_valid_refresh_token():
    result = await verify_refresh_token_service(valid_mock_refresh_token)

    assert isinstance(result, dict)
