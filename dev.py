#!/usr/bin/env python
"""
One-command local development server.

Usage:
    python dev.py          — start dev server on http://localhost:8000
    python dev.py setup    — first-time setup (install deps, migrate, load data)

This script auto-creates a .venv and installs requirements so you never
need to manually activate a virtual environment.
"""

import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
VENV_DIR = BASE_DIR / ".venv"
REQUIREMENTS = BASE_DIR / "requirements.txt"

if sys.platform == "win32":
    VENV_PYTHON = VENV_DIR / "Scripts" / "python.exe"
    VENV_PIP = VENV_DIR / "Scripts" / "pip.exe"
else:
    VENV_PYTHON = VENV_DIR / "bin" / "python"
    VENV_PIP = VENV_DIR / "bin" / "pip"


def ensure_venv() -> None:
    """Create venv and install requirements if missing."""
    if VENV_PYTHON.exists():
        return

    print("Creating virtual environment...")
    subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)])
    print("Installing dependencies...")
    subprocess.check_call([str(VENV_PIP), "install", "-r", str(REQUIREMENTS)])
    print()


def manage(*args: str) -> int:
    """Run a Django management command using the venv Python."""
    return subprocess.call(
        [str(VENV_PYTHON), str(BASE_DIR / "manage.py"), *args],
        env={**os.environ, "DJANGO_SETTINGS_MODULE": "config.settings"},
    )


def main() -> None:
    ensure_venv()

    command = sys.argv[1] if len(sys.argv) > 1 else "serve"

    if command == "setup":
        print("\n=== Installing / updating dependencies ===")
        subprocess.check_call(
            [str(VENV_PIP), "install", "-r", str(REQUIREMENTS), "-q"]
        )
        print("=== Running migrations ===")
        manage("migrate")
        print("\n=== Loading testimonials ===")
        manage("load_testimonials")
        print("\n=== Creating superuser ===")
        print("(Skip with Ctrl+C if you already have one)\n")
        try:
            manage("createsuperuser")
        except KeyboardInterrupt:
            print("\nSkipped.")
        print("\n=== Done! Run 'python dev.py' to start the server ===\n")

    elif command == "serve":
        manage("migrate", "--run-syncdb")
        print("\n  Dev server starting at http://localhost:8000\n")
        manage("runserver", "0.0.0.0:8000")

    else:
        # Pass through any manage.py command: python dev.py shell, etc.
        manage(command, *sys.argv[2:])


if __name__ == "__main__":
    main()
