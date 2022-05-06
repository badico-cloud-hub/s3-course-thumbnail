from factories import create_thumb_factory, get_thumbnail_sizes 

def handler(event, context):
    create_thumb_by_size = create_thumb_factory(event)
    [
        create_thumb_by_size(thumbnail_size) 
        for thumbnail_size 
        in get_thumbnail_sizes()
    ]
    return True








