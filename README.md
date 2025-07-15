# IT Helpdesk Agent

An MCP (Model Context Protocol) server application for managing IT helpdesk services and service requests. This application provides a REST API for tracking IT equipment/services inventory and managing service requests from employees.

## 🚀 Features

- **Service Management**: Track IT services/equipment with quantities
- **Service Request Management**: Handle employee requests for IT services
- **Database Integration**: PostgreSQL database with SQLModel ORM
- **MCP Protocol**: Built using FastMCP for seamless integration with AI assistants
- **Docker Support**: Containerized application for easy deployment
- **Modern Python**: Built with Python 3.13+ and modern async patterns

## 📋 API Endpoints

The application exposes the following MCP tools:

### Service Management

- **`read_services()`** - Fetch all available services
- **`modify_service_quantity(service_id, quantity)`** - Update service inventory quantities

### Service Request Management

- **`read_service_requests()`** - Fetch all service requests
- **`create_new_service_request(request)`** - Create new service requests
- **`modify_service_request_status(request_id, status)`** - Update request status

## 🏗️ Architecture

### Database Models

**Service Model:**

- `id`: Primary key
- `name`: Service name (indexed, max 100 chars)
- `description`: Optional service description (max 500 chars)
- `quantity`: Available quantity (≥ 0)
- `created_at`, `updated_at`: Timestamps

**ServiceRequest Model:**

- `id`: Primary key
- `service_id`: Foreign key to Service
- `requester_name`: Name of requester (max 100 chars)
- `request_date`: When request was made
- `status`: Enum (`pending`, `approved`, `returned`)
- `created_at`, `updated_at`: Timestamps

### Project Structure

```text
├── server/
│   ├── main.py              # MCP server entry point
│   ├── config.py            # Configuration settings
│   ├── models/              # SQLModel database models
│   │   ├── service.py
│   │   └── service_request.py
│   ├── schemas/             # Pydantic schemas for API
│   │   ├── service.py
│   │   └── service_request.py
│   ├── crud/                # Database operations
│   │   ├── service.py
│   │   └── service_request.py
│   └── db/
│       └── init_db.py       # Database initialization
├── Dockerfile               # Multi-stage Docker build
├── compose.yaml             # Docker Compose configuration
├── pyproject.toml           # UV package management
└── requirements.txt         # Python dependencies
```

## 🐳 Getting Started with Docker

### Prerequisites

- Docker and Docker Compose
- PostgreSQL database

### Environment Setup

1. Create a `.env` file in the project root:

```env
POSTGRES_DATABASE_URL=postgresql://username:password@localhost:5432/helpdesk_db
```

### Running the Application

1. **Using Docker Compose (Recommended):**

```bash
docker-compose up --build
```

2. **Using Docker directly:**

```bash
# Build the image
docker build -t it-helpdesk-agent .

# Run the container
docker run -p 8000:8000 --env-file .env it-helpdesk-agent
```

The server will be available at `http://localhost:8000`

## 🛠️ Development Setup

### Local Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- PostgreSQL database

### Local Development

1. **Install dependencies with uv:**

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

2. **Set up environment variables:**

```bash
export POSTGRES_DATABASE_URL="postgresql://username:password@localhost:5432/helpdesk_db"
```

3. **Run the server:**

```bash
python -m server.main --port 8000
```

## 📦 Dependencies

Key dependencies managed by UV:

- **FastMCP**: MCP server framework
- **SQLModel**: Modern SQL toolkit for Python
- **FastAPI**: High-performance web framework
- **asyncpg/psycopg2**: PostgreSQL drivers
- **uvicorn**: ASGI server for production

## 🔧 Configuration

The application uses environment variables for configuration:

| Variable | Description | Required |
|----------|-------------|----------|
| `POSTGRES_DATABASE_URL` | PostgreSQL connection string | Yes |

## 🚀 Deployment

### Production Deployment

1. **Set up PostgreSQL database**
2. **Configure environment variables**
3. **Deploy using Docker Compose:**

```bash
docker-compose up -d --build
```

### Health Checks

The application automatically:

- Creates database tables on startup
- Validates database connectivity
- Provides structured error responses

## 📝 Usage Examples

### Creating a Service Request

```python
# Example service request payload
{
    "service_id": 1,
    "requester_name": "John Doe",
    "status": "pending"
}
```

### Updating Service Quantity

```python
# Example quantity update
{
    "quantity": 50
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:

- Check the documentation
- Review the API schemas in `/server/schemas/`
- Examine the models in `/server/models/`

---

Built with ❤️ using Python, FastMCP, and Docker