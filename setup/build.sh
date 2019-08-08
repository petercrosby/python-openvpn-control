#!/bin/bash
echo "------------------------------------"
echo "Running $BASH_SOURCE..."
echo "------------------------------------"
echo "Moving to toplevel of repo..."
cd "$(git rev-parse --show-toplevel)"
echo "------------------------------------"
echo "Removing 'dist' and 'build' directories..."
rm -r dist/ build/
echo "------------------------------------"
echo "Creating source archive and a wheel for package..."
pipenv run python setup.py sdist bdist_wheel
echo "------------------------------------"
echo "Done"
