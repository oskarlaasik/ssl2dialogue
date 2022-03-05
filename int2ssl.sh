#!/bin/bash

for FILE in "$1"/*; do
int2ssl -1 $FILE; done
