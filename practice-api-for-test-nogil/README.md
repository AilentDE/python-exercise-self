# Practice API for Testing NoGIL

This project aims to test the performance differences of FastAPI running on Python 3.12 and Python 3.13-nogil.

> <span style="color: orange">[PENDING]</span> The project is currently on hold because FastAPI does not yet support Python 3.13.<br/>
> It will be resumed once FastAPI adds support for Python 3.13.

## Dependencies

- FastAPI
- Redis
- Postgres

## Project Structure

- `main.py`: Entry point for the FastAPI application, including middleware and route setup.
- `middlewares/timer.py`: Timer middleware to log the processing time of each request.
- `utils/create_fake_user.py`: Utility functions for creating fake users.
- `routes/users.py`: API routes related to user operations.
- `routes/users_fake.py`: API routes for creating fake users.
- `config/db_postgres.py`: Configuration and initialization for the PostgreSQL database.
- `config/db_redis.py`: Configuration for the Redis database.
- `models/user.py`: SQLAlchemy model for users.
- `schemas/user.py`: Pydantic schema for users.

## Usage

1. (option) Up the database container services.

   ```bash
   docker-compose up -d
   ```

2. Create and activate a virtual environment:
   ```bash
   python3.12 -m venv venv312
   source venv312/bin/activate
   ```
3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Running the FastAPI Application

   ```bash
   uvicorn main:app --reload
   ```

5. The application will run at `http://127.0.0.1:8000`.

   Use [Swagger UI](http://127.0.0.1:8000/docs) for testing.
