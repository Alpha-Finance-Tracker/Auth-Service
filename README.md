![Build Status](https://img.shields.io/github/actions/workflow/status/Alpha-Finance-Tracker/Auth-Service/main.yml)
![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
![Platform](https://img.shields.io/badge/platform-windows-blue)
[![Coverage Status](https://coveralls.io/repos/github/Alpha-Finance-Tracker/Auth-Service/badge.svg?branch=main)](https://coveralls.io/github/Alpha-Finance-Tracker/Auth-Service?branch=main)





# FastAPI Authentication Service

This FastAPI service is a part of a microservices based project. It provides endpoints for  login, registration, token management, and verification.

## Features

- **Login:** Authenticate users and return access tokens.
- **Register:** Create a new user account.
- **Refresh Tokens:** Obtain new access or refresh tokens using existing tokens.
- **Verify Tokens:** Validate access and refresh tokens.

## Installation

To set up this FastAPI service, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Alpha-Finance-Tracker/Auth-Service.git

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt

3. **Run the application:**
    ```bash
    uvicorn main:app --reload

Build with docker:
  ```bash
  docker build -t auth_app .
  
