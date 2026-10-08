"""Central dark desktop theme for v0.0.3."""

APP_STYLESHEET = """
QMainWindow, QWidget#root { background-color: #10151f; color: #edf1f7; }
QWidget { font-family: 'Segoe UI', 'Arial', sans-serif; font-size: 10pt; }
QMenuBar { background: #141c28; padding: 5px; color: #e7edf7; }
QMenuBar::item { padding: 6px 12px; border-radius: 5px; }
QMenuBar::item:selected { background: #243248; }
QMenu { background: #192435; border: 1px solid #394b63; color: #e7edf7; }
QMenu::item { padding: 7px 27px; }
QMenu::item:selected { background: #304766; }
QMenu::item:disabled { color: #7a8798; }
QToolBar { background: #151f2e; spacing: 7px; border-bottom: 1px solid #28364c; padding: 5px 10px; }
QToolButton { color: #e7edf7; border-radius: 6px; padding: 7px 12px; }
QToolButton:hover { background: #293951; }
QToolButton:disabled { color: #6e798a; }
QStatusBar { background: #141c28; color: #aebdd1; border-top: 1px solid #28364c; }
QStatusBar::item { border: 0; }
QFrame#heroCard { border: 1px solid #2e425e; background: #172335; border-radius: 17px; }
QFrame#scorePreviewFrame { border: 1px solid #384963; border-radius: 12px; background: #121c2a; }
QGraphicsView { background: #1c2635; border: 0; }
QPushButton { background: #263448; color: #eff4fc; border: 1px solid #3b526d; border-radius: 7px; padding: 6px 12px; }
QPushButton:hover { background: #354861; }
QLabel#brandSymbol { font-size: 46pt; color: #74bafc; }
QLabel#heroTitle { font-size: 24pt; font-weight: 700; color: #f5f7fc; }
QLabel#pageTitle { font-size: 19pt; font-weight: 600; color: #f5f7fc; }
QLabel#subtitle { color: #a6b8cd; font-size: 10pt; }
QLabel#eyebrow { color: #83bcf2; font-size: 9pt; font-weight: 600; }
QLabel#mutedLabel { color: #8497ae; font-size: 10pt; }
QPushButton#primaryButton { background: #3e94e9; color: white; border: none; border-radius: 8px; padding: 11px 20px; font-weight: 700; }
QPushButton#primaryButton:hover { background: #61aaf2; }
QPushButton#primaryButton:pressed { background: #2979cc; }
QMessageBox { background: #172335; color: #edf1f7; }
QMessageBox QLabel { color: #edf1f7; }
QMessageBox QPushButton { min-width: 75px; padding: 6px; }
"""
