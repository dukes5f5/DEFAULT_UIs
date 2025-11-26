myApp — Modular PyQt5 Dialog Framework
A scalable, teachable PyQt5 application framework with:
- Centralized resource loading (dev + frozen)
- Machine-bound license enforcement (7-day timeout)
- Dialog registry with validation logic
- Global stylesheet support
- PyInstaller-ready for distribution
Project Structure
myApp/
├── main.py
├── main.spec
├── dialog_factory.py
├── dialogs_registry.py
├── license_manager.py
├── resource_loader.py
├── license.dat
├── resources/
│   ├── ui/
│   ├── styles/
│   ├── images/
│   └── sounds/
└── README.md
Running the App
Development:
python main.py
Freezing with PyInstaller:
Windows:
pyinstaller main.spec
macOS/Linux:
pyinstaller main.spec
This will generate a dist/myApp/ folder containing myApp.exe (or myApp on macOS/Linux).
License Behavior
- On first run, license.dat is created at the project root.
- Bound to machine fingerprint (system info).
- Expires after 7 days.
- If expired or copied to another machine, the app will not launch.
Dialog Registration
To add a new dialog:
- Create a .ui file in resources/ui/
- Define init_ and get_ functions in dialogs_registry.py
- Register it in REGISTRY:
"mydialog": (
loader.get_ui("MyDialog.ui"),
get_mydialog_result,
init_mydialog
)
Styling
Place .qss files in resources/styles/. To apply globally:
DialogFactory(style_path="style_dark.qss")
Resource Access
Use ResourceLoader:
from resource_loader import ResourceLoader
loader = ResourceLoader()
ui_path = loader.get_ui("main_window.ui")
style_path = loader.get_style("style_dark.qss")
Extending the Loader
Add new categories:
def get_font(self, filename: str) -> str:
return self.get("fonts", filename)
def get_data(self, filename: str) -> str:
return self.get("data", filename)
Best Practices
- Never hardcode paths — always use ResourceLoader
- Use require() for mandatory assets
- Keep dialogs modular and registered in dialogs_registry.py
- Use DialogFactory to apply global styles and instantiate dialogs
Collaborator Onboarding
- Clone the repo
- Run python main.py
- Add your .ui files to resources/ui/
- Register new dialogs in dialogs_registry.py
- Freeze with pyinstaller if needed
Questions?
Open an issue or contact the maintainer: dukes
