import setuptools

longDescription = open("README.md").read()

setuptools.setup(
    name = "volt-vtk",
    version = "0.1.0",
    author = "Volt Project",
    description = "Volt Toolkit, a Python library for creating consistent user interfaces in terminals.",
    long_description = longDescription,
    long_description_content_type = "text/markdown",
    url = "https://github.com/voltverse/vtk",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires = ">= 3.5"
)