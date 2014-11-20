#!/bin/bash

# get the project name (current directory) and the john directory
name=${PWD##*/};
dir="$( dirname $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd ))";

echo $name
echo $dir

# set up directories
mkdir -p docs		# documentation (should be online for users, comments for devs)
mkdir -p source		# multi-lang source; subdirectories should be by functionality
mkdir -p data		# generated data
mkdir -p test		# (should be subdirectories)
mkdir -p install	# dependencies? build process? run tests...
mkdir -p dev		# things for during development, excludable for live version
mkdir -p bin		# binaries? other 'compiled' (derived) files?
# external (third party) modules and libraries
# many static files belong in a functional module (e.g. appname.static)
# settings for the project (source?)
# tests, as said, should be in subdirecties

# readme
# setup (/make)

# virtualenv -> .env

# 'input' (fundamental) data in a separate, read-only directory (under code version control if appropriate)
# output is derived should go in 'data', not in version control; final output should be copied out and stored

# git init

## science:
# literature?
# report
