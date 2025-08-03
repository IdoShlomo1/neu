# Neu Dockerized Testing Environment

## Project Structure

```text
neu/
├── README.md
├── requirements.txt
├── automation/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── rest_client.py
│   │   ├── strings_api.py
│   ├── plugin/
│   │   ├── docker_wrapper.py
│   │   ├── pytest_docker_plugin.py
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_string_api.py
├── rest_app/
│   ├── app.py
│   └── Dockerfile
```

- `rest_app/`: Flask app and Dockerfile
- `automation/plugin/pytest_docker_plugin.py`: Pytest plugin for Docker management
- `automation/plugin/docker_wrapper.py`: Docker control utilities
- `automation/api/`: API client and helpers
- `automation/tests/`: Test suite

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/IdoShlomo1/neu.git
   cd neu
   ```

2. **Install Python dependencies:**

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

   Ensure you have [Docker](https://www.docker.com/get-started) installed and running.

## Execution

### 1. Build the Docker Image

   ```sh
   cd rest_app
   ```

   ```sh
   docker build -t flask-reverse-api .
   ```

### 2. Run the Container (Manual)

   ```sh
   docker run -p 8000:8000 flask-reverse-api
   ```

### 3. Run Tests with Docker Management

The custom pytest plugin will automatically start/stop the container if you use the `--with-docker` flag:

```sh
neu $ pytest automation/tests/ -s --with-docker
```

#### Additional Options

- `--container-name`: Set the Docker image/container name (default: `flask-reverse-api`)
- `--container-scope`: Set to `session` (default) or `test` for container lifecycle per test
- `--request-debug`: Enable detailed request debugging output for API calls

Example:

```sh
pytest automation/tests/  --with-docker --container-name=flask-reverse-api --container-scope=test
```

## Server Endpoints

The Flask API provides the following endpoints:

- `GET /reverse?text=your+text+here`
  - Reverses the order of words in the `text` query parameter and caches the result.
  - **Example:**

    ```sh
    curl 'http://localhost:8000/reverse?text=hello+world'
    # {"result": "world hello"}
    ```

- `GET /restore`
  - Returns the most recently cached result from `/reverse`.
  - **Example:**

    ```sh
    curl 'http://localhost:8000/restore'
    # {"result": "hello world"}
    ```

## Automation Plugin & Usage

The automation part is handled by a custom pytest plugin:

- Located at `automation/plugin/pytest_docker_plugin.py` and `automation/plugin/docker_wrapper.py`.
- When running tests with `--with-docker`, the plugin will:
  - Start the Docker container before the test session or each test (configurable with `--container-scope`)
  - Stop the container after the session or each test

This ensures a clean and isolated environment for your integration tests.

### Best Practices

- Use `--container-scope=session` for faster test runs when tests can share a container
- Use `--container-scope=test` for full isolation between tests
- Set logging to DEBUG for more output: `pytest --log-cli-level=DEBUG`
- Ensure your Docker image is built before running tests
