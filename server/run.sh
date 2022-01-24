#!/usr/bin/env bash

echo "[*] Creating The Virtual Environment.."
python -m venv venv

echo "[*] Activating The Virtual Environment.."
source ./venv/bin/activate

echo "[*] Installing Requirements.."
pip install -r requirements.txt

echo "[*] Launching The Server.."
uvicorn main:app --port 2356 --host 0.0.0.0 --reload