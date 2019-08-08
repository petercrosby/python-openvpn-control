#!/bin/bash
echo "------------------------------------"
echo "Running $BASH_SOURCE..."
echo "------------------------------------"
echo "Moving to toplevel of repo..."
cd "$(git rev-parse --show-toplevel)"
echo "------------------------------------"
echo "Running setup.py test with coverage..."
pipenv run coverage run setup.py test
pipenv run coverage report
pipenv run coverage html
pipenv run codecov
echo "------------------------------------"
echo "Done"
