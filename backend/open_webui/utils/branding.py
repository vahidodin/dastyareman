"""Local branding files and display name.

Uploaded assets are kept on the data disk and copied onto the static
directory at startup, so a new container still shows the configured brand.
"""

from __future__ import annotations

import logging
import shutil
from pathlib import Path

from open_webui.env import DATA_DIR, STATIC_DIR, WEBUI_NAME

log = logging.getLogger(__name__)

BRANDING_DIR = Path(DATA_DIR) / 'branding'

# slot -> static filenames written from that upload
ASSET_TARGETS = {
    'logo': ['logo.png'],
    'favicon': ['favicon.png', 'favicon-96x96.png'],
    'splash': ['splash.png'],
    'splash-dark': ['splash-dark.png'],
    'apple-touch-icon': ['apple-touch-icon.png'],
    'pwa-192': ['web-app-manifest-192x192.png'],
    'pwa-512': ['web-app-manifest-512x512.png'],
}


def branding_path(slot: str) -> Path:
    return BRANDING_DIR / f'{slot}.png'


def apply_branding_assets() -> None:
    """Copy persisted uploads onto the static files the UI actually serves."""
    if not BRANDING_DIR.exists():
        return
    static_dir = Path(STATIC_DIR)
    static_dir.mkdir(parents=True, exist_ok=True)
    for slot, targets in ASSET_TARGETS.items():
        source = branding_path(slot)
        if not source.is_file():
            continue
        for name in targets:
            destination = static_dir / name
            shutil.copyfile(source, destination)
            log.info('Applied branding asset %s -> %s', slot, destination.name)


def save_branding_asset(slot: str, data: bytes) -> None:
    if slot not in ASSET_TARGETS:
        raise ValueError(f'Unknown branding asset: {slot}')
    if not data:
        raise ValueError('Empty branding file')
    BRANDING_DIR.mkdir(parents=True, exist_ok=True)
    branding_path(slot).write_bytes(data)
    apply_branding_assets()


async def apply_runtime_branding(app) -> None:
    """Refresh the process-wide name from config, then the static assets."""
    from open_webui.models.config import Config

    name = await Config.get('ui.branding.name')
    if isinstance(name, str) and name.strip():
        app.state.WEBUI_NAME = name.strip()
    elif not getattr(app.state, 'WEBUI_NAME', None):
        app.state.WEBUI_NAME = WEBUI_NAME
    apply_branding_assets()
