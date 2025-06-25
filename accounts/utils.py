from google.oauth2 import id_token
from google.auth.transport import requests as googleAuthRequests
import requests
from django.conf import settings
from jose import jwt
from jose.exceptions import JWTError


def verify_google_token(token):
    try:
        idinfo = id_token.verify_oauth2_token(
            token, googleAuthRequests.Request(), settings.GOOGLE_CLIENT_ID)
        return idinfo  # contains user info like email, sub, name
    except ValueError:
        return None


APPLE_KEYS_URL = "https://appleid.apple.com/auth/keys"


def get_apple_public_keys():
    response = requests.get(APPLE_KEYS_URL)
    response.raise_for_status()
    return response.json()['keys']


def verify_apple_identity_token(identity_token, audience):
    """
    Verify Apple identity token JWT.
    :param identity_token: JWT string from Apple
    :param audience: Your app's Bundle ID (Apple App ID)
    :return: decoded payload dict if valid, else None
    """
    keys = get_apple_public_keys()

    for key in keys:
        try:
            payload = jwt.decode(
                identity_token,
                key,
                algorithms=['RS256'],
                audience=audience,
                issuer='https://appleid.apple.com'
            )
            return payload  # Valid token payload
        except JWTError:
            continue
    return None
