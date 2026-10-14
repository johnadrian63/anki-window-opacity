from aqt import mw, gui_hooks
from aqt.qt import (QAction, QDialog, QVBoxLayout, QHBoxLayout,
                    QSlider, QLabel, QPushButton, Qt)

KEY = "window_opacity_percent"


def _get():
    try:
        return int(mw.pm.profile.get(KEY, 100))
    except Exception:
        return 100


def _apply(widget, percent):
    widget.setWindowOpacity(max(30, min(100, percent)) / 100)


def _set(percent):
    mw.pm.profile[KEY] = percent
    _apply(mw, percent)


def open_dialog():
    dlg = QDialog(mw)
    dlg.setWindowTitle("Window opacity")
    dlg.setMinimumWidth(320)
    layout = QVBoxLayout(dlg)

    label = QLabel()
    slider = QSlider(Qt.Orientation.Horizontal)
    slider.setRange(30, 100)
    slider.setValue(_get())

    def changed(value):
        label.setText(f"Opacity: {value}%")
        _set(value)

    slider.valueChanged.connect(changed)
    changed(slider.value())

    reset = QPushButton("Reset to 100%")
    reset.clicked.connect(lambda: slider.setValue(100))
    close = QPushButton("Close")
    close.clicked.connect(dlg.accept)
    row = QHBoxLayout()
    row.addWidget(reset)
    row.addStretch()
    row.addWidget(close)

    layout.addWidget(label)
    layout.addWidget(slider)
    layout.addLayout(row)
    dlg.exec()


def on_profile_open():
    _apply(mw, _get())


def on_browser(browser):
    _apply(browser, _get())


gui_hooks.profile_did_open.append(on_profile_open)
gui_hooks.browser_will_show.append(on_browser)

action = QAction("Window opacity...", mw)
action.triggered.connect(open_dialog)
mw.form.menuTools.addAction(action)