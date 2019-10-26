# python3 setup.py sdist bdist_wheel
# python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# python3 -m pip install -i https://test.pypi.org/simple/ justpy-test==5.0.0
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="justpy-test",
    python_requires=">=3.6",
    version="5.0.0",
    license="Apache",
    author="Eliezer Mintz",
    author_email="eli.mintz@gmail.com",
    description="An object oriented high-level Python Web Framework that requires no front-end programming",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'starlette',
        'addict',
    ],
    # need to add package_data
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
