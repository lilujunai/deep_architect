#!/bin/bash

for ((i=1;i<=$1;i++)); do
    python tutorials/full_search/search.py -c file -n $1&
done