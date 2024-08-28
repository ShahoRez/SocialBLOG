# users/picturhandler.py

import os
from PIL import Image
from flask import current_app


def add_profile_pic(pic_upload, username):
    filename = pic_upload.filename
    file_ext = filename.split(".")[-1]
    print(file_ext)
    storage_filename = str(username) + "." + file_ext
    print(storage_filename)
    filepath = os.path.join(
        current_app.root_path, "static\profile_pic", storage_filename
    )
    print(filepath)
    output_size = (150, 150)
    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename
