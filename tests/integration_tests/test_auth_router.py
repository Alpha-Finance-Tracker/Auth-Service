import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from login_app.api.auth_router import auth_router
from tests.mocked_data import auth_data, mock_user_db_information, registration_data, mock_payload, mock_token, \
    expiring_refresh_token_payload

app = FastAPI()
app.include_router(auth_router)


@pytest.mark.asyncio
async def test_unsuccessful_login_flow(mocker):
    mocker.patch('login_app.api.auth_services.read_query',mocker.AsyncMock(return_value=None))

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post('/login',data=auth_data)

        assert response.status_code == 404

@pytest.mark.asyncio
async def test_successful_login_flow(mocker):
    mocker.patch(f'login_app.api.auth_services.read_query',mocker.AsyncMock(return_value=mock_user_db_information))
    mocker.patch('login_app.api.auth_services.bcrypt.checkpw',mocker.MagicMock(return_value=True))

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post('/login',data=auth_data)

        assert response.status_code == 200

@pytest.mark.asyncio
async def test_unsuccessful_registration_flow(mocker):
    mocker.patch('login_app.api.auth_services.read_query',mocker.AsyncMock(return_value=mock_user_db_information))

    async with AsyncClient(app=app,base_url="http://testserver") as client:
        response = await client.post('/register',params=registration_data)

        assert response.status_code == 409

@pytest.mark.asyncio
async def test_successful_registration_flow(mocker):
    mocker.patch('login_app.api.auth_services.read_query',mocker.AsyncMock(return_value=None))
    mocker.patch('login_app.api.auth_services.bcrypt.hashpw')
    mocker.patch('login_app.api.auth_services.update_query')


    async with AsyncClient(app=app,base_url="http://testserver") as client:
        response = await client.post('/register',params=registration_data)

        assert response.status_code == 200

@pytest.mark.asyncio
async def test_unsuccessful_access_token_refresh():
    async with AsyncClient(app=app,base_url="http://testserver") as client:
        response = await client.post('/refresh_access_token',headers={'Authorization': f'Bearer {mock_token}'})

        assert response.status_code == 405


@pytest.mark.asyncio
async def test_successful_access_token_refresh(mocker):
    mocker.patch('login_app.api.auth_services.verify_refresh_token_service',mocker.AsyncMock(return_value=mock_payload))
    mocker.patch('login_app.api.auth_services.create_access_token',mocker.AsyncMock(return_value=mock_payload))

    async with AsyncClient(app=app,base_url="http://testserver") as client:
        response = await client.get('/refresh_access_token',headers={'Authorization': f'Bearer {mock_token}'})

        assert response.status_code == 200

@pytest.mark.asyncio
async def test_invalid_access_token_validation():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get('/verify_access_token', headers={'Authorization': f'Bearer {mock_token}'})

        assert response.status_code == 401

@pytest.mark.asyncio
async def test_valid_access_token_validation(mocker):
    mocker.patch('login_app.api.auth_services.jwt.decode',mocker.MagicMock(return_value=mock_payload))
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get('/verify_access_token', headers={'Authorization': f'Bearer {mock_token}'})

        assert response.status_code == 200


@pytest.mark.asyncio
async def test_expiring_refresh_token_validation(mocker):
    mocker.patch('login_app.api.auth_services.jwt.decode', mocker.MagicMock(return_value=expiring_refresh_token_payload))

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get('/verify_refresh_token', headers={'Authorization': f'Bearer {mock_token}'})

        assert response.status_code == 200

