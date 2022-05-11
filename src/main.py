try:
  import unzip_requirements
except ImportError:
  pass

from src.factories import make_create_thumb, get_thumbnail_sizes 

def handler(event, context):
    create_thumb_by_size = make_create_thumb(event)
    [
        create_thumb_by_size(thumbnail_size) 
        for thumbnail_size 
        in get_thumbnail_sizes()
    ]
    return True








