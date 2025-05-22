# Certificate Generation System

A Django-based system for generating and validating certificates with QR code integration.

## Project Structure

```
certificate_project/
├── apps/                    # Main applications directory
│   └── certificate/         # Django app for certificate generation and QR code
├── config/                  # Django project configuration
├── shared/                  # Shared utilities and models
├── docker/                  # Docker configuration files
│   └── django/             # Django service Docker files
├── scripts/                 # Utility scripts
├── tests/                   # Test suites
├── .env.example            # Example environment variables
├── docker-compose.yml      # Docker compose configuration
└── requirements/           # Python dependencies
    ├── base.txt           # Common dependencies
    └── django.txt         # Django-specific dependencies
```

## Services

1. **Certificate Service (Django)**

   - Main application for certificate generation
   - User management and authentication
   - Certificate template management
   - Database operations
   - QR code generation for certificates

## Setup Instructions

1. Clone the repository
2. Copy `.env.example` to `.env` and configure environment variables
3. Build and run services:
   ```bash
   docker-compose up --build
   ```

## Development

- Django service runs on port 8000
- PostgreSQL runs on port 5432
- Swagger UI available at `http://localhost:8000/swagger/`

## Testing

```bash
# Run all tests
docker-compose run django python manage.py test
```

## API Documentation

The API documentation is available through Swagger UI at `http://localhost:8000/swagger/`. This interactive documentation allows you to:

- View all available API endpoints
- Test endpoints directly through the interface
- Understand request/response schemas
- Authenticate using JWT tokens

### Available Endpoints

#### Authentication

- **Token Obtain:** `/api/token/` (POST)
- **Token Refresh:** `/api/token/refresh/` (POST)

#### Certificates

- **List/Create:** `/api/certificates/` (GET, POST)
- **Detail/Update/Delete:** `/api/certificates/{id}/` (GET, PUT, PATCH, DELETE)
- **QR Code:** `/api/certificates/{id}/qr-code/` (GET)
- **Validate:** `/api/certificates/validate/` (POST)

#### Students

- **List/Create:** `/api/students/` (GET, POST)
- **Detail/Update/Delete:** `/api/students/{id}/` (GET, PUT, PATCH, DELETE)

#### Courses

- **List/Create:** `/api/courses/` (GET, POST)
- **Detail/Update/Delete:** `/api/courses/{id}/` (GET, PUT, PATCH, DELETE)

### Authentication

The API uses JWT (JSON Web Token) authentication. To access protected endpoints:

1. Obtain a token using the `/api/token/` endpoint
2. Include the token in the Authorization header: `Authorization: Bearer <your_token>`

For more details about authentication and available endpoints, please refer to the Swagger UI documentation.
