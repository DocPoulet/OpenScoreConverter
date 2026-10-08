"""Application startup and top-level Qt configuration."""

import sys
from collections.abc import Sequence

from .config import APP_NAME, APP_ORGANIZATION, VERSION


def main(argv: Sequence[str] | None = None) -> int:
    """Create the Qt application and run its event loop.

    Args:
        argv: Optional command-line arguments. Defaults to sys.argv.

    Returns:
        Qt's process exit code.
    """
    try:
        from PySide6.QtWidgets import QApplication
    except ImportError as exc:
        raise SystemExit(
            "PySide6 is not installed. Run: python -m pip install -r requirements.txt"
        ) from exc

    from .ui.main_window import MainWindow
    from .ui.theme import APP_STYLESHEET

    app = QApplication(list(argv if argv is not None else sys.argv))
    app.setApplicationName(APP_NAME)
    app.setApplicationDisplayName(APP_NAME)
    app.setOrganizationName(APP_ORGANIZATION)
    app.setApplicationVersion(VERSION)
    app.setStyle("Fusion")
    app.setStyleSheet(APP_STYLESHEET)

    window = MainWindow()
    window.show()
    return app.exec()
