# =========================
# resource_loader.py
# =========================
import sys
import logging
from pathlib import Path

# Configure logging globally
logging.basicConfig(
    level=logging.INFO,  # switch to DEBUG for more detail
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

class ResourceLoader:
    """
    Unified resource loader for dev and frozen states.
    Anchors everything to project root (next to main.py) or PyInstaller _MEIPASS.
    Logs directory selection and missing resources.
    """

    def __init__(self):
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # PyInstaller bundle
            self.base_path = Path(sys._MEIPASS)
            logging.debug("ResourceLoader: Frozen mode; base_path set to _MEIPASS")
        else:
            # Development mode
            self.base_path = Path(__file__).resolve().parent
            logging.debug("ResourceLoader: Dev mode; base_path set to script directory")

        self.resources_dir = self.base_path / "resources"
        logging.info(f"ResourceLoader: resources directory -> {self.resources_dir}")

    def get(self, *parts: str) -> str:
        """
        Resolve a resource path under the resources directory.
        Logs a warning if the file does not exist.
        """
        path = self.resources_dir.joinpath(*parts)
        if not path.exists():
            logging.warning(f"ResourceLoader: Resource not found -> {path}")
        else:
            logging.debug(f"ResourceLoader: Resource resolved -> {path}")
        return str(path)

    def get_ui(self, filename: str) -> str:
        return self.get("ui", filename)

    def get_style(self, filename: str) -> str:
        return self.get("styles", filename)

    def get_image(self, filename: str) -> str:
        return self.get("images", filename)

    def get_sound(self, filename: str) -> str:
        return self.get("sounds", filename)

    def require(self, *parts: str) -> str:
        """
        Like get(), but raises FileNotFoundError if the resource is missing.
        Useful when a resource is mandatory for startup.
        """
        path = Path(self.get(*parts))
        if not path.exists():
            raise FileNotFoundError(f"Required resource missing: {path}")
        return str(path)

    # =========================
    # EXTENSION EXAMPLES
    # =========================
    # To add new resource categories, simply add methods like:
    #
    # def get_font(self, filename: str) -> str:
    #     return self.get("fonts", filename)
    #
    # def get_data(self, filename: str) -> str:
    #     return self.get("data", filename)
    #
    # This keeps the loader auditable and easy to extend.