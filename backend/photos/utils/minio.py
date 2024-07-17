import io
import uuid

from fastapi import UploadFile
from minio import Minio


class MinioClient:
    def __init__(self, endpoint: str, access_key: str, secret_key: str, bucket_name: str):
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self.client = Minio(endpoint=endpoint, access_key=access_key, secret_key=secret_key, secure=False)

        self.create_if_not_exists_bucket()

    def create_if_not_exists_bucket(self) -> str:
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)
        return self.bucket_name

    def upload_image(self, file: UploadFile) -> str:
        file_s3_name = self.get_unique_file_name(file)
        file_data: bytes = file.file.read()
        return self.__put_object(file=file_data, filename=file_s3_name)

    def __put_object(self, file: bytes, filename: str) -> str:
        content_type = "image/" + filename.split(".")[-1]
        self.client.put_object(
            bucket_name=self.bucket_name,
            object_name=filename,
            data=io.BytesIO(file),
            length=len(file),
            content_type=content_type)
        return self.get_file_url(filename)

    @staticmethod
    def get_unique_file_name(file: UploadFile) -> str:
        file_extension = file.filename.split('.')[-1]
        new_file_name = f'{uuid.uuid4()}.{file_extension}'
        return new_file_name

    def get_file_url(self, file_name: str) -> str:
        file_url = f"{self.endpoint}/{self.bucket_name}/{file_name}"
        return file_url

    def update_image(self, image_url: str, file: UploadFile) -> str:
        filename = image_url.split("/")[-1]
        file_data: bytes = file.file.read()
        return self.__put_object(file=file_data, filename=filename)

    def delete_image(self, image_url: str):
        object_name = image_url.split("/")[-1]
        self.client.remove_object(
            bucket_name=self.bucket_name,
            object_name=object_name
        )


