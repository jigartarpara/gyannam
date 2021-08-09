from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in gyannam/__init__.py
from gyannam import __version__ as version

setup(
	name='gyannam',
	version=version,
	description='Educational',
	author='Jigar Tarpara',
	author_email='team@khatavahi.in',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
