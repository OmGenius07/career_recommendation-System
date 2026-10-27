# AI Career Path Recommender (Python Only)

## Setup

1. Clone repo
2. Install backend deps:
pip install -r backend/requirements.txt
3. Install frontend deps:
pip install -r frontend/requirements.txt
4. Start backend:
uvicorn backend.main:app --reload
5. Start frontend:
streamlit run frontend/app.py

Make sure to set `OPENAI_API_KEY` in your environment variables.
