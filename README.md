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

## Testing

```bash
# Run all tests
docker-compose run django python manage.py test
```
