import datetime
import os
from decouple import config

try:
    from .ignore2 import AWS_ACCESS_KEY_ID,  AWS_SECRET_ACCESS_KEY
except:
    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", "AKIAJARK375PALZJC55Q")
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", "g+CST4E55dcMZozbgVMkpNTWjhkfxKQibU0egT6k")



YOUR_S3_BUCKET = "zappa-1o7we1h38"

STATICFILES_STORAGE = "django_s3_storage.storage.StaticS3Storage"
AWS_S3_BUCKET_NAME_STATIC = YOUR_S3_BUCKET

# # These next two lines will serve the static files directly
# # from the s3 bucket
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % YOUR_S3_BUCKET
STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

# OR...if you create a fancy custom domain for your static files use:
# AWS_S3_PUBLIC_URL_STATIC = "https://static.zappaguide.com/"
