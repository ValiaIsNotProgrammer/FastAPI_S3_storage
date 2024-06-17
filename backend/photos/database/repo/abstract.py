
from typing import Generic, TypeVar, Any
from uuid import UUID

from fastapi import HTTPException


from fastapi_async_sqlalchemy import db
from sqlalchemy import ScalarResult, exc
from sqlmodel import select, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from ..models.base import ModelBase

AbstractModel = TypeVar('AbstractModel', bound=SQLModel)


class Repository(Generic[AbstractModel]):

    def __init__(self, model: type[ModelBase]):
        self.model = model
        self.db = db

    def get_db(self) -> type(db):
        return self.db

    async def get_all(self, *, session: AsyncSession | None = None) -> ScalarResult[ModelBase]:
        db_session = session or self.db.session
        query = select(self.model).where(self.model.id == id)
        response = await db_session.execute(query)
        return response.scalars()

    async def get_multi_paginated(self, *, session: AsyncSession | None = None, offset: int = 0, limit: int = 0) -> ScalarResult[ModelBase]:
        db_session = session or self.db.session
        query = select(self.model).offset(offset).limit(limit)
        response = await db_session.execute(query)
        return response.scalars()

    async def get_by_id(self, id: UUID, *, session: AsyncSession | None = None) -> ModelBase | None:
        db_session = session or self.db.session
        query = select(self.model).where(self.model.id == id)
        response = await db_session.execute(query)
        result = response.scalar_one_or_none()
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found")
        return result

    async def delete(self, id: UUID, *, session: AsyncSession) -> None:
        db_session: AsyncSession = session or self.db.session
        obj = await self.get_by_id(id=id, session=session)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")
        await db_session.delete(obj)
        await db_session.commit()
        return

    async def create(self, obj_in: AbstractModel, session: AsyncSession) -> AbstractModel | None:
        db_session: AsyncSession = session or self.db.session
        obj = self.model.model_validate(obj_in)  # type: ignore
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

    async def update(self, id: UUID, obj_in: AbstractModel, session: AsyncSession) -> ModelBase | None:
        db_session: AsyncSession = session or self.db.session
        obj = self.model.model_validate(obj_in)  # type: ignore
        obj = await self.get_by_id(id, session=session)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found")

        for key, value in obj.dict(exclude_unset=True).items():
            setattr(obj, key, value)
        db_session.add(obj)
        await db_session.commit()
        await db_session.refresh(obj)
        return obj


    # async def update(self, ident: int, **values):
    #     if isinstance(obj_new, dict):
    #         update_data = obj_new
    #     else:
    #         update_data = obj_new.dict(
    #             exclude_unset=True
    #         )  # This tells Pydantic to not include the values that were not sent
    #     for field in update_data:
    #         setattr(obj_current, field, update_data[field])
    #
    #     db_session.add(obj_current)
    #     await db_session.commit()
    #     await db_session.refresh(obj_current)
    #     return obj_current

    # async def create(
    #     self,
    #     *,
    #     obj_in: BaseModel,
    #     created_by_id: UUID | str | None = None,
    #     db_session: AsyncSession | None = None,
    # ) -> BaseModel:
    #     db_session = db_session or self.db.session
    #     db_obj = self.model.model_validate(obj_in)  # type: ignore
    #
    #     if created_by_id:
    #         db_obj.created_by_id = created_by_id
    #
    #     try:
    #         db_session.add(db_obj)
    #         await db_session.commit()
    #     except exc.IntegrityError:
    #         await db_session.rollback()
    #         raise HTTPException(
    #             status_code=409,
    #             detail="Resource already exists",
    #         )
    #     await db_session.refresh(db_obj)
    #     return db_obj





















