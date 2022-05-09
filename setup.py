# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

packages = find_packages()
# ['ums',
#  'ums.common',
#  'ums.orvi',
#  'ums.sima',
#  'ums.sima.common',
#  'ums.sima.widgets',
#  'ums.sima.widgets.add']

package_data = \
{'': ['*']}

install_requires = [] #\
# ['PySide2>=5.15.2,<6.0.0',
#  'SQLAlchemy>=1.4.23,<2.0.0',
#  'alembic>=1.7.1,<2.0.0',
#  'keyring>=23.2.1,<24.0.0',
#  'matplotlib>=3.4.3,<4.0.0',
#  'numpy>=1.21.2,<2.0.0',
#  'pandas>=1.3.3,<2.0.0',
#  'psycopg2>=2.9.1,<3.0.0']

entry_points = \
{'console_scripts': ['mavr-orvi = ums.orvi:run', 'mavr-sima = ums.sima:run']}

setup_kwargs = {
    'name': 'ums',
    'version': '0.0.1',
    'description': 'Will be...',
    'long_description': open('README.md', 'r').read(),
    'author': 'Anatoly Beskakotov',
    'author_email': 'beskakotov.as@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
