#!/bin/bash

# This is the path to your Python executable. Adjust it if needed.
PYTHON_EXEC=python

# This is the path to your main.py file. Adjust it if needed.
MAIN_PY_FILE=main.py

# Execute the main.py file with the specified Python interpreter
$PYTHON_EXEC $MAIN_PY_FILE

# Check the exit status of the Python script
if [ $? -eq 0 ]; then
  echo "Script executed successfully"
else
  echo "Script failed with exit code $?"
fi