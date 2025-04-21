## To run the application, follow these steps:

### Installation:

**Clone the Git repository:**

```bash
git clone https://github.com/Monnkes/Swift-Data-API.git
```

### Running with Docker:

1. **Ensure Docker and Docker Compose are installed**:
    - Install Docker: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
    - Install Docker Compose: [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)


2. **Build and run the Docker containers**:
   To run the application:
   ```bash
   docker-compose up --build
   ```

   This will:
    - Build the Docker images for the app and database.
    - Start the services defined in the `docker-compose.yml` file.

3. **Stop the containers**:
   To stop the running containers, use:
   ```bash
   docker-compose down
   ```
   Or, to remove all containers, volumes, and networks:
   ```bash
   docker-compose down -v
   ```

### Access the application:

- API: The swift app will be available at [http://localhost:8080](http://localhost:8080)

## Testing the Application

### Prerequisites
Before running tests, ensure you have:
- ensure you have already running app
- ensure you are in swift_app package:
```bash
    cd swift_app
```

### Running Tests
With prerequisites you can run all tests with one command:
```bash
    pytest
```

To get test coverage:
```bash
    coverage run -m pytest
    coverage report -m
```

If you want to run only unit test, your app don't need to run.
You can than use just:
```bash
    pytest tests/unit
```

You can also run endpoint tests manually using postman app by importing this file:
[Download Postman Collection](./SwiftAPI.postman_collection.json)