#!/bin/bash
BASEDIR=$(dirname "$0")
# Download
wget "34.67.40.164:8080/download/test_data.zip" # Own test images
wget "34.67.40.164:8080/download/coco_bus.zip"  # Bus images from COCO dataset

# Extract
unzip -q test_data.zip -d "$BASEDIR"
unzip -q coco_bus.zip -d "$BASEDIR/coco_bus"
