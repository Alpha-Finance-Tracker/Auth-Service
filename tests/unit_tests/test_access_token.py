import pytest
from jose import JWTError

from login_app.models.access_token import AccessToken
from login_app.utils.responses import *
from tests.mocked_data import *


@pytest.mark.asyncio
async def test_verify_access_token_when_token_is_absent():
    with pytest.raises(Unauthorized) as e:
        await AccessToken(token=None, user_id=None).verify()

    assert isinstance(e.value, Unauthorized)


@pytest.mark.asyncio
async def test_verify_access_token_when_expired(mocker):
    mocker.patch('login_app.models.access_token.jwt.decode', mocker.MagicMock(side_effect=JWTError("Token is invalid")))

    with pytest.raises(Unauthorized) as e:
        await AccessToken(token=invalid_token, user_id=None).verify()

    assert isinstance(e.value, Unauthorized)


@pytest.mark.asyncio
async def test_verify_access_token_when_valid():
    result = await AccessToken(token=valid_mock_access_token, user_id=None).verify()
    assert result == valid_mock_access_token
