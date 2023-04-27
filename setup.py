from setuptools import setup


version = "1.3.4"


with open("./ldapauthenticator/__init__.py", "a") as f:
    f.write("\n__version__ = '{}'\n".format(version))


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
