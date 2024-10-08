import pdb

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from login_app.api.routers.auth_router import auth_router
from tests.mocked_data import *

app = FastAPI()
app.include_router(auth_router)


@pytest.mark.asyncio
async def test_unsuccessful_registration_flow(mocker):
    mocker.patch('login_app.database.models.user.User.get_user', mocker.AsyncMock(return_value=True))

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post('/register', params=mock_registration)

        assert response.status_code == 409


@pytest.mark.asyncio
async def test_successful_registration_flow(mocker):
    mocker.patch('login_app.database.models.user.User.get_user', mocker.AsyncMock(return_value=None))

    mocker.patch('login_app.database.models.user.User.register',
                 mocker.AsyncMock(return_value={"message": "User registered successfully!"}))

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post('/register', params=mock_registration)

        assert response.status_code == 200


@pytest.mark.asyncio
async def test_unsuccessful_login_flow(mocker):
    mocker.patch('login_app.database.models.user.User.get_user', mocker.AsyncMock(return_value=None))

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post('/login', data=mock_login)

        assert response.status_code == 404


@pytest.mark.asyncio
async def test_successful_login_flow(mocker):
    user = MockUserFromDBData()
    mocker.patch(f'login_app.api.services.auth_service.AuthService.authenticate',
                 mocker.AsyncMock(return_value=user))

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.post('/login', data=mock_login)
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_unsuccessful_access_token_refresh_flow():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get('/refresh_access_token', headers={'Authorization': f'Bearer {invalid_token}'})

        assert response.status_code == 401


@pytest.mark.asyncio
async def test_successful_access_token_refresh_flow(mocker):
    user = MockUserFromDBData()
    mocker.patch('login_app.database.models.user.User.get_user',
                 mocker.AsyncMock(return_value=user))

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get('/refresh_access_token',
                                    headers={'Authorization': f'Bearer {valid_mock_refresh_token}'})

        assert response.status_code == 200


@pytest.mark.asyncio
async def test_unsuccessful_refresh_token_refreshment_flow():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get('refresh_refresh_token', headers={'Authorization': f'Bearer {invalid_token}'})

        assert response.status_code == 401


@pytest.mark.asyncio
async def test_successful_refresh_token_refreshment_flow(mocker):
    user = MockUserFromDBData()
    mocker.patch('login_app.database.models.user.User.get_user',
                 mocker.AsyncMock(return_value=user))
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get('refresh_refresh_token',
                                    headers={'Authorization': f'Bearer {valid_mock_refresh_token}'})

        assert response.status_code == 200


@pytest.mark.asyncio
async def test_verify_access_token_when_invalid_flow():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get('/verify_access_token', headers={'Authorization': f'Bearer {invalid_token}'})

        assert response.status_code == 401


@pytest.mark.asyncio
async def test_verify_access_token_when_valid_flow():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get('/verify_access_token',
                                    headers={'Authorization': f'Bearer {valid_mock_access_token}'})

        assert response.status_code == 200


@pytest.mark.asyncio
async def test_verify_refresh_token_when_invalid_flow():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get('/verify_refresh_token', headers={'Authorization': f'Bearer {invalid_token}'})

        assert response.status_code == 401


@pytest.mark.asyncio
async def test_verify_refresh_token_when_valid_flow():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get('/verify_refresh_token',
                                    headers={'Authorization': f'Bearer {valid_mock_refresh_token}'})

        assert response.status_code == 200
