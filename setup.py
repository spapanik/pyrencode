from setuptools import setup

PKG_NAME = "pyrencode"
__version__ = "0.1.0"


def contents(filename):
    with open(filename) as f:
        return f.read()


setup(
    name=PKG_NAME,
    packages=[PKG_NAME, "pyrencode.settings"],
    version=__version__,
    description="A pure python rencoder",
    license="MIT",
    long_description=contents("readme.md"),
    author="Stephanos Papanikolopoulos",
    author_email="spapanik21@gmail.com",
    url="https://github.com/spapanik/{pkg_name}".format(pkg_name=PKG_NAME),
    download_url="https://github.com/spapanik/{pkg_name}/tarball/{ver}".format(
        pkg_name=PKG_NAME, ver=__version__
    ),
    tests_require=["pytest>=3.0.0,<4.0.0"],
    keywords=["deluge", "rencode", "encode", "decode"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
