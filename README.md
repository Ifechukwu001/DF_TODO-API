# TODO API

## OpenAPI/Swagger Documentation

The Swagger documentation for the application is hosted on [Render]() along with the application server.

## Setup

- Clone the repository

  ```bash
  git clone https://github.com/Ifechukwu001/DF_TODO-API.git df_todo_api
  cd df_todo_api
  ```

- Setup a new environment with UV. \
  [Click to Install UV](https://docs.astral.sh/uv/getting-started/installation/)

  ```bash
  uv init
  ```

- Synchronize the package requirements

  ```bash
  uv sync
  ```

- Run migrations

  ```bash
  uv run src/manage.py migrate
  ```

- Run the server locally on port 8000

  ```bash
  uv run src/manage.py runserver
  ```
