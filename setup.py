from setuptools import setup, find_packages
with open("README.md", "r",encoding ="utf-8") as fh:
    long_description=fh.read()

author_name = "RAGUL V"
src_repo = "src"
list_of_requirements = ['streamlit']

setup(
    name=src_repo,
    version="0.0.1",
    author=author_name,
    author_email="sachinragul50@gmail.com",
    description="A movie recommendation system using collaborative filtering",
    long_description=long_description,
    long_description_content_type="text/markdown ",
    url='https://github.com/RAGULcse25/Data-Science.git',
    packages=[src_repo],
    python_requires=">=3.7",
    install_requires =list_of_requirements    
)