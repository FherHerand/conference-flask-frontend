# -*- coding: utf-8 -*-
import hashlib
import logging
import hmac
import base64
logging.basicConfig(level=logging.INFO)

def bad_request(message):
    response = {
        'status_code': 400,
        'message': message
    }
    return response, 400, {'content-type': 'application/json'}

def get_encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

def get_secret_hash(username, client_id, client_secret_id):
  msg = username + client_id
  dig = hmac.new(str(client_secret_id).encode('utf-8'), msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
  d2 = base64.b64encode(dig).decode()
  return d2

def get_only_base64(data_uri):
    b64_parts = data_uri.split(',')
    image_64_encode_str = len(b64_parts) == 2 and b64_parts[1] or b64_parts[0]
    return image_64_encode_str

def get_bytes_from_data_uri_str(data_uri):
    base64str = get_only_base64(data_uri)
    data_bytes = base64.b64decode(base64str)
    return data_bytes