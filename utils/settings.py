import json
import flet as ft

from typing import Dict, Any


def get_settings() -> Dict[str, Any]:
    """Get json App settings"""
    with open('settings.json', 'r', encoding='utf-8') as f:
        settings = json.loads(f.read())

    return settings


def setup_page(page: ft.Page):
    """Set page values from settings file."""
    settings = get_settings()

    page.window_width = settings['page_width']
    page.window_height = settings['page_height']
    page.window_resizable = settings['page_resizeable']
    page.title = settings['page_title']
    page.vertical_alignment = getattr(
        ft.MainAxisAlignment,
        settings['vertical_alignment'],
    )
