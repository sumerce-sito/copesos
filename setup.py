from setuptools import setup, find_packages

setup(
    name="copesos",
    version="0.2.0",
    author="sumercesito",
    author_email="",
    description="Utilidades para proyectos colombianos",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sumerce-sito/copesos",
    packages=find_packages(),
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Spanish",
        "Topic :: Office/Business :: Financial",
        "Intended Audience :: Developers",
    ],
    keywords="colombia pesos nómina festivos NIT cédula tributario",
)
