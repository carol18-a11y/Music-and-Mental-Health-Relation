#!/usr/bin/env bash
cd "$(dirname "$0")"
python3 web_dashboard/prepare_data.py
python3 web_dashboard/server.py
