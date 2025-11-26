# reset_license.py
from license_manager import LicenseManager
from pathlib import Path

# Clean slate
Path("license.dat").unlink(missing_ok=True)
Path("userkey.txt").unlink(missing_ok=True)
Path("resources/ui/license.lock").unlink(missing_ok=True)

# Write new user key
new_key = "A1B2-C3D4-E5F6-G7H8"
Path("userkey.txt").write_text(new_key)

# Generate new license
lm = LicenseManager()
lm._write_license()

print("✅ License reset and reissued.")