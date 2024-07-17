from uuid import UUID

from sqlalchemy import and_

from sqlmodel.ext.asyncio.session import AsyncSession

from database.models.photo import PhotoModel
from database.models.user import UserModel
from database.repo.abstract import Repository


class PhotosRepo(Repository[PhotoModel]):

    async def get_photo_by_user(self, *, photo_id: UUID, user: UserModel, session: AsyncSession | None = None):
        whereclause = and_(self.model.id == photo_id, self.model.user_id == user.id)
        return await self.get_by_id(id=photo_id, session=session, whereclause=whereclause)

    async def get_multi_paginated_by_user(self, user: UserModel, *, session: AsyncSession | None = None, offset: int = 0, limit: int = 0):
        whereclause = (user.id == self.model.user_id)
        return await self.get_multi_paginated(session=session, offset=offset, limit=limit, whereclause=whereclause)

    async def delete_photo_by_user(self, *, photo_id: UUID, user: UserModel, session: AsyncSession):
        whereclause = and_(self.model.id == photo_id, self.model.user_id == user.id)
        return await self.delete(id=photo_id, session=session, whereclause=whereclause)

    async def update_photo_by_user(self, *, photo: PhotoModel, user: UserModel, session: AsyncSession):
        whereclause = and_(self.model.id == photo.id, self.model.user_id == user.id)
        return await self.update(obj_in=photo, session=session, whereclause=whereclause)


repo = PhotosRepo(PhotoModel)
