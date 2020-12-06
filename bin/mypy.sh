#!/usr/bin/env bash

echo 'Running mypy...'
mypy --strict "$@"
echo '...done'
