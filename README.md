# Job Sheet Backend

The client has requested a backend service for managing job sheets, including user authentication and job sheet operations. The backend should be built using FastAPI and MongoDB.

## Requirements

- Implement user authentication with JWT tokens.
- Create endpoints for user registration, login, and logout.
- Develop CRUD operations for job sheets.
    - A job sheet should include fields like job ID, customer name, job description, status, and timestamps.
- Ensure proper error handling and validation.
- Write unit tests for the main functionalities.

## Setup Instructions

1. Clone the repository.
2. Run `chmod +x scripts/*.sh` to make the installation script executable.
3. Run `python3 -m venv venv` to create a virtual environment.
4. Activate the virtual environment:
    - On Windows: `.\venv\Scripts\activate`
    - On Unix or MacOS: `source venv/bin/activate`
5. Execute `./scripts/install.sh` to set up the environment and install dependencies.
    - `sh scripts/install.dev.sh` for development setup.
6. Create a `.env` file in the root directory and configure the necessary environment variables (refer to `.env.example`).
7. Start the FastAPI server using `python src/main.py`.

## API Documentation
Once the server is running, access the API documentation at [localhost:8000/docs](http://localhost:8000/docs) for the interactive Swagger UI or [localhost:8000/redoc](http://localhost:8000/redoc) for ReDoc.

## Testing
To run the unit tests, execute `pytest` in the terminal.