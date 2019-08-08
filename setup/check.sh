#!/bin/bash
echo "------------------------------------"
echo "Running $BASH_SOURCE..."
echo "------------------------------------"
echo "Moving to toplevel of repo..."
cd "$(git rev-parse --show-toplevel)"
echo "------------------------------------"
echo "Creating source archive and a wheel for package..."
pipenv run twine check dist/*
echo "------------------------------------"
echo "Done"
