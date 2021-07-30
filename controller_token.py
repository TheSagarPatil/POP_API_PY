import jwt
import datetime

key = "\xc1\xc8\xef\xb6\xd4,\xbc\x82I\x8azD\x08\xb6\xf4\xe4\n]\x0e\xb8\xd7\x8c1\xaf"

def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            #app.config.get('SECRET_KEY'),
            key,
            algorithm='HS256'
        )
    except Exception as e:
        return e