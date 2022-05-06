from cv2 import resize, INTER_AREA

def check_dimensions(width, height, min_size):
    width_lower_than_min = width < min_size
    height_lower_than_min = height < min_size
    return width_lower_than_min or height_lower_than_min 

def get_the_lower_value(width, height):
    print('[Enter "get_the_lower_value" func]')
    return width if width <= height else height

def get_new_size(image_array, min_size):
    print('[Enter "get_new_size" func]')
    print('[min size]: ', min_size)
    height, width, channels = image_array.shape

    print('[height from "shape"]: ', height)
    print('[width from "shape"]: ', width)

    some_dimension_lower_than_min = check_dimensions(width, height, min_size)

    print('[some_dimension_lower_than_min]: ', some_dimension_lower_than_min)

    if some_dimension_lower_than_min:
        return int(width), int(height)

    resize_factor_based_on_width = width / min_size
    resize_factor_based_on_height = height / min_size

    print('[height factor]: ', resize_factor_based_on_height)
    print('[width factor ]: ', resize_factor_based_on_width)

    lower_ratio = get_the_lower_value(resize_factor_based_on_width, resize_factor_based_on_height)

    print('[lower ratio]: ', lower_ratio)

    new_height = height / lower_ratio
    new_width = width / lower_ratio

    print('[new height]: ', new_height)
    print('[new_width]: ', new_width)

    return int(new_width), int(new_height)

def resize_dimensions(image_array, min_size):
    print('[enter the "resize_dimensions" func]')

    new_size = get_new_size(image_array, min_size)

    print('[new_size]: ', new_size)
    print('[new_size type]: ', type(new_size))

    image_resized = resize(image_array, new_size, interpolation=INTER_AREA)

    print('[image_resized]: ', image_resized)
    print('[image_resized type]: ', type(image_resized))

    return image_resized, new_size[0], new_size[1] 