import os

from minio import Minio
from django.conf import settings

# Initialize Minio client
minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_USE_SSL,
)


def upload_to_minio(file_path, object_name):
    """Upload file to MinIO bucket."""
    bucket_name = settings.MINIO_BUCKET_NAME

    # Create bucket if it doesn't exist
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)

    # Upload file to the bucket
    with open(file_path, 'rb') as file_data:
        file_stat = os.stat(file_path)
        minio_client.put_object(
            bucket_name, object_name, file_data, file_stat.st_size
        )

    return f"{settings.MINIO_ENDPOINT}/{bucket_name}/{object_name}"
