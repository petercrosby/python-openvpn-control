#!/bin/bash

echo "------------------------------------"
echo "Running $BASH_SOURCE..."
echo "------------------------------------"
echo "Moving to toplevel of repo..."
cd "$(git rev-parse --show-toplevel)"
echo "------------------------------------"
echo "Uploading distribution to TestPyPi"
pipenv run twine upload --repository test dist/*
echo "------------------------------------"
echo "Done"
