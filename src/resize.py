from cv2 import resize as rsz, imencode, INTER_AREA

def get_the_lower_value(width, height):
    return width if width <= height else height

def check_dimensions(width, height, min_size):
    width_lower_than_min = width < min_size
    height_lower_than_min = height < min_size
    return width_lower_than_min or height_lower_than_min 

def resize(image_array, thumb_size):
    print(f"aplicando resize para {thumb_size}px")

    height, width, _ = image_array.shape
    print('[original height]: ', height)
    print('[original width]: ', width)

    dimension_lower_than_min = check_dimensions(width, height, thumb_size)
    print('[dimension_lower_than_min]: ', dimension_lower_than_min)

    if dimension_lower_than_min:
        dimension = [int(width), int(height)]
        return rsz(image_array, dimension, interpolation=INTER_AREA)

    resize_factor_based_on_width = width / thumb_size
    resize_factor_based_on_height = height / thumb_size

    print('[width factor]: ', resize_factor_based_on_width)
    print('[height factor]: ', resize_factor_based_on_height)

    lower_ratio = get_the_lower_value(
        resize_factor_based_on_width, 
        resize_factor_based_on_height
    )

    print('[lower ratio]: ', lower_ratio)

    thumb_height = height / lower_ratio
    thumb_width = width / lower_ratio

    print('[new height]: ', thumb_height)
    print('[new_width]: ', thumb_width)

    dimension = [int(thumb_width), int(thumb_height)]
    return rsz(image_array, dimension, interpolation=INTER_AREA)









