
from setuptools import setup

setup(
    name = 'stones',
    version = '0.1.1',
    author = 'Cristi Constantin',
    author_email = 'cristi.constantin@live.com',
    description = 'Persistent key-value containers, compatible with Python dict',
    keywords = 'persistent dict',
    url = 'https://github.com/croqaz/Stones',
    license = 'MIT',
    packages = ['stones', 'tests'],
    include_package_data = True,
    zip_safe = True,
    python_requires = '>= 3.6',
    extras_require = {
        'dev': ['flake8', 'codecov'],
        'test': ['pytest', 'pytest-cov'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Database',
    ]
)
