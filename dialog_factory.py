# -*- coding: utf-8 -*-
"""
Created on Sat Nov 15 13:33:15 2025
@author: dukes
"""

# --------------------------------
# dialog_factory.py (refactored)
# --------------------------------
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication

from dialogs_registry import REGISTRY
from resource_loader import ResourceLoader

class DialogFactory:
    def __init__(self, style_path=None):
        self.loader = ResourceLoader()

        # Resolve style path using loader
        if style_path:
            self.style_path = self.loader.get_style(style_path)
        else:
            self.style_path = None

        self._apply_global_styles()

    def _apply_global_styles(self):
        if self.style_path and os.path.exists(self.style_path):
            with open(self.style_path, "r") as f:
                qss = f.read()
                QApplication.instance().setStyleSheet(qss)

    def create_dialog(self, key, parent=None, params=None):
        if key not in REGISTRY:
            raise KeyError(f"Dialog '{key}' not registered.")

        ui_file, result_func, init_func = REGISTRY[key]
        ui_path = self.loader.get_ui(ui_file)

        class CallableDialog(QDialog):
            def __init__(self, parent=None, params=None):
                super().__init__(parent)
                uic.loadUi(ui_path, self)

                if init_func and params:
                    init_func(self, params)

                if hasattr(self, "buttonBox"):
                    self.buttonBox.accepted.connect(self.accept)
                    self.buttonBox.rejected.connect(self.reject)

            def __call__(self):
                if self.exec_() == QDialog.Accepted:
                    return result_func(self) if result_func else {}
                return None

        return CallableDialog(parent, params)