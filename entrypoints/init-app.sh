#!/bin/bash
echo "Executando entrypoint."
python -m debugpy --listen 0.0.0.0:5678 -m uvicorn src.main:app --reload --workers 3 --host 0.0.0.0 --port 8000
