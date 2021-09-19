# -*- coding: utf-8 -*-
import boto3
import botocore
from botocore.exceptions import ClientError

from flask import Blueprint, request, abort, jsonify
from flask_cors import CORS, cross_origin

import base64
import json

from server import credentials as creds, cognito, s3, rekognition, dynamodb
from server.utils import bad_request, logging, get_bytes_from_data_uri_str

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/login', methods = ['POST'])
@cross_origin()
def login():
    if request.method == 'POST':
        content = request.get_json()
        type = content['type']
        
        if type == 'camera':
            data_uri = content['data_uri']
            data_uri_bytes = get_bytes_from_data_uri_str(data_uri)
            cognito_response, success = cognito.get_users()
            if success:
                for user in cognito_response['Users']:
                    attrs = {}
                    attrs['username'] = user['Username']
                    for attr in user['Attributes']:
                        attrs[attr['Name']] = attr['Value']
                    rek_response, success = rekognition.compare_faces_image_bytes_path(creds.BUCKET_NAME, data_uri_bytes, attrs['custom:relative_image_path'])
                    if success:
                        if len(rek_response['FaceMatches']) > 0:
                            data = {
                                'name': attrs['name'],
                                'username': attrs['username'],
                                'profile_image_path': attrs['custom:profile_image_path'],
                            }
                            return data, 200, {'content-type': 'application/json'}
                return bad_request('No hay coincidencia de rostro, intente nuevamente')
            else:
                return cognito_response
        elif type == 'credentials':
            username = content['username']
            password = content['password']
            cognito_response, success = cognito.login_user(username, password)
            
            if success:
                attrs = cognito_response['ChallengeParameters']['userAttributes']
                attrs = json.loads(attrs)
                data = {
                    'name': attrs['name'],
                    'username': username,
                    'profile_image_path': attrs['custom:profile_image_path'],
                }
                return data, 200, {'content-type': 'application/json'}
            else:
                return cognito_response

@bp.route('/register', methods = ['POST'])
@cross_origin()
def register():
    if request.method == 'POST':
        content = request.get_json()
        name = content['name']
        username = content['username']
        password = content['password']
        data_uri = content['data_uri']
        profile_image_path = ''
        relative_image_path = ''
        face_id = ''
        
        if data_uri:
            bucketname = creds.BUCKET_NAME
            s3_response, metadata = s3.upload_image(bucketname, creds.BUCKET_FOLDER_USERS, username, data_uri)
            if metadata:
                profile_image_path = metadata['full_path']
                relative_image_path = metadata['key']
                rek_response, success = rekognition.get_face_id(bucketname, relative_image_path)
                if success:
                    if rek_response['FaceDetails'] and len(rek_response['FaceDetails']) == 1:
                        index_response, success = rekognition.index_face_id(creds.REKOGNITION_COLLECTION_ID, bucketname, relative_image_path)
                        if success:
                            face_id = index_response['FaceRecords'][0]['Face']['FaceId']
                        else:
                            return index_response
                    else:
                        return bad_request('La imagen no pudo ser procesada, intente de nuevo')
                else:
                    return rek_response
            else:
                return s3_response
            
        cognito_response, success = cognito.create_user(name, username, password, face_id, profile_image_path, relative_image_path)
        if success:
            data = {
                'name': name,
                'username': username,
                'profile_image_path': profile_image_path,
            }
            return data, 200, {'content-type': 'application/json'}
        else:
            return cognito_response

@bp.route('/student', methods = ['POST', 'GET'])
@cross_origin()
def student():
    if request.method == 'GET':
        dynamodb_response, success = dynamodb.get_students()
        if success:
            data = {
                'items': dynamodb_response['Items']
            }
            return data, 200, {'content-type': 'application/json'}
        else:
            return dynamodb_response
    elif request.method == 'POST':
        content = request.get_json()
        name = content['name']
        code = content['code']
        data_uri = content['data_uri']
        
        if data_uri:
            bucketname = creds.BUCKET_NAME
            s3_response, metadata = s3.upload_image(bucketname, creds.BUCKET_FOLDER_STUDENTS, name, data_uri)
            if metadata:
                full_image_path = metadata['full_path']
                relative_image_path = metadata['key']
                dynamodb_response, success = dynamodb.add_student(code, name, full_image_path, relative_image_path)
                if success:
                    data = {
                        'code': code,
                        'name': name,
                    }
                    return data, 200, {'content-type': 'application/json'}
                else:
                    return dynamodb_response
            else:
                return s3_response
        else:
            return bad_request('Error en el archivo')
        
@bp.route('/attendance', methods = ['POST', 'GET'])
@cross_origin()
def attendance():
    if request.method == 'GET':
        dynamodb_response, success = dynamodb.get_attendances()
        if success:
            data = {
                'items': dynamodb_response['Items']
            }
            return data, 200, {'content-type': 'application/json'}
        else:
            return dynamodb_response
    elif request.method == 'POST':
        content = request.get_json()
        name = content['name']
        similarity = int(content['similarity'])
        data_uri = content['data_uri']
        bucketname = creds.BUCKET_NAME
        
        students_dynamodb_response, success = dynamodb.get_students()
        if success:
            s3_response, metadata = s3.upload_image(bucketname, creds.BUCKET_FOLDER_GROUPS, name, data_uri)
            if metadata:
                full_image_path = metadata['full_path']
                relative_image_path = metadata['key']
            
                dynamodb_response, attendance_id, timestamp, success = dynamodb.add_attendance(name, full_image_path, relative_image_path, similarity)
                if success:
                    for student in students_dynamodb_response['Items']:
                        rek_response, success = rekognition.compare_faces_image_path_path(bucketname, student['relative_image_path'], relative_image_path, similarity)
                        if success:
                            assist = len(rek_response['FaceMatches']) > 0
                            student['assist'] = assist
                        else:
                            student['assist'] = False
                        
                        dynamodb_response, success = dynamodb.add_student_to_attendance(attendance_id, timestamp, student)
                    
                    data = {
                        'name': name,
                    }
                    return data, 200, {'content-type': 'application/json'}
                else:
                    return dynamodb_response
            else:
                return s3_response
        else:
            return students_dynamodb_response
            
    
#rekognition.create_collection_id(creds.REKOGNITION_COLLECTION_ID)
