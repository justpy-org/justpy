# git clone https://github.com/elimintz/justpy.git [directory]
# python3 setup.py sdist bdist_wheel
# python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# python3 -m twine upload  dist/*

# python3 -m pip install -i https://test.pypi.org/simple/ justpy-test==5.0.5
import setuptools

def get_long_description():
    with open("README.md", encoding="utf8") as f:
        return f.read()

setuptools.setup(
    name="justpy",
    python_requires=">=3.6",
    version="0.0.3",
    license="Apache",
    author="Eliezer Mintz",
    author_email="eli.mintz@gmail.com",
    description="An object oriented high-level Python Web Framework that requires no front-end programming",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/elimintz/justpy",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'starlette>=0.12.0', 'uvicorn>=0.7.1', 'itsdangerous>=1.1.0',
        'addict>=2.2.1', 'jinja2>=2.10.1', 'demjson>=2.2.4', 'requests', 'aiofiles'
    ],
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

