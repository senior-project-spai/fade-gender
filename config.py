# application configuration
import os
from enum import Enum
from starlette.config import Config
from pydantic import PostgresDsn, validator
from typing import Dict, Any, Optional


class Settings():

    # Load Starlette Configuration
    # Read from environment variable
    config = Config()

    # TFServer
    RESTfulURL: str = config('RESTful_URL')
    ageURLstr: str = config('ageURL')
    emotionURLstr: str = config('emotionURL')
    faceURLstr: str = config('faceURL')
    genderURLstr: str = config('genderURL')

    @classmethod
    def tfserverurl(cls, modelurl):
        return f'{cls.RESTfulURL}{modelurl}'

    @property
    def ageurl(self):
        return self.tfserverurl(self.ageURLstr)
    @property
    def emotionurl(self):
        return self.tfserverurl(self.emotionURLstr)
    @property
    def faceurl(self):
        return self.tfserverurl(self.faceURLstr)
    @property
    def genderurl(self):
        return self.tfserverurl(self.genderURLstr)

    # Model configuration
    FACE_POS_DEPLOY_TXT: str = config('FACE_POS_DEPLOY_TXT')
    FACE_POS_WEIGHT: str = config('FACE_POS_WEIGHT')

    REPR_MODEL:str = config('REPR_MODEL')


settings = Settings()


# Enumerator

# Upload Configuation
class AllowedType(Enum):
    @classmethod
    def has(cls, value):
        return value in cls._value2member_map_


class AllowImageType(str, AllowedType):
    jpg = 'jpg'
    jpeg = 'jpeg'
    png = 'png'
    dotjpg = '.jpg'
    dotjpeg = '.jpeg'
    dotpng = '.png'


class AllowVideoType(str, AllowedType):
    mp4 = 'mp4'
    dotmp4 = '.mp4'
