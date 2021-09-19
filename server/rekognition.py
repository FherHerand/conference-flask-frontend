# -*- coding: utf-8 -*-
import boto3
import botocore
from botocore.exceptions import ClientError, ParamValidationError

from server import credentials as creds
from server.utils import bad_request, logging

def get_rekognition_client():
    return boto3.client(
        'rekognition',
        aws_access_key_id=creds.rekognition['access_key_id'],
        aws_secret_access_key=creds.rekognition['secret_access_key'],
        region_name=creds.rekognition['region'],
    )

def create_collection_id(collection_id):
        client = get_rekognition_client()
        try:
            response = client.create_collection(
                CollectionId=collection_id
            )
            #logging.info(response)
            return response
        except ClientError as e:
            logging.error(e)
            return e.response

def get_face_id(bucketname, key):
        client = get_rekognition_client()
        try:
            response = client.detect_faces(
                Image={
                    'S3Object': {
                        'Bucket': bucketname,
                        'Name': key,
                    }
                },
                Attributes=[
                    'DEFAULT',
                ]
            )
            #logging.info(response)
            return response, True
        except ClientError as e:
            logging.error(e)
            return bad_request('La imagen no contiene un solo rostro'), False
        
def index_face_id(collection_id, bucketname, key):
        client = get_rekognition_client()
        try:
            response = client.index_faces(
                CollectionId=collection_id,
                Image={
                    'S3Object': {
                        'Bucket': bucketname,
                        'Name': key,
                    }
                },
                DetectionAttributes=[
                    'DEFAULT'
                ],
                MaxFaces=1,
            )
            #logging.info(response)
            response2 = client.list_faces(
                CollectionId=collection_id,
                MaxResults=100
            )
            logging.info(list(f['FaceId'] for f in response2['Faces']))
            return response, True
        except ClientError as e:
            logging.error(e)
            return bad_request('La imagen no pudo ser procesada, intente de nuevo'), False
        
def compare_faces_image_bytes_path(bucketname, source_image_bytes, target_image_path, similarity_threshold=80):
        client = get_rekognition_client()
        try:
            response = client.compare_faces(
                SourceImage={
                    'Bytes': source_image_bytes
                },
                TargetImage={
                    'S3Object': {
                        'Bucket': bucketname,
                        'Name': target_image_path,
                    }
                },
                SimilarityThreshold=similarity_threshold,
            )
            logging.info(response)
            return response, True
        except ClientError as e:
            logging.error(e)
            return bad_request('Error al comparar imágenes'), False
        
def compare_faces_image_path_path(bucketname, source_image_path, target_image_path, similarity_threshold=80):
        client = get_rekognition_client()
        try:
            response = client.compare_faces(
                SourceImage={
                    'S3Object': {
                        'Bucket': bucketname,
                        'Name': source_image_path,
                    }
                },
                TargetImage={
                    'S3Object': {
                        'Bucket': bucketname,
                        'Name': target_image_path,
                    }
                },
                SimilarityThreshold=similarity_threshold,
            )
            #logging.info(response)
            return response, True
        except ClientError as e:
            logging.error(e)
            return bad_request('Error al comparar imágenes'), False