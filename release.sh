#!/bin/bash

python setup.py clean

python setup.py register -r pypi
python setup.py sdist upload -r pypi
