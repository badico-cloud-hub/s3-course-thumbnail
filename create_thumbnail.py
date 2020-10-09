
import numpy as np
import cv2
import boto3
import os

s3 = boto3.resource('s3')
session = boto3.Session()
client = session.client('s3')

BUCKET_TARGET = os.environ.get('BUCKET_TARGET')
BUCKET_THUMBNAIL = os.environ.get('BUCKET_THUMBNAIL')

def get_image(key_image):
    response = client.get_object(Bucket=BUCKET_TARGET, Key=key_image)
    print(response)
    return response['Body']

def buffer_to_array(buffer):
    image = np.asarray(bytearray(buffer.read()), dtype="uint8")
    image_array = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image_array

def get_image_attribute(key_image):
    prefix, file = key_image.split('/')
    image_helper = file.split('.')
    return image_helper[0], image_helper[1], prefix


def generate_buffer(image_array, image_extension):
    _, image_buffer_array = cv2.imencode('.%s' % image_extension, image_array)
    byte_image = image_buffer_array.tobytes()
    return byte_image

def create_thumbnail(key_image, size):
    buffer = get_image(key_image)
    image_array = buffer_to_array(buffer)
    image_resized = cv2.resize(image_array, size, interpolation=cv2.INTER_AREA)
    image_name, image_extension, prefix = get_image_attribute(key_image)
    image_bytes = generate_buffer(image_resized, image_extension)

    thumbnail_name = '%s_%sx%s.%s' % (image_name, size[0], size[1], image_extension)


    s3.Bucket(BUCKET_THUMBNAIL).put_object(Key='%s/%s' % (prefix, thumbnail_name),
                                    Body=image_bytes,
                                    ACL='public-read',
                                    ContentType='image/%s' % image_extension)
    

def handler(event, context):
    
    key_image = event['Records'][0]['s3']['object']['key']
    size = int(114), int(84)

    create_thumbnail(key_image, size)
    
    return True

if os.environ.get('DEBUG'):
    key_img = 'originals/autonomous_car_vision.jpg'
    size = 114, 84
    create_thumbnail(key_img, size)