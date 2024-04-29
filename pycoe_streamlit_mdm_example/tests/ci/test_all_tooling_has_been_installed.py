import importlib.util
import pytest

def check_package(package_name):
    spec = importlib.util.find_spec(package_name)
    assert spec is not None, f"Package '{package_name}' is not installed."

@pytest.mark.parametrize("package", [
    "streamlit",
    "pandas",
    "safety",
    "faker",
    "numpy",
    "recordlinkage",
    "timedelta",
    "pytest",
    "selenium",
])
def test_packages_installed(package):
    check_package(package)
