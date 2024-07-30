from storages.backends.s3boto3 import S3Boto3Storage
from config import settings


class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION
    default_acl = settings.AWS_DEFAULT_ACL


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    default_acl = settings.AWS_DEFAULT_ACL
    custom_domain = False
