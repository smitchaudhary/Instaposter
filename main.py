import os.path
import instabot
import getpass
from PIL import Image as pillowImage
from exif import Image as exifImage
from PIL import ExifTags

def login(path = "credentials"):
    pass

def select_photo():
    pass

def make_caption():
    pass

def edit_photo():
    pass

def post_photo():
    pass

def get_exif():
    pillow_image = pillowImage.open("Images/1.jpeg")
    img_exif = pillow_image.getexif()

    for tag in PILLOW_TAGS:
        english_tag = ExifTags.TAGS[tag]
        print(english_tag)
    return 1

if __name__ == '__main__':
    PILLOW_TAGS = [
        34853, # GPS Tag
        271, # Make
        272, # Model
        306, # Date and Time
    ]

    EXIF_TAGS = [
        "make",
        "model",
        "datetime_original",
        "gps_latitude",
        "gps_longitude",
        "gps_latitude_ref",
        "gps_longitude_ref",
        "gps_altitude",
    ]

    output = get_exif()
    print(output)