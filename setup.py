"""Setup configuration for dinnovos-agent-cli."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dinnovos-agent-cli",
    version="1.0.1",
    author="Dinnovos",
    author_email="info.dinnovos@gmail.com",
    description="CLI tool to create new AI agent projects based on LangGraph and FastAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dinnovos/agent-base-project",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": ["cookiecutter-template/**/*"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.11",
    install_requires=[
        "cookiecutter>=2.1.0",
    ],
    entry_points={
        "console_scripts": [
            "dinnovos-create-agent=dinnovos_cli.main:main",
        ],
    },
)
