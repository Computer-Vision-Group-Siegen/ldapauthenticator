from setuptools import setup
import os
import re

version = "1.3.4"

VERSION_PATTERN = "__version__\s?=\s?[\"\'][0-9A-z\.\-]+[\"\']"

def set_version():
    file = None
    with open(os.path.join(os.path.dirname(__file__), "ldapauthenticator", "__init__.py"), "r") as f:
        file = f.read()
    with open(os.path.join(os.path.dirname(__file__), "ldapauthenticator", "__init__.py"), "w") as f:
        version_str = "__version__ = '{}'".format(version)
        matches = re.findall(VERSION_PATTERN, file)
        if len(matches) == 0:
            f.write(file + os.linesep + version_str + os.linesep)
        else:
            file = re.sub(VERSION_PATTERN, version_str, file)
            f.write(file)

set_version()

setup(
    name="jupyterhub-ldapauthenticator",
    version=version,
    description="LDAP Authenticator for JupyterHub",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jupyterhub/ldapauthenticator",
    author="Jan Philipp Schneider",
    author_email="jp-schneider@users.noreply.github.com",
    license="3 Clause BSD",
    packages=["ldapauthenticator"],
    install_requires=["jupyterhub", "ldap3", "tornado", "traitlets"],
)
