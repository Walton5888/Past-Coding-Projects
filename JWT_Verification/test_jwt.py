import pytest
import jwt_verify
from jwt_verify import is_weekday, check_admin, main
import jwt
import os
import datetime
from unittest.mock import patch

'''Confirms error is thrown for non-admin token if inputted.'''
def test_main_not_admin(capsys):
        user_input=['-t', 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE2OTc1OTI2NDcsImV4cCI6MTcwMDI3MTA0NywiYXVkIjoiemIuY29tIiwic3ViIjoiemJAemIuY29tIiwiR2l2ZW5OYW1lIjoiWkIiLCJTdXJuYW1lIjoiWkIiLCJFbWFpbCI6IlpCQFpCLmNvbSIsIlJvbGUiOlsiQWRtaW4iLCJQcm9qZWN0IEFkbWluaXN0cmF0b3IiXX0.NSvLW-hMfDZSJs2WVAvzGWSqjgZdmxVKMoa9oUI75k5', '-s', 'qwertyuiopasdfghjklzxcvbnm123456', "-a", "zb.com"]
        #Non-admin token is inserted.
        with patch('sys.argv', user_input):
         with pytest.raises(Exception):
          out, _ = capsys.readouterr() #Searches for key words in the output.
          assert "Error: token lacks admin privileges." in out #Confirms that error exists in output when an invalid key is inputted.

'''Denies access if it is the weekend.'''
def test_main_admin_on_weekend(capsys):
    user_input = ["-t", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE2OTc1OTI2NDcsImV4cCI6MTcwMDI3MTA0NywiYXVkIjoiemIuY29tIiwic3ViIjoiemJAemIuY29tIiwiR2l2ZW5OYW1lIjoiWkIiLCJTdXJuYW1lIjoiWkIiLCJFbWFpbCI6IlpCQFpCLmNvbSIsIlJvbGUiOlsiQWRtaW4iLCJQcm9qZWN0IEFkbWluaXN0cmF0b3IiXX0.NSvLW-hMfDZSJs2WVAvzGWSqjgZdmxVKMoa9oUI75k4", "-s", "qwertyuiopasdfghjklzxcvbnm123456", "-a", "zb.com"]
    picked_date = datetime.date(2022, 10, 23) # A Sunday is selected.
    with patch('sys.argv', user_input, picked_date):
            with pytest.raises(Exception):
             out, _ = capsys.readouterr() #Scans what is outputted to user. 
             assert 'Error: this is the weekend.' in out #Confirms an error message is receieved. 

'''Verifies the success of decoding an admin token.'''
def test_main_admin(capsys):
    user_input = ["-t", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE2OTc1OTI2NDcsImV4cCI6MTcwMDI3MTA0NywiYXVkIjoiemIuY29tIiwic3ViIjoiemJAemIuY29tIiwiR2l2ZW5OYW1lIjoiWkIiLCJTdXJuYW1lIjoiWkIiLCJFbWFpbCI6IlpCQFpCLmNvbSIsIlJvbGUiOlsiQWRtaW4iLCJQcm9qZWN0IEFkbWluaXN0cmF0b3IiXX0.NSvLW-hMfDZSJs2WVAvzGWSqjgZdmxVKMoa9oUI75k4", "-s", "qwertyuiopasdfghjklzxcvbnm123456", "-a", "zb.com"]
    #Valid key is inserted. 
    with patch ('sys.argv', user_input):
        with pytest.raises(Exception):
            out, _ = capsys.readoutter()
            assert 'Decoding of JWT containing admin was successful.' in out #Verifies that admin token was granted access without an exception.


'''Checks if admin privileges are present in the token on a weekday.'''
def test_main_valid_admin_weekday(capsys):
    user_input = ["-t", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE2OTc1OTI2NDcsImV4cCI6MTcwMDI3MTA0NywiYXVkIjoiemIuY29tIiwic3ViIjoiemJAemIuY29tIiwiR2l2ZW5OYW1lIjoiWkIiLCJTdXJuYW1lIjoiWkIiLCJFbWFpbCI6IlpCQFpCLmNvbSIsIlJvbGUiOlsiQWRtaW4iLCJQcm9qZWN0IEFkbWluaXN0cmF0b3IiXX0.NSvLW-hMfDZSJs2WVAvzGWSqjgZdmxVKMoa9oUI75k4", "-s", "qwertyuiopasdfghjklzxcvbnm123456", "-a", "zb.com"]
    picked_date = datetime.date(2022, 10, 25) #A Tuesday is selected.
    with patch('sys.argv', user_input, picked_date):
        with pytest.raises(Exception):
            out, _ = capsys.readoutter() #Scans output to user.
            assert 'User is admin. It is a weekday.' in out #See if the output recognizes if it's a weekday.

'''See if the secret key is decoded correctly by the decoder.'''
def test_decode_JWT_key():
    key = 'qwertyuiopasdfghjklzxcvbnm123456'
    algorithm = 'HS256'
    with pytest.raises(Exception):
        jwt_verify.decode_JWT(key, algorithm)#Request for key to be decoded. 
        assert jwt_verify.decode_JWT(key, algorithm)=='qwertyuiopasdfghjklzxcvbnm123456'#See if the correct key value is outputted. 


'''See if the decoder properly decodes a token.'''
def test_decode_JWT_token():
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE2OTc1OTI2NDcsImV4cCI6MTcwMDI3MTA0NywiYXVkIjoiemIuY29tIiwic3ViIjoiemJAemIuY29tIiwiR2l2ZW5OYW1lIjoiWkIiLCJTdXJuYW1lIjoiWkIiLCJFbWFpbCI6IlpCQFpCLmNvbSIsIlJvbGUiOlsiQWRtaW4iLCJQcm9qZWN0IEFkbWluaXN0cmF0b3IiXX0.NSvLW-hMfDZSJs2WVAvzGWSqjgZdmxVKMoa9oUI75k4'
    algorithm = 'HS256'
    with pytest.raises(Exception):
        jwt_verify.decode_JWT(token, algorithm) #Request for the token to be decoded.
        assert jwt_verify.decode_JWT(token, algorithm) == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE2OTc1OTI2NDcsImV4cCI6MTcwMDI3MTA0NywiYXVkIjoiemIuY29tIiwic3ViIjoiemJAemIuY29tIiwiR2l2ZW5OYW1lIjoiWkIiLCJTdXJuYW1lIjoiWkIiLCJFbWFpbCI6IlpCQFpCLmNvbSIsIlJvbGUiOlsiQWRtaW4iLCJQcm9qZWN0IEFkbWluaXN0cmF0b3IiXX0.NSvLW-hMfDZSJs2WVAvzGWSqjgZdmxVKMoa9oUI75k4"
        #Checks to see if the decoder outputs the correct token value.

'''Tests if surname from the payload is decoded properly using decode_JWT.'''
def test_surname_case():
        key = "qwertyuiopasdfghjklzxcvbnm123456"
        payload = {"iss": "Online JWT Builder",
        "iat": 1697592647,
        "exp": 1700271047,
        "aud": "zb.com",
        "sub": "zb@zb.com",
        "GivenName": "ZB",
        "Surname": "ZB",
        "Email": "ZB@ZB.com",
        "Role": [
        "Admin",
        "Project Administrator"
    ]
} #Token information
        web_token = jwt.encode(payload, key, algorithm='HS256')
        decoded_web_token = jwt_verify.decode_JWT(web_token, key, audience = "zb.com")
        assert decoded_web_token['Surname']=='ZB' #See if surname is decoded properly. 

'''Tests to see if token expires when it should.'''
def test_expiration_case():
        key = "qwertyuiopasdfghjklzxcvbnm123456"
        payload = {"iss": "Online JWT Builder",
        "iat": 1697592647,
        "exp": 1700271047,
        "aud": "zb.com",
        "sub": "zb@zb.com",
        "GivenName": "ZB",
        "Surname": "ZB",
        "Email": "ZB@ZB.com",
        "Role": [
        "Admin",
        "Project Administrator"
    ]
} #Token information
        web_token = jwt.encode(payload, key, algorithm='HS256')
        decoded_web_token = jwt_verify.decode_JWT(web_token, key, audience = "zb.com")
        assert decoded_web_token['exp']==1700271047
 
'''Checks to see if the day is a weekday.'''
def test_is_weekday():
    picked_date = datetime.date(2022, 10, 25)  #A Tuesday is picked as the selected date. 
    with patch('datetime.date') as dummy_date:
        dummy_date.today.return_value = picked_date
        assert is_weekday() == True

'''Verify the day isn't during the week.'''
def test_is_weekday_weekend():
    """Verify if the selected date is not during the week by picking a day on the weekend."""
    picked_date = datetime.date(2022, 10, 23)  # A Sunday is picked as the selected date.
    with patch('datetime.date') as dummy_date:
        dummy_date.today.return_value = picked_date
        assert is_weekday() == False

'''See if the admin role is properly recognized by the check_admin function.'''
def test_check_admin():
      decrypted_token = {"Role": "Admin"} #Admin role is inserted into token's payload.
      assert check_admin(decrypted_token) == True

'''See if a non-admin role is properly idnetified by the check_admin function.'''
def test_check_admin_non_admin():
    decrypted_token = {'Role': 'User'} #Role other than user is inserted. 
    assert check_admin(decrypted_token) == False
       

if __name__ == '__main__':
    pytest.main()