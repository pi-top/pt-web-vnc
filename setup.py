from os import environ

import setuptools

if __name__ == "__main__":
    setuptools.setup(
        scripts=["scripts/pt-web-vnc"],
        version=environ.get("PYTHON_PACKAGE_VERSION", "0.0.1.dev1").replace('"', ""),
    )
