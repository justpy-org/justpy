import setuptools

def get_long_description():
    with open("README.md", encoding="utf8") as f:
        return f.read()

setuptools.setup(
    name="justpy",
    python_requires=">=3.6",
    version="0.1.3",
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
        'addict>=2.2.1', 'jinja2>=2.10.1', 'demjson>=2.2.4', 'httpx>=0.11.0', 'aiofiles'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: User Interfaces",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License"
    ]
)

