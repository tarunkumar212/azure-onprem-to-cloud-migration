#!/bin/bash
# Startup script for Azure App Service
# Used during migration from VM to App Service
cd /home/site/wwwroot
gunicorn --workers 2 --bind 0.0.0.0:8000 --timeout 120 app:app
