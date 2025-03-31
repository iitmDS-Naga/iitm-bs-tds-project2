Step 1

using pydanticai and fast api create basic agent that can provide a json response to a api call made

## Instructions to run the application

1. Set up environment variables:
   - Create a `.env` file in the project root
   - Add your OpenAI API key: `OPENAI_API_KEY=your-api-key-here`

2.  Install dependencies: `uv pip install --requirements pyproject.toml`
3.  Run the application: `uvicorn src.main:app --reload`
4.  Access the API endpoint at: `http://localhost:6000/`

## Docker Instructions

1. Set up environment variables as described above

2. Build the Docker image:
   ```bash
   docker build -t iitm-bs-tds-project2 .
   ```

3. Run the Docker container:
   ```bash
   docker run -p 6000:6000 iitm-bs-tds-project2
   ```

4. Access the API endpoint at: `http://localhost:6000/`

## Docker Compose Instructions

1. Start the application:
   ```bash
   docker compose up --build
   ```

2. Stop the application:
   ```bash
   docker compose down
   ```

3. Access the API endpoint at: `http://localhost:6000/`