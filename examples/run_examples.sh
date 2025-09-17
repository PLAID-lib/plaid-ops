#!/bin/bash

FILES="mesh/*.py"

for file in $FILES
do
    echo "--------------------------------------------------------------------------------------"
    echo "#---# run python $file"
    python "$file"
    if [ $? -ne 0 ]; then
        exit 1
    fi
done