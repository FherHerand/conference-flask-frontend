# -*- coding: utf-8 -*-
import boto3
import botocore
from botocore.exceptions import ClientError, ParamValidationError

from server import credentials as creds
from server.utils import bad_request, logging, get_encrypt_string, get_secret_hash

def get_cognito_client():
    return boto3.client(
        'cognito-idp',
        aws_access_key_id=creds.cognito['access_key_id'],
        aws_secret_access_key=creds.cognito['secret_access_key'],
        region_name=creds.cognito['region'],
    )

def create_user(name, username, password, face_id, profile_image_path, relative_image_path):
    client = get_cognito_client()
    try:
        response = client.admin_create_user(
            UserPoolId=creds.COGNITO_USER_POOL_ID,
            Username=username,
            UserAttributes=[
                {
                    'Name': 'name',
                    'Value': name
                },
                {
                    'Name': 'custom:face_id',
                    'Value': face_id
                },
                {
                    'Name': 'custom:profile_image_path',
                    'Value': profile_image_path
                },
                {
                    'Name': 'custom:relative_image_path',
                    'Value': relative_image_path
                },
            ],
            TemporaryPassword=password,
        )
        #logging.info(response)
        return response, True
    except ClientError as e:
        logging.error(e)
        if e.response['Error']['Code'] == 'UsernameExistsException':
            return bad_request('El usuario ya existe'), False
        elif e.response['Error']['Code'] == 'InvalidPasswordException':
            return bad_request('El usuario ya existe'), False
        else:
            return bad_request('El usuario no pudo ser guardado'), False
        
def login_user(username, password):
    client = get_cognito_client()
    try:
        secret = get_secret_hash(username, creds.COGNITO_CLIENT_ID, creds.COGNITO_CLIENT_SECRET_ID)
        response = client.admin_initiate_auth(
            UserPoolId=creds.COGNITO_USER_POOL_ID,
            ClientId=creds.COGNITO_CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,
                'SECRET_HASH': secret,
                'PASSWORD': password,
            },
            ClientMetadata={
                'username': username,
                'password': password,
            },
        )
        logging.info(response)
        return response, True
    except ClientError as e:
        logging.error(e)
        if e.response['Error']['Code'] == 'NotAuthorizedException':
            return bad_request('El usuario o contraseña es incorrecto'), False
        elif e.response['Error']['Code'] == 'UserNotConfirmedException':
            return bad_request('El usuario no está confirmado'), False
        else:
            return bad_request('El usuario no pudo ser verificado'), False
        
def get_users():
    client = get_cognito_client()
    try:
        response = client.list_users(
            UserPoolId=creds.COGNITO_USER_POOL_ID,
        )
        #logging.info(response)
        return response, True
    except ClientError as e:
        logging.error(e)
        return bad_request('Error al obtener usuarios'), False
        