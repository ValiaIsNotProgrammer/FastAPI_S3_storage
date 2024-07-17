from fastapi import HTTPException
from sqlalchemy import exc
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import EmailStr
from starlette import status

from core.security import verify_password, get_password_hash
from database.models.user import UserModel
from database.repo.abstract import Repository
from schemas.user import UserCreate


class UsersRepo(Repository[UserModel]):

    async def create(self, obj_in: UserCreate, session: AsyncSession) -> UserModel | None:
        hashed_password = get_password_hash(password=obj_in.password)
        db_session: AsyncSession = session or self.db.session
        user = UserModel(email=obj_in.email, hashed_password=hashed_password)
        obj: UserModel = self.model.model_validate(user)  # type: ignore
        try:
            db_session.add(obj)
            await db_session.commit()
        except exc.IntegrityError:
            await db_session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Resource already exists",
            )
        await db_session.refresh(obj)
        return obj

    async def get_by_email(self, email: EmailStr, session: AsyncSession | None = None) -> UserModel:
        db_session = session or self.db.session
        query = select(self.model).where(self.model.email == email)
        response = await db_session.execute(query)
        result = response.scalar_one_or_none()
        return result

    async def authenticate(self, email: EmailStr, password: str, session: AsyncSession) -> UserModel | None:
        db_session = session or self.db.session
        user = await self.get_by_email(email, db_session)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


repo = UsersRepo(UserModel)