#!/bin/bash
find . -name '*.egg-info' -type d -exec rm -rf {} \; -exec echo "Removed: " {} \; 2> /dev/null
find . -name '.eggs' -type d -exec rm -rf {} \; -exec echo "Removed: " {} \; 2> /dev/null
find . -name '.cache' -type d -exec rm -rf {} \; -exec echo "Removed: " {} \; 2> /dev/null
find . -name 'build' -type d -exec rm -rf {} \; -exec echo "Removed: " {} \; 2> /dev/null
find . -name 'dist' -type d -exec rm -rf {} \; -exec echo "Removed: " {} \; 2> /dev/null
find . -name '__pycache__' -type d -exec rm -rf {} \; -exec echo "Removed: " {} \; 2> /dev/null
find . -name '*.pyc' -type f -exec rm -rf {} \; -exec echo "Removed: " {} \; 2> /dev/null
