from PIL import Image, ExifTags
from functools import cached_property
from fractions import Fraction
import time
import geocoder
import emoji
import pycountry
import random

from extras import MONTH, HASHTAGS


class InstaPoster():
    def __init__(self, image = "random"):
        if image == "random":
            self.image = Image.open(self._choose_image())
        else:
            self.image = Image.open(image)
        self.exif_data = self._exif_data()

    def _choose_image(self):
        pass
    
    def _exif_data(self):
        return {ExifTags.TAGS[k] : v for k, v in self.image._getexif().items() if k in ExifTags.TAGS}
    
    @cached_property
    def _camera_specs(self):
        specs = {
            "Device" : self._device,
            "ShutterSpeed" : self._shutterSpeed,
            "Date" : self._date,
            "Time" : self._time,    
        }

    @cached_property
    def _device(self):
        try:
            Make = self.exif_data["Make"]
            Model = self.exif_data["Model"]
        except:
            return None
        if Make == "Apple":
            return Model
        return Make + " " + Model
    
    @cached_property
    def _date(self):
        try:
            date = self.exif_data["DateTimeOriginal"][:10]
            return f"{date[8:10]} {MONTH[int(date[5:7])]} '{date[2:4]}"
        except:
            return None
    
    @cached_property
    def _time(self):
        try:
            return self.exif_data["DateTimeOriginal"][11:16]
        except:
            return None
    @cached_property
    def _height(self):
        try:
            h = self.exif_data["ExifImageHeight"]
            return h
        except:
            return None
    
    @cached_property
    def _width(self):
        try:
            w = self.exif_data["ExifImageWidth"]
            return w
        except:
            return None
    
    @cached_property
    def _apperture(self):
        try:
            f_number = self.exif_data["FNumber"]
            return f_number
        except:
            return None
    
    @cached_property
    def _f(self):
        try:
            f = self.exif_data["FocalLengthIn35mmFilm"]
            return f"{f} mm"
        except:
            return None
    
    @cached_property
    def _ISO(self):
        try:
            return self.exif_data["ISOSpeedRatings"]
        except:
            return None
        
    @cached_property
    def _shutterSpeed(self):
        try:
            t = self.exif_data["ExposureTime"]
            return(Fraction(t).limit_denominator())
        except:
            return None
    
    @cached_property
    def _location(self):
        try:
            GPS_INFO = self.exif_data["GPSInfo"]
            lat_hem = 1 if GPS_INFO[1] == 'N' else -1
            d, m, s = GPS_INFO[2][0], GPS_INFO[2][1], GPS_INFO[2][2]
            lat = lat_hem*(d + m/60 + s/3600)

            lng_hem = 1 if GPS_INFO[3] == 'E' else -1
            d, m, s = GPS_INFO[4][0], GPS_INFO[4][1], GPS_INFO[4][2]
            lng = lng_hem*(d + m/60 + s/3600)

            for i in range(10):
                address = geocoder.osm([lat, lng], method='reverse').current_result
                if address is not None:
                    return address
                time.sleep(0.1)
        except:
            return None


    @cached_property
    def _caption(self):
        CAPTION = f"Some Text here for the caption.\n\n"
        hashtags = HASHTAGS[:]

        if self._location is not None:
            cap = emoji.emojize(":round_pushpin:")
            city, state, country = self._location.city, self._location.state, self._location.country
            country_code = self._location.country_code.upper()
            standard_country_name = pycountry.countries.get(alpha_2 = country_code).name
            flag = emoji.emojize(f":{standard_country_name.replace(' ', '_')}:")
            cap += f" {city}, {state}, {country} {flag}.\n"
            hashtags += [f"{city.replace(' ', '_').replace('-', '_')}", f"{state.replace(' ', '_').replace('-', '_')}", f"{country.replace(' ', '_').replace('-', '_')}", f"{country_code}photograpghy"]
            if country != standard_country_name:
                hashtags += [f"{standard_country_name.replace(' ', '_')}"]
            CAPTION += cap

        has_info = False
        cap = f"Shot"
        if self._device is not None:
            cap += f" using {self._device}"
            if self._device[:6] == "iPhone":
                hashtags += ["iPhonephotography"]
            has_info = True
        if self._date is not None:
            cap += f" on {self._date}"
            has_info = True
        if has_info:
            CAPTION += cap + ".\n\n"
        
        has_info = False
        cap = emoji.emojize(":camera:")
        if self._height and self._width is not None:
            cap += f" | {self._height}x{self._width}"
        if self._f is not None:
            cap += f" | lens @ {self._f}"
            has_info = True
        if self._apperture is not None:
            cap += f" | ƒ/{self._apperture}"
            has_info = True
        if self._shutterSpeed is not None:
            cap += f" | {self._shutterSpeed} sec"
            has_info = True
        if self._ISO is not None:
            cap += f" | ISO {self._ISO}"
            has_info = True
        if has_info:
            CAPTION += cap + ".\n"
        
        CAPTION += 3*".\n"

        random.shuffle(hashtags)

        for tag in hashtags:
            CAPTION += f"#{tag} "

        return CAPTION

img = InstaPoster("Images/1.jpeg")
print(img._caption)