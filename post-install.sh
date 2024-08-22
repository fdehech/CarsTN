#!/bin/bash
set -e

# Update package list and install missing libraries
apt-get update
apt-get install -y \
    libgstreamer-plugins-base1.0-0 \
    libgstreamer1.0-0 \
    libenchant2 \
    libsecret-1-0 \
    libgles2-mesa \
    libgtk-3-0
