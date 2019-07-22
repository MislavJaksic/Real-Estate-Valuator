from setuptools import setup, find_packages


with open("README.md") as f:
  readme = f.read()

setup(
  name="Real Estate Valuator",
  version="0.1.0",
  description="Evaluate or find real estate",
  long_description=readme,
  
  author="Mislav Jaksic",
  author_email="jaksicmislav@gmail.com",
  url="",
  
  packages=find_packages(exclude=("tests", "docs")),
  
  entry_points={"console_scripts" : ["project_name = src.Valuator.runner:Run"]} 
)

