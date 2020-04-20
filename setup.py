from setuptools import setup, find_packages

setup(
    name="asdf-sextant",
    version="0.1.0",
    author="Lion Krischer",
    author_email="lion.krischer@gmail.com",
    classifiers=["Programming Language :: Python :: 3"],
    packages=find_packages(),
    package_data={
        "asdf_sextant": [
            "icon.png",
            "resources/index_event.html",
            "resources/index.html",
            "resources/script.js",
            "resources/script_event.js",
        ]
    },
    python_requires=">=3.6, <4",
    install_requires=[
        "pyasdf",
        "pyside2",
        "pyqtgraph>=0.11.0rc0",
        "qdarkstyle",
    ],
    entry_points={
        "console_scripts": ["asdf-sextant=asdf_sextant.main:launch"],
    },
)
