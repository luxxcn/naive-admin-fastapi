"""登录验证"""

import jwt
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from fastapi import Body, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

from config.secure import SECRET_KEY, ALGORITHM, TOKEN_EXPIRE_MINUTES
from libs.error_code import AuthFailed, Forbidden, NotFound
from libs.scope import is_in_scope
from models import DatabaseDep
from models.user.user import User

token_url = "/api/auth"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_url)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginForm(BaseModel):
    """登录json"""

    username: str | None = "admin"
    secret: str = "123456"
    captcha: str = "12gl"


class Token(BaseModel):
    """返回给客户端的token"""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """token中包含的信息"""

    uid: int | None = None
    scope: str = "UserScope"
    role_code: str = "USER"


def create_access_token(user: User, role_code=None):
    """生成token"""
    if role_code:
        user.switch_role(role_code)
    token_data = TokenData(uid=user.id, role_code=user.currentRole.code)
    if user.currentRole.code == "SUPER_ADMIN":
        token_data.scope = "AdminScope"

    to_encode = token_data.model_dump()
    expire = datetime.now(
        timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return Token(access_token=encode_jwt)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, secret: str, db: DatabaseDep):
    user = User.get_user(username, db)
    if not user:
        raise AuthFailed("用户名或密码错误")
    if not verify_password(secret, user.hashed_password):
        raise AuthFailed("用户名或密码错误")
    return user


def generate_token(form: Annotated[OAuth2PasswordRequestForm,
                                   Depends()], db: DatabaseDep):
    user = authenticate_user(form.username, form.password, db)
    return create_access_token(user)


def generate_token_json(form: Annotated[LoginForm, Body()], db: DatabaseDep):
    user = authenticate_user(form.username, form.secret, db)
    return create_access_token(user)


def auth_token(token: Annotated[str, Depends(oauth2_scheme)],
               request: Request):
    """校验token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenData(**payload)
    except InvalidTokenError:
        raise AuthFailed("token无效")

    # scope校验
    if not is_in_scope(token_data.scope, request):
        raise Forbidden()

    return token_data


TokenDep = Annotated[TokenData, Depends(auth_token)]
login_required = TokenDep


async def get_current_user(token: TokenDep, db: DatabaseDep):
    user = db.get(User, token.uid)
    if user is None:
        raise AuthFailed("token无效")
    return user


async def get_current_active_user(user: Annotated[User,
                                                  Depends(get_current_user)]):
    if not user.enable:
        raise NotFound("用户不存在")
    return user


GetCurrentUserDep = Annotated[User, Depends(get_current_active_user)]
