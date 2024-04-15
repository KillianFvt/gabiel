import subprocess
import sys


def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def is_module_installed(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True
