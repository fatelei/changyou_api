import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="changyou",
    version="1.0.5",
    author="fatelei",
    author_email="fatelei@gmail.com",
    description="changyou api client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fatelei/changyou_api",
    project_urls={
        "Bug Tracker": "https://github.com/fatelei/changyou_api/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    package_data={
        "": ["*.html"]
    }
)
