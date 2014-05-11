from setuptools import setup, find_packages


setup(
    name="simple-crawler",
    version="0.1",
    url="https://github.com/shonenada/crawler",
    author="shonenada",
    author_email="shonenada@gmail.com",
    description="Simple crawler",
    zip_safe=True,
    platforms="any",
    packages=find_packages(),
    install_requires=["requests==2.2.1"],
)
