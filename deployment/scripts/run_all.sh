#!/bin/bash

# Start Streamlit app in background
streamlit run streamlit_app.py &

# Start FastAPI
uvicorn api_server:app --host 0.0.0.0 --port 8000
