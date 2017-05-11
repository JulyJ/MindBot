from os import path
from sys import exit
from uuid import uuid1

from pip.req import parse_requirements
from setuptools import setup, find_packages
from setuptools.command.test import test


basedir = path.dirname(__file__)


def get_version():
    with open(path.join(basedir, 'mindbot/__init__.py')) as f:
        variables = {}
        exec(f.read(), variables)
        return '.'.join(str(x) for x in variables['VERSION'])


def get_requirements(filename):
    requirements_path = path.join(basedir, filename)
    requirements = parse_requirements(requirements_path, session=uuid1())
    return [str(r.req) for r in requirements]


setup(
    name='MindBot',
    version=get_version(),
    url='https://github.com/JulyJ/MindBot',
    license='MIT',
    author='Julia Koveshnikova',
    author_email='julia.koveshnikova@gmail.com',
    description='Mind backup telegram bot',
    long_description='Mind backup telegram bot',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
    tests_require=get_requirements('requirements-dev.txt'),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    entry_points={
        'console_scripts': [
            'mindbot = mindbot.bot:run',
        ],
    },
    classifiers=[
        # As from https://pypi.python.org/pypi?:action=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Communications :: Chat',
    ],
)
