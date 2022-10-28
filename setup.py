from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    """
    This functino returns a list of requirements
    """
    requirement_list:List[str] = []
    return requirement_list

setup(

    name="sensor",
    version="0.0.1",
    author="Rahul",
    author_email="ragulr404@gmail.com",
    package = find_packages(),
    install_requires=get_requirements(),#["pymongo==4.2.0"],
)