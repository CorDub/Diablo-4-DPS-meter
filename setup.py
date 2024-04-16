from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='D4DPSM',
      version='0.0.1',
      description="Diablo 4 DPS Meter with text extraction",
      author="Corentin Dubois, Jack Wotton",
      author_email="corentindubois22@gmail.com, jlwotton17@gmail.com",
      install_requires=requirements,
      packages=find_packages())
