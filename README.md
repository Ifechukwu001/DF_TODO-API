# TODO API

## OpenAPI/Swagger Documentation

The Swagger documentation for the application is hosted on [Render](https://df-todo-api.onrender.com/api/docs) along with the application server.

## Setup

- Clone the repository

  ```bash
  git clone https://github.com/Ifechukwu001/DF_TODO-API.git df_todo_api
  cd df_todo_api
  ```

- Setup UV. \
  [Click to Install UV](https://docs.astral.sh/uv/getting-started/installation/)

- Synchronize the package requirements

  ```bash
  uv sync
  ```

- Setup environment variables \
  You can use src/.env file to configure the variables
  ```txt
  SECRET_KEY=application_secret_key
  DEBUG=True
  ALLOWED_HOSTS=localhost, 127.0.0.1
  ```

- Run migrations

  ```bash
  uv run src/manage.py migrate
  ```

- Run the server locally on port 8000

  ```bash
  uv run src/manage.py runserver
  ```
