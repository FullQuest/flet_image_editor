"""Module with static data for setup"""
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass
from flet import icons

from utils.filters.filter_mixin import FilterMixin
from utils.filters.units.brightness import BrightnessFilter
from utils.filters.units.contrast import ContrastFilter
from utils.filters.units.hue import HUEFilter
from utils.filters.units.saturation import SaturationFilter
from utils.filters.units.sharpness import SharpnessFilter


@dataclass
class ImageSettings:
    """Class to connect filter modules with app."""

    @classmethod
    def filter_settings(cls) -> List[Dict[str, Any]]:
        return [
            {
                'name': 'contrast',
                'icon': icons.CONTRAST,
                'proc': ContrastFilter,
            }, {
                'name': 'saturation',
                'icon': icons.COLOR_LENS,
                'proc': SaturationFilter,
            }, {
                'name': 'brightness',
                'icon': icons.BLUR_ON_SHARP,
                'proc': SharpnessFilter,
            }, {
                'name': 'sharpness',
                'icon': icons.BRIGHTNESS_6,
                'proc': BrightnessFilter,
            },
            {
                'name': 'hue',
                'icon': icons.FORMAT_COLOR_FILL,
                'proc': HUEFilter,
            },
        ]

    @classmethod
    def slider_settings(cls) -> List[Tuple[str, str]]:
        return [
            (f['name'], f['icon'])
            for f in cls.filter_settings()
        ]

    @classmethod
    def default_gui_settings(cls):
        return {
            img_filter['name']: BrightnessFilter.DEFAULT_SLIDER_VALUE
            for img_filter in cls.filter_settings()
        }

    @classmethod
    def filters(cls) -> Dict[str, FilterMixin]:
        return {
            el['name']: el['proc']
            for el in cls.filter_settings()
        }
