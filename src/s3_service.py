import boto3
import os

s3 = boto3.resource('s3')
session = boto3.Session()
client = session.client('s3')

BUCKET_TARGET = os.environ.get('BUCKET_TARGET')
BUCKET_THUMBNAIL = os.environ.get('BUCKET_THUMBNAIL')

def get_image(key_image):
    response = client.get_object(Bucket=BUCKET_TARGET, Key=key_image)
    return response['Body']

def save_image(key_image, image_extension, image_bytes):
    client.put_object(Bucket=BUCKET_THUMBNAIL, 
                      Key=key_image,
                      Body=image_bytes,
                      ContentType=f"image/{image_extension}"
                      )
