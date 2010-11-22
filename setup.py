import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = ['pyramid', "pyramid_beaker"]

setup(name='tictactroll',
      version='0.3',
      description='tictactroll',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Bertrand Janin',
      author_email='tamentis@neopulsar.org',
      url='',
      keywords='web wsgi bfg pyramid pylons tic-tac-toe reddit',
      packages=find_packages(),
      scripts=[
        "scripts/get.py",
        "scripts/load.py",
      ],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="tictactroll",
      entry_points = """\
      [paste.app_factory]
      app = tictactroll:app
      """,
      paster_plugins=['pyramid'],
      )

