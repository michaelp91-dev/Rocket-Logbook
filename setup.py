"""
Rocket Logbook - Setup Script

This is a minimal setup.py file that works with pyproject.toml.
Most of the configuration is in pyproject.toml.
"""

from setuptools import setup, find_packages

# This setup script is only needed for backwards compatibility.
# Modern Python packaging uses pyproject.toml for configuration.
if __name__ == "__main__":
    setup(
        packages=find_packages(),
        # All other configuration is in pyproject.toml
    )