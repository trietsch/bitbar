#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR/../"

MODULE_NAME="$1"

# Get path to Python as defined in the config file of this module
PYTHON_BIN="$(awk -F '=' '{if (! ($0 ~ /^;/) && $0 ~ /python_binary/) print $2}' "$DIR/../../config/$MODULE_NAME-config.ini" | xargs )"

"$PYTHON_BIN" -m "python.$MODULE_NAME"