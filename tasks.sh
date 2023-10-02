#!/bin/bash

# Run the cropper script
python3 cropper.py

# Copy all files from ./output to ./backup/cropped
cp ./output/* ./backup/cropped/

# Run the scene_splitter script
python3 scene_splitter.py

# Run the video_maker script
python3 videomaker.py

# Shut down the computer
# Note: The exact command to shut down the computer might vary depending on your OS.
# The following command works for most Linux distributions:
shutdown -h now
