import os
import secrets
from PIL import Image

from flask import current_app


def save_picture(picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.config['SERVER_PATH'], picture_fn)
    output_size = (125, 125)
    i = Image.open(picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


# def display_picture(logo):
#     picture_path = os.path.join(current_app.config['SERVER_PATH'], logo)
#     img = Image.open(picture_path)
#     img.show()


def recursive_flatten_iterator(d):
    for k, v in d.items():
        if isinstance(v, list):
            yield v
        if isinstance(v, dict):
            yield from recursive_flatten_iterator(v)
