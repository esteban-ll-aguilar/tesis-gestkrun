from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_session, require_any_role, require_role
from app.domain.entities.user import User
from app.domain.enums import Rol
from app.infrastructure.persistence.models.user_model import UserModel

router = APIRouter(prefix="/users", tags=["users"])


class UpdateRolRequest(BaseModel):
    rol: str


@router.patch("/{user_id}/rol")
async def update_user_rol(
    user_id: str,
    body: UpdateRolRequest,
    current_user: User = Depends(require_role(Rol.ADMIN)),
    db: AsyncSession = Depends(get_session),
):
    if body.rol not in [r.value for r in Rol]:
        raise HTTPException(status_code=400, detail=f"Invalid role: {body.rol}")

    result = await db.execute(
        select(UserModel).where(UserModel.id == user_id, UserModel.deleted_at.is_(None))
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.execute(
        update(UserModel).where(UserModel.id == user_id).values(rol=body.rol)
    )
    await db.commit()
    return {"message": "Role updated"}


@router.get("")
async def list_users(
    search: str | None = Query(None, description="Search by name or email"),
    current_user: User = Depends(require_any_role(Rol.ADMIN, Rol.PRODUCT_OWNER)),
    db: AsyncSession = Depends(get_session),
):
    query = select(UserModel).where(UserModel.deleted_at.is_(None))

    if search:
        query = query.where(
            (UserModel.nombre.ilike(f"%{search}%"))
            | (UserModel.email.ilike(f"%{search}%"))
        )

    result = await db.execute(query)
    users = result.scalars().all()

    return [
        {
            "id": u.id,
            "nombre": u.nombre,
            "email": u.email,
            "rol": u.rol,
            "fechaRegistro": u.fecha_registro.isoformat(),
        }
        for u in users
    ]
