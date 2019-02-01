from setuptools import setup
from setuptools import find_packages

setup(
    name="ai-forge",
    version="0.1.0",
    author="raynardj",
    author_email="raynard@rasenn.com",
    description="Ray's tool for managing machine learning",
    packages = find_packages(),
    py_modules=['forgebox','forge',],
)