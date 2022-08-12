from os import environ

import setuptools

if __name__ == "__main__":
    setuptools.setup(
        scripts=["scripts/pt-web-vnc"],
        version=environ.get("PACKAGE_VERSION", "0.0.1").replace('"', ""),
    )
