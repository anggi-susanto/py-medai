
# Flask Application with Docker and Makefile

This is a Flask application that includes a basic setup for running the project with a virtual environment, Docker, and Flask-Migrate for database migrations.

## Prerequisites

- Python 3.12
- Docker and Docker Compose
- Make (for running the `Makefile` commands)

## Project Setup

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/anggi-susanto/py-medai
cd py-medai
```

### 2. Create a Virtual Environment

Use the `Makefile` to create a virtual environment:

```bash
make install
```

This command will:

- Create a virtual environment in the `venv` directory.
- Install the required Python dependencies listed in `requirements.txt`.

### 3. Running the Application

Run the Flask application with hot reloading:

```bash
make run
```

This command will:

- Set the `FLASK_APP` to `main.py`.
- Set the `FLASK_ENV` to `development` and enable `FLASK_DEBUG` mode.
- Start the Flask application on `http://localhost:5000`.

### 4. Database Migrations

This project uses Flask-Migrate for handling database migrations. The following commands are available:

- **Initialize the Database**: Creates the migrations directory.

    ```bash
    make db-init
    ```

- **Create a New Migration**: Generates a new migration script.

    ```bash
    make db-migrate
    ```

- **Apply Migrations**: Applies the migrations to the database.

    ```bash
    make db-upgrade
    ```

- **Rollback the Last Migration**: Reverts the last migration.

    ```bash
    make db-downgrade
    ```

### 5. Clean Up

To remove the virtual environment:

```bash
make clean
```

### 6. Freeze Dependencies

If you add new dependencies, you can freeze them to `requirements.txt`:

```bash
make freeze
```

## Docker Setup

If you prefer to run the application using Docker, follow these steps:

### 1. Build and Run the Docker Containers

Use Docker Compose to build and run the containers:

```bash
docker-compose up --build
```

This will:

- Build the Docker image for your Flask application.
- Start the Flask application and a MySQL database in Docker containers.

### 2. Access the Application

Once the containers are up, you can access the Flask app at `http://localhost:5000`.

### 3. Stopping the Containers

To stop the Docker containers:

```bash
docker-compose down
```

## Endpoints

The application includes the following endpoints:

- **Authentication**: `/api/v1/auth`
- **Profile Management**: `/api/v1/profile`
- **Profile Photo Upload**: `/api/v1/profile/photo`
- **Refresh Token**: `/api/v1/auth/refresh`

## Swagger API Documentation

You can view the API documentation by navigating to:

```
http://localhost:5000/apidocs/
```

This documentation is automatically generated using Flasgger and OpenAPI 3.

## License

This project is licensed under the MIT License.
