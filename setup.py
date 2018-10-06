from setuptools import find_packages, setup

__author__ = "spapanik"
__version__ = "0.1.3"
__license__ = "MIT"

PKG_NAME = "pyrencode"
PKG_URL = f"https://github.com/{__author__}/{PKG_NAME}"


def contents(filename):
    with open(filename) as f:
        return f.read()


setup(
    name=PKG_NAME,
    packages=find_packages("src"),
    package_dir={"": "src"},
    version=__version__,
    author=__author__,
    author_email="spapanik21@gmail.com",
    license=__license__,
    description="A pure python rencoder",
    long_description=contents("readme.md"),
    url=PKG_URL,
    download_url=f"{PKG_URL}/tarball/{__version__}",
    python_requires=">=3.6",
    tests_require=["pytest>=3.0.0,<4.0.0"],
    keywords=["deluge", "rencode", "encode", "decode"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
