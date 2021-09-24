import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import os
from dotenv import load_dotenv
from flask import session, request, abort

load_dotenv()

AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
ALGORITHMS = os.getenv('ALGORITHMS')
API_AUDIENCE = os.getenv('API_AUDIENCE')
# AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")


## Auth Header

def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    print("HEADERS", request.headers)
    if session["token"] is not None:
        token = session["token"]
        return token
    else:
        auth = request.headers.get('Authorization', None)
        if not auth:
            print("GET AUTH", auth)
            raise AuthError({
                'code': 'authorization_header_missing',
                'description': 'Authorization header is expected.'
            }, 401)

        parts = auth.split()
        if parts[0].lower() != 'bearer':
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Authorization header must start with "Bearer".'
            }, 401)

        elif len(parts) == 1:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Token not found.'
            }, 401)

        elif len(parts) > 2:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Authorization header must be bearer token.'
            }, 401)

        token = parts[1]
        return token


def check_permissions(permission, payload):
    # print("PERMISSIONs", payload["permissions"])
    if "permissions" not in payload:
        raise AuthError({
                        'code': 'invalid_claims',
                        'description': 'Permissions not included in JWT.'
                        }, 400)

    if permission not in payload["permissions"]:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 401)

    return True


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 401)


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def requires_auth(permission=""):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # token = None
            # if session["token"]:
            #     token = session["token"]
            #     print("SESSION TOKEN FROM AUTH0", token)
            # else:
            #     token = get_token_auth_header()
            #     print("TOKEN GET TOKEN", token)
            # print("SESSION TOKEN", session["token"])
            # session["token"] = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFoRHk4TDczSUFfVDZuVEw3Y08zeSJ9.eyJpc3MiOiJodHRwczovL2tvcnpoeWstYXBwLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTNhNjUxYjRmZWM2ZDAwNjgyYWM1ZTYiLCJhdWQiOlsiYXBwIiwiaHR0cHM6Ly9rb3J6aHlrLWFwcC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjMyNDA0ODgwLCJleHAiOjE2MzI1NzQ4ODAsImF6cCI6ImEwbXpMUFgwUFo2S1BXVkdvMDU4RkZDVVVOd1NocUlOIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphdXRob3IiLCJkZWxldGU6Ym9vayIsImdldDphdXRob3JzIiwiZ2V0OmJvb2tzIiwicGF0Y2g6YXV0aG9yIiwicGF0Y2g6Ym9vayIsInBvc3Q6YXV0aG9yIiwicG9zdDpib29rIl19.GN8lBOlbjBv1rnN0rMsy-niu360s964xTs3WjahYNviLRFZl55bNttMM2VYG4htlWA-zzNFcGHccA5a-jbFSU6uqGGSP-WgzsH5AhQOTi_yqqHwK7k1xdT-zPc3SqvYVj1itaXbWVKHOBQmHMGk3-G7TTl6JB2BSVMx9mGROk6Gec4MJ0NqaWludhFemXcNj3NrkXogQWvHwXWNpAMKSp8Gl9H44-jyBVobSACZtLtLpMswXOiooL_UYK43NfQBVU8ew4TLy_1x3a4tQWcrH2Xp2AcEOPGNFWIZidSaNm5bw1rfkOoF32oQQ1CTx87pOVc9Os6w641ebth7FVWwYUA"
            # print("SESSION AUTH TEST", session["token"])
            # if session["token"]:
            #     token = session["token"]
            # # elif session.headers["Authorization"] is not None:
            # #     token = session.headers["Authorization"] 
            # else:
            #     print("session headers", request.headers["Authorization"])
            #     token = get_token_auth_header()
            # # print("TOKEN", token)
            # # if session["token"]:
            # #     token = session["token"]
            # print("session headers", request.headers["Authorization"])
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
