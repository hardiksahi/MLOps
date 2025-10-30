#!/bin/bash

echo "Running customer facing FastAPI application"

uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level debug