# ResolveAI

An AI powered customer support platform. The current milestone is a ticket-management API built with FastAPI and PostgreSQL.

## Current Features

- Create, list, retrieve, update, and delete tickets
- Validate ticket input and status values
- Return appropriate errors for invalid or missing tickets

## Tech Stack

- Python
- FastAPI
- PostgreSQL

## Run Locally

1. Create and activate a Python virtual environment.
2. Install dependencies:
   `python -m pip install fastapi "uvicorn[standard]" "psycopg[binary]" python-dotenv`
3. Create a `.env` file with your PostgreSQL connection settings.
4. Start the API:
   `python -m uvicorn main:app --reload`
5. Open `http://127.0.0.1:8000/docs`.

## Project Status

Backend ticket CRUD is implemented. Frontend and AI features are planned.