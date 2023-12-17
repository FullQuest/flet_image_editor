"""Image processing Module."""
import io
import base64

from PIL import Image
from typing import List, Dict, Tuple, Optional

from utils.filters.setup_filters import (
    ImageSettings,
)

GUISettings = Dict[str, int]
ImageBase64 = str
CachedMove = Tuple[GUISettings, ImageBase64]


class ImageContainer:
    """Class that processes the image and contains settings."""

    def __init__(self, max_scale: int = 512):
        self.scale = max_scale
        image: Image.Image = Image.new('RGBA', (self.scale, self.scale))

        self.images_raw: List[Image.Image] = [image]
        self.image_preview: Image.Image = image

        self.settings_history: List[CachedMove] = [(
             ImageSettings.default_gui_settings(),
             self.to_base(image)
        )]
        self.current_index = 0
        self.allowed_extensions = ['jpg', 'png', 'webp']
        self.filters = ImageSettings.filters()

    def import_image(self, image: bytes):
        new_image: Image.Image = Image.open(io.BytesIO(image))
        new_image = new_image.convert('RGBA')

        self.images_raw = [new_image]

        ratio = max(new_image.size) / self.scale

        new_image_scale = (
            int(new_image.size[0] / ratio),
            int(new_image.size[1] / ratio),
        )

        new_image = new_image.resize(new_image_scale)

        self.image_preview = new_image
        self.settings_history = [(
            ImageSettings.default_gui_settings(),
            self.to_base(new_image),
        )]
        self.current_index = 0

    def export_image(self, path: str):
        processed_img = self.process_filters(
            self.gui_settings(),
            self.images_raw[0],
        )
        processed_img.save(path)

    def cur(self) -> CachedMove:
        """Cur tuple"""
        return self.settings_history[self.current_index]

    def gui_settings(self):
        """Cur gui settings"""
        return self.cur()[0]

    def base64(self) -> str:
        """Cur base64"""
        return self.cur()[1]

    def upd(
        self,
        image: Image.Image,
        gui_settings: GUISettings,
    ):
        """Update current image"""
        self.settings_history = self.settings_history[:self.current_index+1]
        self.settings_history.append((
            gui_settings,
            self.to_base(image)
        ))
        self.current_index = len(self.settings_history) - 1

    def undo(self):
        if self.current_index >= 1:
            self.current_index -= 1

    def redo(self):
        if self.current_index < len(self.settings_history) - 1:
            self.current_index += 1

    @staticmethod
    def to_base(image: Image.Image) -> ImageBase64:
        """Convert image to base64"""
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        return img_str

    def process_preview(self, gui_settings: GUISettings) -> ImageBase64:
        """
        :param gui_settings: must be in self filters. Ex: {"contrast": 75}
        :return: processed image
        """
        processed_image = self.process_filters(gui_settings)
        self.upd(processed_image, gui_settings)

        return self.base64()

    def process_filters(
        self,
        gui_settings: GUISettings,
        image: Optional[Image.Image] = None,
    ) -> Image.Image:
        image = image or self.image_preview

        for filter_name, filter_class in self.filters.items():
            value = gui_settings[filter_name]
            image = filter_class.process_image(image, value)

        return image
