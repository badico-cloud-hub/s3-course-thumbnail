import os
from urllib.parse import unquote_plus
from numpy import asarray
from cv2 import imdecode, imencode, IMREAD_COLOR

import src.s3_service as s3
from src.resize import resize 

THUMBNAIL_SIZES = os.environ.get('THUMBNAIL_SIZES')

def get_thumbnail_sizes():
    str_values = str(THUMBNAIL_SIZES).split(':')
    mapObj = map(lambda x: int(x), str_values)
    return list(mapObj)

def get_attributes_from_event(event):
    image_key = event['Records'][0]['s3']['object']['key'] 
    unquoted_image_key = unquote_plus(image_key) 
    image_key_splitted = unquoted_image_key.split('.')
    return unquoted_image_key, '.'.join(image_key_splitted[:-1]), image_key_splitted[-1]

def resolve_image(image_key):
    buffer = s3.get_image(image_key)
    buffer_content = buffer.read()
    bytearray_obj = bytearray(buffer_content)
    image = asarray(bytearray_obj, dtype="uint8")
    return imdecode(image, IMREAD_COLOR)

def make_save_thumbnail(image_name, image_extension):

    def save_thumbnail(thumbnail_array, thumbnail_size):
        _, thumb_buffer_array = imencode(f".{image_extension}", thumbnail_array)
        thumb_bytes = thumb_buffer_array.tobytes()
        thumbnail_name = f"{image_name}_{thumbnail_size}_.{image_extension}"
        s3.save_image(thumbnail_name, image_extension, thumb_bytes)
        return
    
    return save_thumbnail

def make_create_thumb(event):
    image_key, image_name, image_extension = get_attributes_from_event(event) 
    image = resolve_image(image_key)
    save_thumbnail = make_save_thumbnail(image_name, image_extension)

    def create_function(thumbnail_size):
        thumbnail = resize(image, thumbnail_size)
        save_thumbnail(thumbnail, thumbnail_size)

    return create_function 



