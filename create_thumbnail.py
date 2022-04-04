
try:
  import unzip_requirements
except ImportError:
  pass
from urllib.parse import unquote_plus
from numpy import asarray
from cv2 import imdecode, imencode, IMREAD_COLOR
import boto3
import os

from resize import resize_dimensions


s3 = boto3.resource('s3')
session = boto3.Session()
client = session.client('s3')

MEDIUM_MIN_DIMENSION = 300
SMALL_MIN_DIMENSION = 150

BUCKET_TARGET = os.environ.get('BUCKET_TARGET')
BUCKET_THUMBNAIL = os.environ.get('BUCKET_THUMBNAIL')

def get_image(key_image):
    response = client.get_object(Bucket=BUCKET_TARGET, Key=key_image)
    print(response)
    return response['Body']

def buffer_to_array(buffer):
    image = asarray(bytearray(buffer.read()), dtype="uint8")
    image_array = imdecode(image, IMREAD_COLOR)
    return image_array

def get_image_attribute(key_image):
    image_helper = key_image.split('.')
    return '.'.join(image_helper[:-1]), image_helper[-1]


def generate_buffer(image_array, image_extension):
    _, image_buffer_array = imencode('.%s' % image_extension, image_array)
    byte_image = image_buffer_array.tobytes()
    return byte_image

def create_thumbnail(key_image, min_size):
    buffer = get_image(key_image)
    image_array = buffer_to_array(buffer)
    image_resized, final_width, final_height = resize_dimensions(image_array, min_size)
    image_name, image_extension = get_image_attribute(key_image)
    image_bytes = generate_buffer(image_resized, image_extension)

    thumbnail_name = '%s_%s_.%s' % (image_name, min_size, image_extension)

    s3.Bucket(BUCKET_THUMBNAIL).put_object(Key='%s' % (thumbnail_name),
                                    Body=image_bytes,
                                    # ACL='public-read',
                                    ContentType='image/%s' % image_extension)
    

def handler(event, context):

    print('[Enter the Handler]: the event, ', event)
    
    key_image = event['Records'][0]['s3']['object']['key']

    print('[original image key]: ', key_image)
    unquoted_key_image = unquote_plus(key_image)

    print('[unquoted image key]: ', unquoted_key_image )    
    create_thumbnail(unquoted_key_image, MEDIUM_MIN_DIMENSION)
    create_thumbnail(unquoted_key_image, SMALL_MIN_DIMENSION)

    print('[Finish Handler] \n')
    print('[key_image]: ', unquoted_key_image)
    
    return True

if os.environ.get('DEBUG'):
    key_img = 'originals/autonomous_car_vision.jpg'
    size = 114, 84
    create_thumbnail(key_img, size)
