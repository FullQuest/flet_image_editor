"""Flet entrypoint."""
import flet as ft

from utils.filters.setup_sliders import SliderProcessor
from utils.image_processor import (
    ImageContainer,
    GUISettings,
)
from utils.file_processor import FileProcessor
from utils.settings import get_settings


def main(page: ft.Page):

    # Load settings from JSON
    settings = get_settings()

    page.window_width = settings['page_width']
    page.window_height = settings['page_height']
    page.window_resizable = settings['page_resizeable']
    page.title = settings['page_title']
    page.vertical_alignment = getattr(
        ft.MainAxisAlignment,
        settings['vertical_alignment'],
    )

    image_proc = ImageContainer(settings['preview_resolution'])
    base_image = ft.Image(src_base64=image_proc.base64())
    slider_proc = SliderProcessor(page, base_image, image_proc)

    # REDO UNDO FUNCTIONAL
    def undo(_event):
        image_proc.undo()
        base_image.src_base64 = image_proc.base64()
        update_gui_filters(image_proc.gui_settings())
        page.update()

    def redo(_event):
        image_proc.redo()
        base_image.src_base64 = image_proc.base64()
        update_gui_filters(image_proc.gui_settings())
        page.update()

    def update_gui_filters(gui_settings: GUISettings):
        for slider_name, slider in slider_proc.sliders_dict.items():
            slider.value = gui_settings[slider_name]

    # Notification text preparation
    notification_text = ft.Text("")

    def message(text: str):
        notification_text.value = text
        page.update()

    # File picker setup
    file_processor = FileProcessor(
        page,
        message,
        image_proc,
        base_image,
        slider_proc.reset_slider,
    )
    page.overlay.append(file_processor.picker)

    # Upper panel setup
    page.add(ft.Row(
        [
            ft.ElevatedButton(
                "Choose files...",
                on_click=lambda _: file_processor.picker.pick_files(
                    allow_multiple=False,
                    allowed_extensions=['jpg', 'jpeg', 'webp', 'png'],
                ),
            ),
            ft.IconButton(ft.icons.UNDO, on_click=undo),
            ft.IconButton(ft.icons.REDO, on_click=redo),
            ft.ElevatedButton(
                "Export",
                on_click=lambda _: file_processor.picker.save_file(
                    allowed_extensions=['png']
                )
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    ))

    # Sliders setup
    sliders_column = slider_proc.get_sliders_column()
    page.add(ft.Row(
        [
            base_image,
            ft.Column(sliders_column),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    ))

    page.add(ft.Row([notification_text]))


if __name__ == '__main__':
    ft.app(target=main)
