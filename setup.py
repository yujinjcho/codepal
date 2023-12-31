from setuptools import setup, find_packages

setup(
    name="codepal",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "tiktoken",
        "openai",
    ],
    entry_points={
        "console_scripts": [
            "codepal = codepal.main:main",
        ],
    },
)

