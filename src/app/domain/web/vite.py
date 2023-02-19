from __future__ import annotations

import json
from pathlib import Path
from typing import Any, ClassVar
from urllib.parse import urljoin

import markupsafe
from pydantic import BaseModel
from starlite import TemplateConfig
from starlite.contrib.jinja import JinjaTemplateEngine

from app.lib import settings


class ViteConfig(BaseModel):
    """Configuration for InertiaJS support.

    To enable inertia JS responses, pass an instance of this class to the :class:`Starlite <starlite.app.Starlite>` constructor
    using the 'plugins' key.
    """

    hot_reload: bool = False
    is_react: bool = False
    assets_path: str = "static/"
    vite_manifest_path: Path = Path(settings.PUBLIC_DIR / "manifest.json")
    vite_host: str = "localhost"
    vite_protocol: str = "http"
    vite_port: int = 3000


vite_config = ViteConfig()


class ViteLoader:
    """Vite  manifest loader."""

    _instance: ClassVar[ViteLoader | None] = None
    _manifest: ClassVar[dict[str, Any]] = {}

    def __new__(cls) -> ViteLoader:
        """Singleton manifest loader."""
        if cls._instance is None:
            cls._manifest = cls.parse_manifest()
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    def parse_manifest() -> dict[str, Any]:
        """Read and parse the Vite manifest file.

        Raises:
            RuntimeError: if cannot load the file or JSON in file is malformed.
        """
        manifest = {}
        if not vite_config.hot_reload:
            with open(vite_config.vite_manifest_path) as manifest_file:
                manifest_content = manifest_file.read()
            try:
                manifest = json.loads(manifest_content)
            except Exception as exc:
                raise RuntimeError(
                    "Cannot read Vite manifest file at %s",
                    vite_config.vite_manifest_path,
                ) from exc
        return manifest

    def generate_vite_server_url(self, path: str | None = None) -> str:
        """Generate an URL to and asset served by the Vite development server.

        Keyword Arguments:
            path {Optional[str]} -- Path to the asset. (default: {None})

        Returns:
            str -- Full URL to the asset.
        """
        base_path = "{protocol}://{host}:{port}".format(
            protocol=vite_config.vite_protocol,
            host=vite_config.vite_host,
            port=vite_config.vite_port,
        )
        return urljoin(
            base_path,
            urljoin(vite_config.assets_path, path if path is not None else ""),
        )

    def generate_script_tag(self, src: str, attrs: dict[str, str] | None = None) -> str:
        """Generate an HTML script tag."""
        attrs_str = ""
        if attrs is not None:
            attrs_str = " ".join([f'{key}="{value}"' for key, value in attrs.items()])

        return f'<script {attrs_str} src="{src}"></script>'

    def generate_stylesheet_tag(self, href: str) -> str:
        """Generate and HTML <link> stylesheet tag for CSS.

        Arguments:
            href {str} -- CSS file URL.

        Returns:
            str -- CSS link tag.
        """
        return f'<link rel="stylesheet" href="{href}" />'

    def generate_vite_ws_client(self) -> str:
        """Generate the script tag for the Vite WS client for HMR.

        Only used in development, in production this method returns
        an empty string.

        Returns:
            str -- The script tag or an empty string.
        """
        if not vite_config.hot_reload:
            return ""

        return self.generate_script_tag(
            self.generate_vite_server_url("@vite/client"),
            {"type": "module"},
        )

    def generate_vite_react_hmr(self) -> str:
        """Generate the script tag for the Vite WS client for HMR.

        Only used in development, in production this method returns
        an empty string.

        Returns:
            str -- The script tag or an empty string.
        """
        if vite_config.is_react and vite_config.hot_reload:
            return f"""
                <script type="module">
                import RefreshRuntime from '{self.generate_vite_server_url()}@react-refresh'
                RefreshRuntime.injectIntoGlobalHook(window)
                window.$RefreshReg$ = () => {{}}
                window.$RefreshSig$ = () => (type) => type
                window.__vite_plugin_react_preamble_installed__=true
                </script>
                """
        return ""

    def generate_vite_asset(self, path: str, scripts_attrs: dict[str, str] | None = None) -> str:
        """Generate all assets include tags for the file in argument.

        Returns:
            str -- All tags to import this asset in your HTML page.
        """
        if vite_config.hot_reload:
            return self.generate_script_tag(
                self.generate_vite_server_url(path),
                {"type": "module", "async": "", "defer": ""},
            )

        if path not in self._manifest:
            raise RuntimeError("Cannot find %s in Vite manifest at %s", path, vite_config.vite_manifest_path)

        tags = []
        manifest_entry: dict = self._manifest[path]
        if not scripts_attrs:
            scripts_attrs = {"type": "module", "async": "", "defer": ""}

        # Add dependent CSS
        if "css" in manifest_entry:
            for css_path in manifest_entry.get("css", {}):
                tags.append(self.generate_stylesheet_tag(urljoin(vite_config.assets_path, css_path)))

        # Add dependent "vendor"
        if "imports" in manifest_entry:
            for vendor_path in manifest_entry.get("imports", {}):
                tags.append(self.generate_vite_asset(vendor_path, scripts_attrs=scripts_attrs))

        # Add the script by itself
        tags.append(
            self.generate_script_tag(
                urljoin(vite_config.assets_path, manifest_entry["file"]),
                attrs=scripts_attrs,
            )
        )

        return "\n".join(tags)


def vite_hmr_client() -> markupsafe.Markup:
    """Generate the script tag for the Vite WS client for HMR.

    Only used in development, in production this method returns an empty string.


    Returns:
        str -- The script tag or an empty string.
    """
    tags: list = []
    tags.append(ViteLoader().generate_vite_react_hmr())
    tags.append(ViteLoader().generate_vite_ws_client())
    return markupsafe.Markup("\n".join(tags))


def vite_asset(path: str, scripts_attrs: dict[str, str] | None = None) -> markupsafe.Markup:
    """Generate all assets include tags for the file in argument.

    Generates all scripts tags for this file and all its dependencies
    (JS and CSS) by reading the manifest file (for production only).
    In development Vite imports all dependencies by itself.
    Place this tag in <head> section of your page
    (this function marks automatically <script> as "async" and "defer").

    Arguments:
        path {str} -- Path to a Vite asset to include.

    Keyword Arguments:
        scripts_attrs {Optional[Dict[str, str]]} -- Override attributes added to scripts tags. (default: {None})
        with_imports {bool} -- If generate assets for dependant assets of this one. (default: {True})

    Returns:
        str -- All tags to import this asset in your HTML page.
    """
    return markupsafe.Markup(ViteLoader().generate_vite_asset(path, scripts_attrs=scripts_attrs))


def vite_asset_url(path: str) -> str:
    """Generate only the URL of an asset managed by ViteJS.

    Warning, this function does not generate URLs for dependant assets.

    Arguments:
        path {str} -- Path to a Vite asset.

    Returns:
        [type] -- The URL of this asset.
    """
    return ViteLoader().generate_vite_asset(path)


template_config = TemplateConfig(
    directory=settings.TEMPLATES_DIR,
    engine=JinjaTemplateEngine,
)
template_config.engine_instance.engine.globals["vite_hmr_client"] = vite_hmr_client
template_config.engine_instance.engine.globals["vite_asset"] = vite_asset
