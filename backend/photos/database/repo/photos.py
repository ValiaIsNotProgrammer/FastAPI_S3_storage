from database.models.photo import PhotoModel
from database.repo.abstract import Repository


class PhotosRepo(Repository[PhotoModel]):
    ...


repo = PhotosRepo(PhotoModel)