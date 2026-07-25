from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_session
from app.core.config import settings
from app.core.rate_limiter import limiter
from app.domain.entities.user import User
from app.domain.value_objects import Email
from app.infrastructure.auth.jwt_provider import JWTProvider
from app.infrastructure.auth.password_hasher import PasswordHasherService
from app.infrastructure.persistence.models.user_model import UserModel
from app.infrastructure.persistence.repositories.user_repository import UserRepository

router = APIRouter(prefix="/auth", tags=["auth"])

hasher = PasswordHasherService()
jwt_provider = JWTProvider()


class RegisterRequest(BaseModel):
    nombre: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str = Field(alias="accessToken")
    refresh_token: str = Field(alias="refreshToken")


class RecoverPasswordRequest(BaseModel):
    email: EmailStr


@router.post("/register", status_code=201)
@limiter.limit("20/minute")
async def register(
    request: Request, body: RegisterRequest, db: AsyncSession = Depends(get_session)
):
    repo = UserRepository(db)
    existing = await repo.get_by_email(body.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    domain_user = User.register(
        body.nombre, Email(body.email), hasher.hash(body.password)
    )
    model = UserModel(
        id=str(domain_user.id),
        nombre=domain_user.nombre,
        email=str(domain_user.email),
        password_hash=str(domain_user.password_hash),
        rol=domain_user.rol,
        fecha_registro=domain_user.fecha_registro,
    )
    db.add(model)
    await db.commit()

    return {
        "id": str(domain_user.id), "nombre": domain_user.nombre,
        "email": str(domain_user.email),
    }


@router.post("/login")
@limiter.limit("20/minute")
async def login(
    request: Request, body: LoginRequest, response: Response,
    db: AsyncSession = Depends(get_session)
):
    repo = UserRepository(db)
    user = await repo.get_by_email(body.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not hasher.verify(user.password_hash, body.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = jwt_provider.create_access_token(str(user.id), user.rol.value)
    refresh_token = jwt_provider.create_refresh_token(str(user.id))

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.environment != "development",
        samesite="lax",
        max_age=60 * 60 * 24 * settings.refresh_token_expire_days,
    )

    return TokenResponse(accessToken=access_token, refreshToken=refresh_token)


@router.post("/refresh")
@limiter.limit("20/minute")
async def refresh(
    request: Request, db: AsyncSession = Depends(get_session)
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")

    if not jwt_provider.is_refresh_token(refresh_token):
        raise HTTPException(status_code=401, detail="Invalid token type")

    user_id = jwt_provider.get_user_id_from_token(refresh_token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    repo = UserRepository(db)
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    access_token = jwt_provider.create_access_token(str(user.id), user.rol.value)
    return {"accessToken": access_token}


@router.post("/logout")
@limiter.limit("20/minute")
async def logout(request: Request, response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}


@router.get("/me")
async def get_me(current_user=Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "nombre": current_user.nombre,
        "email": str(current_user.email),
        "rol": current_user.rol.value,
        "fechaRegistro": current_user.fecha_registro.isoformat(),
    }


@router.post("/recover-password")
@limiter.limit("5/minute")
async def recover_password(
    request: Request, body: RecoverPasswordRequest,
    db: AsyncSession = Depends(get_session)
):
    repo = UserRepository(db)
    user = await repo.get_by_email(body.email)
    if not user:
        return {"message": "If the email exists, a recovery link has been sent"}
    return {"message": "If the email exists, a recovery link has been sent"}
