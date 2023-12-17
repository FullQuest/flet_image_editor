"""Module with file processing utilities."""
import json
import flet as ft

from typing import Callable

from utils.image_processor import ImageContainer


class FileProcessor:

    def __init__(
        self,
        page: ft.Page,
        message_proc: Callable,
        image_container: ImageContainer,
        base_image: ft.Image,
        reset_sliders: Callable,
    ):
        self.page = page
        self.message = message_proc
        self.ic = image_container
        self.base_image = base_image
        self.reset_slider = reset_sliders
        self.picker = ft.FilePicker(
            on_result=self.file_process,
        )

    def is_save(self, pick_event_data: str) -> bool:
        if json.loads(pick_event_data).get('path'):
            return True
        return False

    def file_process(self, e: ft.FilePickerResultEvent):
        """Same picker for export and import, so we need to divide them."""
        if self.is_save(e.data):
            self.file_saver(e)
        else:
            self.file_picker(e)

    def file_saver(self, e: ft.FilePickerResultEvent):
        save_path = json.loads(e.data).get('path')

        if save_path[-4:] != '.png':
            save_path = f'{save_path}.png'

        self.ic.export_image(save_path)

        self.message(f'Image saved: {save_path}')

    def file_picker(self, e: ft.FilePickerResultEvent):
        if not e.files:
            return

        extension = e.files[0].path.split('.')[-1]
        if extension not in self.ic.allowed_extensions:
            self.message(f'Extension: {extension} not allowed.')
            return

        with open(e.files[0].path, 'rb') as f:
            self.ic.import_image(f.read())
            self.message(f'Opened: {e.files[0].path}')

        self.base_image.src_base64 = self.ic.base64()
        self.reset_slider(self.page)
        self.page.update()
