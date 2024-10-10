from setuptools import setup, find_packages

setup(
    name='checkInvalidURLs',
    version='0.1',
    py_modules=['checkInvalidURLs'],
    install_requires=[
        'requests',
        'pandas',
        'openpyxl',
    ],
    entry_points={
        'console_scripts': [
            'checkInvalidURL=checkInvalidURLs:main',
        ],
    },
)
