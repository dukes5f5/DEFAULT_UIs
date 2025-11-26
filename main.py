# main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from dialog_factory import DialogFactory
from resource_loader import ResourceLoader
from license_manager import LicenseManager
from stdout_console import StdoutConsole  # ✅ Import your new class

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.loader = ResourceLoader()

        # Load UI and stylesheet
        ui_path = self.loader.get_ui("main_window.ui")
        style_path = self.loader.get_style("style_dark.qss")
        uic.loadUi(ui_path, self)
        self.factory = DialogFactory(style_path=style_path)

        # ✅ Redirect stdout/stderr to lineResults
        self.console = StdoutConsole(self.lineResults)

        # Connect buttons
        self.pushButtonName.clicked.connect(lambda: self.open_dialog("name"))
        self.pushButtonSettings.clicked.connect(lambda: self.open_dialog("settings"))
        self.pushButtonTable.clicked.connect(self.open_table_dialog)
        self.pushButtonCombo.clicked.connect(self.open_combo_dialog)
        self.pushButtonValidated.clicked.connect(self.open_validated_dialog)

    def open_dialog(self, key):
        dialog = self.factory.create_dialog(key, parent=self)
        result = dialog()
        self.lineResults.appendPlainText(str(result) if result else "Dialog canceled.")

    def open_table_dialog(self):
        columns = ["ICAO", "RWY Length", "HI", "LO"]
        dialog = self.factory.create_dialog("table", parent=self, params={"columns": columns})
        result = dialog()
        if result:
            self.lineResults.appendPlainText(str(result) if result else "Table dialog not accepted.")


    def open_combo_dialog(self):
        values = ["Option A", "Option B", "Option C"]
        dialog = self.factory.create_dialog("combo", parent=self, params={"values": values})
        result = dialog()
        if result:
            self.lineResults.appendPlainText(str(f"Selected: {result['choice']}") if result else None)

    def open_validated_dialog(self):
        targets = [
            {"name": "lineEdit1", "rules": [{"type": "length", "value": 4}]},
            {"name": "lineEdit2", "rules": [{"type": "regex", "pattern": r"^[A-Z]{3}$"}]},
            {"name": "lineEdit3", "rules": [{"type": "range", "min": 10, "max": 99}]}
        ]
        dialog = self.factory.create_dialog("validated", parent=self, params={"targets": targets})
        result = dialog()
        if result:
            self.lineResults.appendPlainText(str(result) if result else None)

    def closeEvent(self, event):
        self.console.restore()  # ✅ Restore original streams
        super().closeEvent(event)

def validate_license():
    try:
        license_mgr = LicenseManager()
        if not license_mgr.check():
            print("❌ License expired, deleted, or invalid for this machine/key.")
            sys.exit(1)
    except Exception as e:
        print(f"❌ License check failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    validate_license()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())