from PIL import Image, ImageEnhance
from utils.filters.filter_mixin import FilterMixin


class BrightnessFilter(FilterMixin):

    @classmethod
    def apply_filter(
        cls,
        img: Image.Image,
        value: float,
    ) -> Image.Image:
        return ImageEnhance.Brightness(img).enhance(value)
