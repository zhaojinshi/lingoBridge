import sys
import winreg
from pathlib import Path

from core.config import APP_DIR


APP_NAME = "lingoBridge"
RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"


def _startup_command():
    if getattr(sys, "frozen", False):
        return f'"{sys.executable}" --no-admin'

    python_exe = Path(sys.executable)
    pythonw_exe = python_exe.with_name("pythonw.exe")
    launcher = pythonw_exe if pythonw_exe.exists() else python_exe
    return f'"{launcher}" "{APP_DIR / "main.py"}" --no-admin'


def is_autostart_enabled():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY) as key:
            winreg.QueryValueEx(key, APP_NAME)
        return True
    except FileNotFoundError:
        return False


def set_autostart_enabled(enabled):
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, RUN_KEY) as key:
        if enabled:
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, _startup_command())
        else:
            try:
                winreg.DeleteValue(key, APP_NAME)
            except FileNotFoundError:
                pass
