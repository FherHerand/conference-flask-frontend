# -*- coding: utf-8 -*-
import boto3
import botocore
from botocore.exceptions import ClientError

import base64
import tempfile
import uuid

from server import credentials as creds
from server.utils import bad_request, logging, get_only_base64

def get_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=creds.s3['access_key_id'],
        aws_secret_access_key=creds.s3['secret_access_key'],
    )

def upload_image(bucketname, foldername, name, data_uri, ext='jpg'):
    image_64_encode_str = get_only_base64(data_uri)

    client = get_s3_client()

    file_name = '%s-%s.%s' % (name, uuid.uuid4(), ext)
    file_path = '%s/%s' % (foldername, file_name)
    image_64_encode = base64.b64decode((image_64_encode_str))
    f = tempfile.TemporaryFile()
    f.write(image_64_encode)
    f.seek(0)

    try:
        response = client.put_object(Body=f, Bucket=bucketname, Key=file_path, ACL='public-read')
        #logging.info(response)
        full_path = '%s/%s' % (creds.S3_BASE_DOMAIN, file_path)
        return response, {'full_path': full_path, 'key': file_path}
    except ClientError as e:
        logging.error(e)
        return bad_request('La imagen no pudo ser guardada'), False

