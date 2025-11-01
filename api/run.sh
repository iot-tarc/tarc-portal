#!/bin/bash
# Script para rodar a aplicação FastAPI

uvicorn main:app --reload --host 0.0.0.0 --port 8000

