# We_Talk - Nepali Dating Platform

A Django-based REST API for a Nepali dating application that enables users to discover matches, send connection requests, and communicate with potential matches.

## 🎯 Features

- **User Authentication**: JWT-based authentication with token refresh
- **User Discovery**: Browse other users with filtering capabilities
- **Connection Requests**: Send, receive, and manage connection requests
- **Messaging System**: Direct messaging between connected users
- **User Profiles**: Comprehensive user profiles with personal information
- **Notifications**: Real-time notifications for activities
- **Activity Tracking**: Track user activities like login and profile updates
- **Docker Support**: Containerized deployment with PostgreSQL

## 🛠 Tech Stack

- **Backend Framework**: Django 5.0+
- **API Framework**: Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: PostgreSQL (with SQLite support for development)
- **Real-time Features**: Django Channels & Channels-Redis
- **Web Server**: Gunicorn
- **Image Processing**: Pillow
- **Containerization**: Docker & Docker Compose

## 📁 Project Structure

```
nepali_dating_python/
├── backend/                 # Django project configuration
│   ├── __init__.py
│   ├── asgi.py             # ASGI configuration for async support
│   ├── settings.py         # Django settings and configurations
│   ├── urls.py             # Main URL routing
│   ├── wsgi.py             # WSGI configuration
│
├── users/                  # Main application for user management
│   ├── migrations/         # Database migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_notification.py
│   │
│   ├── __init__.py
│   ├── admin.py            # Django admin configuration
│   ├── apps.py             # App configuration
│   ├── models.py           # Database models
│   ├── views.py            # API views and endpoints
│   ├── urls.py             # URL routing for users app
│   ├── tests.py            # Unit tests
│
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Docker Compose orchestration
├── Jenkinsfile             # CI/CD pipeline for Jenkins
├── deploy.jenkinsfile      # Deployment pipeline
└── README.md               # Project documentation
```

## 📊 Database Schema

### User Model
- **Extends**: AbstractUser (Django's built-in user model)
- **Fields**:
	- `age`: Integer - User's age
	- `gender`: CharField - User's gender
	- `location`: CharField - User's location
	- `bio`: TextField - User biography
	- `image`: ImageField - Profile picture (uploads to `profiles/` directory)

### Connection Model
- **Fields**:
	- `sender`: ForeignKey(User) - User sending the request
	- `receiver`: ForeignKey(User) - User receiving the request
	- `status`: CharField - Connection status (pending, accepted, rejected)
	- `created_at`: DateTimeField - Request creation timestamp

### Message Model
- **Fields**:
	- `sender`: ForeignKey(User) - Message sender
	- `receiver`: ForeignKey(User) - Message recipient
	- `message`: TextField - Message content
	- `created_at`: DateTimeField - Message timestamp

### Notification Model
- **Fields**:
	- `user`: ForeignKey(User) - Notification recipient
	- `message`: TextField - Notification content
	- `is_read`: BooleanField - Read status (default: False)
	- `created_at`: DateTimeField - Notification timestamp

### Activity Model
- **Fields**:
	- `user`: ForeignKey(User) - User performing activity
	- `activity_type`: CharField - Type of activity (e.g., "login", "profile_update")
	- `timestamp`: DateTimeField - Activity timestamp

## 🔌 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|----------------|
| POST | `/api/register/` | Register a new user | No |
| POST | `/api/login/` | Login and get JWT token | No |

### User Discovery

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|----------------|
| GET | `/api/` | API root and available endpoints | No |
| GET | `/api/discover/` | Get list of available users (excluding self) | Yes |

### Connections

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|----------------|
| POST | `/api/connect/<user_id>/` | Send connection request to a user | Yes |
| POST | `/api/respond/<connection_id>/` | Accept/reject connection request | Yes |

## 🚀 Setup and Installation

### Prerequisites
- Python 3.12+
- PostgreSQL 15+ (optional, SQLite can be used for development)
- Docker & Docker Compose (for containerized deployment)

### Local Development Setup

1. **Clone the repository**
	 ```bash
	 git clone <repository-url>
	 cd nepali_dating_python
	 ```

2. **Create a virtual environment**
	 ```bash
	 python -m venv venv
	 source venv/bin/activate  # On Windows: venv\Scripts\activate
	 ```

3. **Install dependencies**
	 ```bash
	 pip install -r requirements.txt
	 ```

4. **Set up environment variables**
	 ```bash
	 # For SQLite (default):
	 export DEBUG=True
   
	 # For PostgreSQL:
	 export DB_ENGINE=django.db.backends.postgresql
	 export DB_NAME=dating_db
	 export DB_USER=postgres
	 export DB_PASSWORD=your_password
	 export DB_HOST=localhost
	 export DB_PORT=5432
	 ```

5. **Run database migrations**
	 ```bash
	 python manage.py migrate
	 ```

6. **Create a superuser (admin)**
	 ```bash
	 python manage.py createsuperuser
	 ```

7. **Run the development server**
	 ```bash
	 python manage.py runserver
	 ```

The API will be available at `http://localhost:8000/api/`

### Docker Setup

1. **Build and start containers**
	 ```bash
	 docker-compose up --build
	 ```

2. **Run migrations in container**
	 ```bash
	 docker-compose exec backend python manage.py migrate
	 ```

3. **Create superuser in container**
	 ```bash
	 docker-compose exec backend python manage.py createsuperuser
	 ```

The API will be available at `http://localhost:8000/api/`

**Services**:
- Backend API: `http://localhost:8000`
- PostgreSQL: `localhost:5432`

## 📝 API Usage Examples

### Register a User
```bash
curl -X POST http://localhost:8000/api/register/ \
	-H "Content-Type: application/json" \
	-d '{
		"username": "john_doe",
		"email": "john@example.com",
		"password": "securepassword123",
		"age": 28,
		"gender": "Male",
		"location": "Kathmandu"
	}'
```

### Login
```bash
curl -X POST http://localhost:8000/api/login/ \
	-H "Content-Type: application/json" \
	-d '{
		"username": "john_doe",
		"password": "securepassword123"
	}'
```

### Discover Users
```bash
curl -X GET http://localhost:8000/api/discover/ \
	-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Send Connection Request
```bash
curl -X POST http://localhost:8000/api/connect/5/ \
	-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
### ☸️ Kubernetes Deployment
## Deploy namespace

kubectl apply -f k8s/namespace.yaml

Deploy ConfigMaps

kubectl apply -f k8s/configmap.yaml

Deploy Secrets

kubectl apply -f k8s/secret.yaml

Deploy PostgreSQL

kubectl apply -f k8s/postgres/

Deploy Backend

kubectl apply -f k8s/backend/

Deploy Ingress

kubectl apply -f k8s/ingress.yaml

### Verify

kubectl get all

## 🔧 Configuration

### Django Settings
Configuration is managed in backend/settings.py:

- **Debug Mode**: Set `DEBUG = False` for production
- **Secret Key**: Change `SECRET_KEY` in production
- **Allowed Hosts**: Update `ALLOWED_HOSTS` for production domains
- **Database**: Configure database engine and credentials
- **Authentication**: JWT token configuration in REST_FRAMEWORK settings

### Environment Variables
```
DEBUG=True/False
SECRET_KEY=your_secret_key
DB_ENGINE=django.db.backends.postgresql
DB_NAME=dating_db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

## 🧪 Testing

Run tests with:
```bash
python manage.py test
```

Run specific test module:
```bash
python manage.py test users.tests
```

## 📦 Dependencies

See requirements.txt for complete list:
- Django 5.0+
- djangorestframework
- djangorestframework-simplejwt
- pillow
- psycopg2-binary
- channels
- channels-redis
- gunicorn

## 🔐 Security Notes

⚠️ **Important**: These settings are for development only!

- Change `SECRET_KEY` in production
- Set `DEBUG = False` in production
- Update `ALLOWED_HOSTS` with your domain
- Use environment variables for sensitive data
- Implement HTTPS in production
- Add CORS configuration for frontend domains

## 🐳 Deployment

### Using Docker
```bash
# Build production image
docker build -t dating-app:latest .

# Run with production settings
docker run -e DEBUG=False \
	-e SECRET_KEY=your_production_key \
	-e DB_HOST=your_db_host \
	dating-app:latest
```

### CI/CD Pipeline
The project includes Jenkins configurations:
- Jenkinsfile - Main pipeline
- deploy.jenkinsfile - Deployment pipeline

## 🤝 Contributing

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Commit your changes (`git commit -m 'Add amazing feature'`)
3. Push to the branch (`git push origin feature/amazing-feature`)
4. Open a Pull Request

## 📄 License

This project is part of the We_Talk Nepali Dating Platform.

## 📞 Support

For issues and questions, please open an issue in the repository.

## 👥 Team

Built with ❤️ for the Nepali community.

---

**Last Updated**: 2024
**Version**: 1.0.0
