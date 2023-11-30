from setuptools import setup
import os


def read(filename):
    path = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(path, filename), encoding='utf-8') as f:
        return f.read()


setup(
    name='deterrers-api',
    version='0.5',
    description='Python API client for DETERRERS',
    url='https://github.com/virtUOS/deterrers-api',
    author='Lars Kiesow',
    author_email='lkiesow@uos.de',
    license='MIT',
    packages=['deterrersapi'],
    license_files=('LICENSE'),
    include_package_data=True,
    install_requires=read('requirements.txt').split(),
    long_description=read('README.md'),
    long_description_content_type='text/markdown'
    )
