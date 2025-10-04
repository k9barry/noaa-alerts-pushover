#!/bin/bash
# Remove config.txt directory if it exists and create config.txt file from example
if [ -d "config.txt" ]; then
  echo "Removing directory named config.txt..."
  rm -rf config.txt
fi
if [ ! -f "config.txt" ]; then
  echo "Copying config.txt.example to config.txt..."
  cp config.txt.example config.txt
fi
