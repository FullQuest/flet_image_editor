"""Module with base setup for filters."""
import flet as ft

from typing import Optional, Dict

from utils.image_processor import ImageContainer
from utils.filters.setup_filters import ImageSettings


class SliderProcessor:
    """Slider processor for Flet GUI."""

    def __init__(
        self,
        page: ft.Page,
        base_image: ft.Image,
        image_container: ImageContainer,
    ):
        self.page = page
        self.base_image = base_image
        self.ic = image_container
        self.sliders_dict: Dict[str, ft.Slider] = {}

    def reset_slider(
        self,
        page: ft.Page,
        _event=None,
        slider_name: Optional[str] = None,
    ):
        slider_value = ImageSettings.default_gui_settings()
        if not slider_name:
            for filter_name, slider in self.sliders_dict.items():
                slider.value = slider_value[filter_name]
        else:
            self.sliders_dict[slider_name].value = slider_value[slider_name]

        self.update_settings()
        page.update()

    def _get_slider(
        self,
        slider_name: str,
        icon
    ) -> ft.Row:
        slider = ft.Slider(
            min=0, max=100, value=50, divisions=25,
            on_change_end=self.update_settings,
        )
        slider_icon = ft.Icon(icon)
        self.sliders_dict[slider_name] = slider

        reset_slider_btn = ft.IconButton(
            ft.icons.CHANGE_CIRCLE,
            on_click=lambda e: self.reset_slider(self.page, e, slider_name),
        )
        return ft.Row([slider_icon, slider, reset_slider_btn])

    def get_sliders_column(self):
        """Get Flet column data with sliders."""
        sliders_column = [
            *[
                self._get_slider(*slider)
                for slider in ImageSettings.slider_settings()
            ],
            # ft.Row([ft.IconButton(    # ICON WAY TO RESET
            #     ft.icons.CHANGE_CIRCLE,
            #     on_click=lambda e: self.reset_slider(self.page, e),
            # )]),
            ft.Row([ft.TextButton(
                "Reset all",
                on_click=lambda e: self.reset_slider(self.page, e),
            )]),
        ]
        return sliders_column

    def update_settings(self, _event=None):
        """Main function that updates image"""
        filters = {
            slider_name: int(float(slider.value))
            for slider_name, slider in self.sliders_dict.items()
        }

        self.base_image.src_base64 = self.ic.process_preview(filters)
        self.page.update()
