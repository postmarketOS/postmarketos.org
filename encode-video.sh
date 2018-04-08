#!/bin/sh
INPUT=$1
OUTPUT=$(echo $INPUT | cut -f 1 -d '.')

# MP4 first pass: analyze
ffmpeg -y -i $INPUT -c:v libx264 -preset slow -b:v 2M -pass 1 -f mp4 /dev/null

# Encode final MP4
ffmpeg -y -i $INPUT -c:v libx264 -preset slow -b:v 2M -pass 2 -f mp4 $OUTPUT-x264.mp4

# VPX first pass: analyze
ffmpeg -y -i $INPUT -c:v libvpx-vp9 -b:v 2M -pass 1 -c:a libopus -f webm /dev/null

# Encode final VPX
ffmpeg -i $INPUT -c:v libvpx-vp9 -b:v 2M -pass 2 -c:a libopus -f webm $OUTPUT-vpx.webm
