import os

THUMBNAIL_SIZES = os.environ.get('THUMBNAIL_SIZES')
BUCKET_TARGET = os.environ.get('BUCKET_TARGET')
BUCKET_THUMBNAIL = os.environ.get('BUCKET_THUMBNAIL')

def get_thumbnail_sizes():
    return str(THUMBNAIL_SIZES).split(':')

def get_attributes_from_event(event):
    image_key = event['Records'][0]['s3']['object']['key'] 
    image_key_splitted = image_key.split('.')
    return image_key, '.'.join(image_key_splitted[:-1]), image_key_splitted[-1]

def create_thumb_factory(event):
    raw_image_key, raw_image_name, image_extension = get_attributes_from_event(event) 

    print(f"buscando e preparando arquivo {raw_image_key} \n")

    def create_function(thumbnail_size):
        print(f"aplicando resize em {raw_image_key} para {thumbnail_size}px")
        print(f"salvando thumbnail \n")

    return create_function 



