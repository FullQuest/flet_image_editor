"""Module with mixin filter class."""
from PIL import Image


class FilterMixin:
    """Parent Mixin class for filters."""

    DEFAULT_SLIDER_VALUE = 50

    @classmethod
    def process_image(
        cls,
        img: Image.Image,
        value: int,
    ) -> Image.Image:
        """Pipeline for single filter"""
        if value == cls.DEFAULT_SLIDER_VALUE:
            return img

        prepared_value = cls.prepare_value(value)
        return cls.apply_filter(img, prepared_value)

    @classmethod
    def apply_filter(
        cls,
        img: Image.Image,
        value: float,
    ) -> Image.Image:
        """Apply filter on given image"""
        return img

    @classmethod
    def prepare_value(cls, value: int) -> float:
        """Convert GUI slider value to filter value.

        :param value: value from 0 to 100.
        """
        if value > 50:
            return ((value - 50) ** 2) / 833 + 1
            # return value / 25 LINEAR PROCESSING

        if value == 50:
            return 1

        return value / 50
