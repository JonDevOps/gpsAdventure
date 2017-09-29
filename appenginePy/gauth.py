from oauth2client import client, crypt

WEB_CLIENT_ID = "474832205158-5q0sqta9e932cmftub9aaihgeb2c6hko.apps.googleusercontent.com"


# (Receive token by HTTPS POST)

try:
    idinfo = client.verify_id_token(token, CLIENT_ID)
    
    # If multiple clients access the backend server:
    if idinfo['aud'] != WEB_CLIENT_ID:
        raise crypt.AppIdentityError("Unrecognized client.")
    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        raise crypt.AppIdentityError("Wrong issuer.")
    if idinfo['hd'] != APPS_DOMAIN_NAME:
        raise crypt.AppIdentityError("Wrong hosted domain.")
except crypt.AppIdentityError:
    # Invalid token
userid = idinfo['sub']
