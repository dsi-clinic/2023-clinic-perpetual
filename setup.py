from setuptools import find_packages, setup

setup(
    name="2023-clinic-Perpetual",
    version="0.1.0",
    packages=find_packages(
        include=[
            "utils",
            "utils.*",
        ]
    ),
    install_requires=[],
)
