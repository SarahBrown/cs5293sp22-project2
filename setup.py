from setuptools import setup, find_packages

setup(
	name='project2',
	version='1.1',
	author='Sarah Brown',
	authour_email='srb@ou.edu',
	packages=find_packages(exclude=('tests', 'docs')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']	
)