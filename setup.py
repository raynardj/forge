from setuptools import setup
from setuptools import find_packages

# data_files = [('etc', ['etc/forgebox.cfg'])]

setup(
    name="ai-forge",
    version="0.1.0",
    author="raynardj",
    author_email="raynard@rasenn.com",
    description="Ray's tool for managing machine learning",
    packages = find_packages(),
    include_package_data=True,
    py_modules=['forgebox','forge',],
    scripts = ['forge/bin/forge', 'forge/bin/forge_db',],
    # package_data={'forge':['./forge/templates/*','./forge/static/*']},
    install_requires = [
        "flask>=1.0.0",
        "flask_appbuilder==4.3.2",
        "pandas>=0.18.0",
        "tqdm>=4.25.0",
    ],
)
