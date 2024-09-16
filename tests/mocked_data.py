mock_login = {'username': 'Test@gmail.com', 'password': '0000'}
mock_registration = {'email': 'Test@gmail.com', 'password': '0000'}
mock_authentication_db_user_info = [(1,'Test@gmail.com','$2b$12$gK3nxM0G/FayDI8rs6Jm1Obl8UKsmaF4Wa8s5UBNp8hNq7PXJ2VLi','user')]

valid_mock_access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMSwiZW1haWwiOiJUZXN0QGdtYWlsLmNvbSIsInJvbGUiOiJ1c2VyIiwiZXhwIjo0ODgxMTI0NjY1fQ.pyN38WUX_zguzaAyeivC0YLv7Rsxz-nDaVdFCeEnG2w'
valid_mock_refresh_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMSwiZXhwIjo0ODgxMTI0NjY1fQ.EPcUZfakItrjDfHtbrnIX2d9BSLnJPSvx-Pv7U4ODkI'
invalid_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'


mock_token_user_info = [('Test@gmail.com','user')]

class MockUserFromDBData:
    user_id = 1
    email = 'Test@gmail.com'
    password = '$2b$12$gK3nxM0G/FayDI8rs6Jm1Obl8UKsmaF4Wa8s5UBNp8hNq7PXJ2VLi'
    role = 'user'
