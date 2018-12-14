from ..django._core import INSTALLED_APPS

INSTALLED_APPS.append('easy_thumbnails')
INSTALLED_APPS.append('image_cropping')

from easy_thumbnails.conf import Settings as thumbnail_settings
THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS