from setuptools import setup, find_packages

setup(
    name='pyspark-venv',
    version='0.1.0-SNAPSHOT',
    description='Virtual environment helper for Pyspark',
    url='https://github.com/alemagnani/PysparkEnv.git',
    author='Alessandro Magnani',
    author_email='AMagnani@walmartlabs.com',
    license='Apache License',

    packages=find_packages(),

    include_package_data=True,

    zip_safe=False,
)

