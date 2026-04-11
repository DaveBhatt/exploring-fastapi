from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, UTC
from . import schemas, database, models
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login') # This creates an instance of the OAuth2PasswordBearer class, which is a FastAPI security utility that provides a way to handle OAuth2 authentication using password flow. The tokenUrl parameter specifies the URL where clients can obtain an access token by providing their credentials (in this case, the /login endpoint).

# SECRET_KEY should be a long, random string in production
# Algorithm should be a secure hashing algorithm like HS256 or RS256
# EXPIRES_IN should be a reasonable time frame for token expiration, such as 15 minutes or 1 hour

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    # Here we can add an expiration time to the token if desired, using the datetime library to calculate the expiration time and adding it to the data dictionary before encoding it.
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # This encodes the data dictionary into a JWT token using the specified secret key and algorithm. The resulting token is a string that can be sent to clients and used for authentication in subsequent requests.

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # This decodes the JWT token using the same secret key and algorithm that were used to create it. If the token is valid and has not expired, this will return the original data dictionary that was encoded in the token. If the token is invalid or has expired, it will raise an InvalidTokenError.
        id: str = payload.get("user_id") # This retrieves the user_id from the token's payload, which we included when we created the token. We can then use this user_id to identify the user making the request and perform any necessary authorization checks.

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id) # This creates a TokenData object using the user_id extracted from the token's payload. The TokenData schema is defined in schemas.py and can be used to validate the structure of the token data and ensure that it contains the expected fields.

    except InvalidTokenError:
        raise credentials_exception
    
    return token_data
    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    
    user = db.query(models.User).filter(models.User.id == token.id).first() # This queries the database for a user with the ID extracted from the token. If a user with that ID exists, it returns the user object; otherwise, it returns None. This allows us to identify the currently authenticated user based on the information contained in the JWT token.

    return user



