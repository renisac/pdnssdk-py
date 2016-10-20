#!/bin/bash

python setup.py clean

python setup.py register -r pypitest
python setup.py sdist upload -r pypitest
