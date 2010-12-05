#!/bin/ksh
#
# This assumes the environment is setup properly, it will generate
# a production-ready EGG for deployement.
#

. virtualenv/bin/activate

python setup.py egg_info -RDb "" sdist bdist_egg

