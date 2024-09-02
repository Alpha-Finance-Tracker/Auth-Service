from datetime import datetime, timedelta

mock_user_db_information = [(1, 'test@example.com', 'hashed_password','user')]
auth_data = {'username':'Test@example.com','password':'0000'}
registration_data = {'email':'Test@example.com', 'password':'0000'}
mock_payload = {'user_id': 1, 'email': 'test@example.com', 'role': 'user','exp': (datetime.now() + timedelta(days=1)).timestamp(),'Validity':'Valid'}
expiring_refresh_token_payload = {'user_id': 1, 'email': 'test@example.com', 'role': 'user','exp': (datetime.now().timestamp()),'Validity':'Valid'}
mock_token  = 'Fake token'