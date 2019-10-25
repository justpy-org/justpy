import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="justpy-test",
    python_requires=">=3.6",
    version="0.0.1",
    license="Apache",
    author="Eliezer Mintz",
    author_email="eli.mintz@gmail.com",
    description="An object oriented high-level Python Web Framework that requires no front-end programming",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License"
    ]
)