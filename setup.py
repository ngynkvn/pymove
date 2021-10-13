from setuptools import setup, find_packages


with open("requirements.txt") as f:
    requirements = f.readlines()

setup(
    name="PyMove",
    version="0.1dev",
    author="Kevin Nguyen",
    author_email="ngynkvn@gmail.com",
    license="MIT",
    packages=find_packages(),
    entry_points={"console_scripts": ["pymove = pymove.pymove:main"]},
    keywords="mv util cli python",
    install_requires=requirements,
    description="A CLI tool for organizing file directories.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
)