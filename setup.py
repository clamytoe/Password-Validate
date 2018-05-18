from setuptools import setup, find_packages

import passwd_validate

VERSION = passwd_validate.__version__
AUTHOR = passwd_validate.__author__
EMAIL = passwd_validate.__email__

setup(
    name="Password Validate",
    version=VERSION,
    packages=find_packages(),
    url="https://github.com/clamytoe/Password-Validate",
    license="MIT",
    author=AUTHOR,
    author_email=EMAIL,
    description="Small little utility to assist you with validating passwords",
    include_package_data=True,
    install_requirements=[
        'pytest',
    ],
    entry_points="""
        [console_scripts]
        passwd_validate=passwd_validate.app:main
    """,
)
