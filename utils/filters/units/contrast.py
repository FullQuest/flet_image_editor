from PIL import Image, ImageEnhance
from utils.filters.filter_mixin import FilterMixin


class ContrastFilter(FilterMixin):

    @classmethod
    def apply_filter(
        cls,
        img: Image.Image,
        value: float,
    ) -> Image.Image:
        return ImageEnhance.Contrast(img).enhance(value)
