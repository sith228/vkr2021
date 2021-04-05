#!/bin/bash
BASEDIR=$(dirname "$0")
wget "35.239.156.163:8080/download/test_data.zip"
unzip -q test_data.zip -d "$BASEDIR"
