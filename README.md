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

## API Documentation

### QR Code Generation

- **Endpoint:** `/api/certificates/{certificate_id}/qr-code/`
- **Method:** GET
- **Description:** Generates a QR code for a specific certificate. The QR code is returned as a PNG image and can be downloaded with the filename `certificate_{certificate_id}_qrcode.png`.

### Certificate Validation

- **Endpoint:** `/api/certificates/validate/`
- **Method:** POST
- **Description:** Validates a certificate using its unique code.
- **Request Body:**
  ```json
  {
    "unique_code": "your-unique-code-here"
  }
  ```
- **Response:**
  ```json
  {
    "unique_code": "your-unique-code-here",
    "is_valid": true,
    "certificate": {
      "id": 1,
      "student": "John Doe",
      "course": "Python Programming",
      "issue_date": "2023-01-01",
      "expiry_date": "2024-01-01",
      "status": "active"
    },
    "message": "Certificate is valid"
  }
  ```
