import pytest
from jose import JWTError

from login_app.api.auth_services import authenticate_user, register_user, verify_access_token_service, \
    verify_refresh_token_service
from login_app.utils.responses import NotFound, EmailExists, Unauthorized
from tests.mocked_data import auth_data, mock_payload, mock_token, mock_user_db_information


@pytest.mark.asyncio
async def test_authenticate_user_when_email_does_not_exist(mocker):
    mocker.patch('login_app.api.auth_services.read_query', mocker.AsyncMock(return_value=[]))

    with pytest.raises(NotFound) as e:
        await authenticate_user(auth_data['username'], auth_data['password'])

    assert isinstance(e.value, NotFound)


@pytest.mark.asyncio
async def test_authenticate_user_when_password_is_wrong(mocker):
    mocker.patch('login_app.api.auth_services.read_query', mocker.AsyncMock(return_value=[]))
    mocker.patch('login_app.api.auth_services.bcrypt.checkpw', mocker.MagicMock(return_value=False))

    with pytest.raises(NotFound) as e:
        await authenticate_user(auth_data['username'], auth_data['password'])

    assert isinstance(e.value, NotFound)


@pytest.mark.asyncio
async def test_authenticate_user_when_correct_password(mocker):
    mocker.patch('login_app.api.auth_services.read_query', mocker.AsyncMock(return_value=mock_user_db_information))
    mocker.patch('login_app.api.auth_services.bcrypt.checkpw', mocker.MagicMock(return_value=True))

    result = await authenticate_user(auth_data['username'], auth_data['password'])

    assert result == mock_user_db_information

@pytest.mark.asyncio
async def test_register_user_when_email_already_exists(mocker):
    mocker.patch('login_app.api.auth_services.read_query', mocker.AsyncMock(return_value=auth_data))

    with pytest.raises(EmailExists) as e:
        await register_user(auth_data['username'], auth_data['password'])

    assert isinstance(e.value,EmailExists)

@pytest.mark.asyncio
async def test_register_user_when_email_does_not_exist(mocker):
    mocker.patch('login_app.api.auth_services.read_query', mocker.AsyncMock(return_value=None))
    mocker.patch('login_app.api.auth_services.bcrypt.checkpw')
    mocker.patch('login_app.api.auth_services.update_query')

    result = await register_user(auth_data['username'], auth_data['password'])
    assert isinstance(result,dict)

@pytest.mark.asyncio
async def test_verify_absent_access_token():
    with pytest.raises(Unauthorized) as e :
        await verify_access_token_service(None)

    assert isinstance(e.value,Unauthorized)

@pytest.mark.asyncio
async def test_verify_expired_access_token(mocker):

    mocker.patch('login_app.api.auth_services.jwt.decode', mocker.MagicMock(side_effect=JWTError("Token is invalid")))

    with pytest.raises(Unauthorized) as e:
        await verify_access_token_service(mock_token)

    assert isinstance(e.value,Unauthorized)

@pytest.mark.asyncio
async def test_verify_valid_access_token(mocker):
    mocker.patch('login_app.api.auth_services.jwt.decode', mocker.MagicMock(return_value = mock_payload))
    result = await verify_access_token_service(mock_token)
    assert result == mock_token


@pytest.mark.asyncio
async def test_verify_absent_refresh_token():
    with pytest.raises(Unauthorized) as e :
        await verify_refresh_token_service(None)

    assert isinstance(e.value,Unauthorized)

@pytest.mark.asyncio
async def test_verify_invalid_refresh_token(mocker):
    mocker.patch('login_app.api.auth_services.jwt.decode', mocker.MagicMock(side_effect=JWTError("Token is invalid")))

    with pytest.raises(Unauthorized) as e:
        await verify_refresh_token_service(mock_token)

    assert isinstance(e.value,Unauthorized)

@pytest.mark.asyncio
async def test_verify_valid_refresh_token(mocker):
    mocker.patch('login_app.api.auth_services.jwt.decode', mocker.MagicMock(return_value=mock_payload))
    result = await verify_refresh_token_service(mock_token)

    assert isinstance(result,dict)


