#!/bin/bash

set -e
testDir="python-sdk-test"
GREEN="\033[0;32m"
NC="\033[0m"

cd /usr/src/app

echo "Installing dependencies for testing..."
pip install -r requirements.txt
pip install tox coverage # For unit tests
/bin/bash package.sh

echo -e "\n\nVobiz SDK setup complete! You can run tests with:"
echo -e "\t$GREEN pytest -q$NC"

# To keep the container running post setup
/bin/bash