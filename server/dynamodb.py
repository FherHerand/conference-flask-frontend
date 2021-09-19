# -*- coding: utf-8 -*-
import boto3
import botocore
from botocore.exceptions import ClientError, ParamValidationError

from datetime import datetime
import uuid

from server import credentials as creds
from server.utils import bad_request, logging

def get_dynamodb_client():
    return boto3.client(
        'dynamodb',
        aws_access_key_id=creds.dynamodb['access_key_id'],
        aws_secret_access_key=creds.dynamodb['secret_access_key'],
        region_name=creds.dynamodb['region'],
    )
    
def get_dynamodb_resource():
    return boto3.resource(
        'dynamodb',
        aws_access_key_id=creds.dynamodb['access_key_id'],
        aws_secret_access_key=creds.dynamodb['secret_access_key'],
        region_name=creds.dynamodb['region'],
    )

def add_student(code, name, full_image_path, relative_image_path):
    client = get_dynamodb_client()
    try:
        response = client.put_item(
            TableName='student',
            Item={
                'code': {'S': code},
                'name': {'S': name},
                'full_image_path': {'S': full_image_path},
                'relative_image_path': {'S': relative_image_path},
            },
        )
        logging.info(response)
        return response, True
    except ClientError as e:
        logging.error(e)
        return bad_request('No se pudo registrar el estudiante'), False

def get_students():
    client = get_dynamodb_resource()
    try:
        table = client.Table('student')
        response = table.scan()
        #logging.info(response)
        return response, True
    except ClientError as e:
        logging.error(e)
        return bad_request('No se pudo obtener estudiantes'), False
    
def add_attendance(name, full_image_path, relative_image_path, similarity):
    client = get_dynamodb_client()
    try:
        id = str(uuid.uuid4())
        timestamp = str(datetime.now().timestamp())
        response = client.put_item(
            TableName='attendance',
            Item={
                'id': {'S': id},
                'timestamp': {'N': timestamp},
                'name': {'S': name},
                'full_image_path': {'S': full_image_path},
                'relative_image_path': {'S': relative_image_path},
                'similarity': {'N': str(similarity)},
                'students': {'L': []},
                'user': {'S': ''}
            },
        )
        #logging.info(response)
        return response, id, timestamp, True
    except ClientError as e:
        logging.error(e)
        return bad_request('No se pudo registrar la asistencia'), None, None, False

def add_student_to_attendance(attendance_id, timestamp, student):
    client = get_dynamodb_client()
    try:
        response = client.update_item(
            TableName='attendance',
            Key={'id': {'S': attendance_id}, 'timestamp': {'N': timestamp}},
            UpdateExpression='SET #students = list_append(#students, :new_student)',
            ExpressionAttributeNames={
                '#students': 'students',
            },
            ExpressionAttributeValues={
                ':new_student': {
                    'L': [
                        {
                            'M': {
                                'code': {'S': student['code']},
                                'name': {'S': student['name']},
                                'full_image_path': {'S': student['full_image_path']},
                                'assist': {'BOOL': student['assist']}
                            }
                        }
                    ]
                }
            },
            ReturnValues='UPDATED_NEW',
        )
        #logging.info(response)
        return response, True
    except ClientError as e:
        logging.error(e)
        return bad_request('No se pudo registrar la asistencia de los estudiantes'), False
    
def get_attendances():
    client = get_dynamodb_resource()
    try:
        table = client.Table('attendance')
        response = table.scan()
        #logging.info(response)
        return response, True
    except ClientError as e:
        logging.error(e)
        return bad_request('No se pudo obtener asistencias'), False
