#!/bin/bash
# vm-setup.sh
# Run this script on the Ubuntu VM after deployment
# to install all dependencies and configure the app stack

set -e

echo "=== Updating system packages ==="
sudo apt update && sudo apt upgrade -y

echo "=== Installing Python and dependencies ==="
sudo apt install -y python3 python3-pip python3-venv sqlite3

echo "=== Installing Nginx ==="
sudo apt install -y nginx

echo "=== Creating app directory ==="
mkdir -p /home/azureuser/flaskapp
cd /home/azureuser/flaskapp

echo "=== Creating virtual environment ==="
python3 -m venv venv
source venv/bin/activate
pip install flask gunicorn

echo "=== Setup complete. Copy app.py and configure Nginx manually. ==="
