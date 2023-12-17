import numpy as np
import colorsys

from PIL import Image
from utils.filters.filter_mixin import FilterMixin


class HUEFilter(FilterMixin):

    @classmethod
    def apply_filter(
        cls,
        img: Image.Image,
        value: int,
    ) -> Image.Image:
        return cls.colorize(img, value)

    @classmethod
    def prepare_value(cls, value: int) -> int:
        """Convert GUI slider value to filter value.

        :param value: value from 0 to 100.
        """
        val = int(value * 3.6)

        return val + 180 if val < 180 else val - 180

    rgb_to_hsv = np.vectorize(colorsys.rgb_to_hsv)
    hsv_to_rgb = np.vectorize(colorsys.hsv_to_rgb)

    @classmethod
    def shift_hue(cls, arr, h_out):
        r, g, b, a = np.rollaxis(arr, axis=-1)
        h, s, v = cls.rgb_to_hsv(r, g, b)
        h = (h + h_out) % 1
        r, g, b = cls.hsv_to_rgb(h, s, v)
        arr = np.dstack((r, g, b, a))
        return arr

    @classmethod
    def colorize(cls, image, hue) -> Image.Image:
        """
        Colorize PIL image `original` with the given
        `hue` (hue within 0-360); returns another PIL image.
        """
        img = image.convert('RGBA')
        arr = np.array(np.asarray(img).astype('float'))
        new_img = Image.fromarray(
            cls.shift_hue(arr, hue / 360.).astype('uint8'),
            'RGBA',
        )

        return new_img
