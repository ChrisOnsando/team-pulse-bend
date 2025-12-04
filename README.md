# Full-stack Team Pulse MVP - Backend API

A Django REST Framework API for tracking team mood and workload through pulse check-ins.

## 📦 Installation

### Prerequisites

- Python 3.9+
- PostgreSQL 12+

### Setup

```bash
# Clone the repository
git clone <your-repository-url>
cd team-pulse-bend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create PostgreSQL database
psql -U postgres
CREATE DATABASE teampulse;
\q

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

## 🚀 Running the Application

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

Admin panel: `http://localhost:8000/admin`

## 🔗 API Endpoints

### Base URL
```
http://localhost:8000/api/v1/
```

### Authentication

#### Register User
```http
POST /api/v1/auth/register/
```
**Request:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe"
}
```
**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "john@example.com",
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "is_staff": false,
  "is_active": true,
  "teams": [],
  "created_at": "2024-01-15T10:30:00Z",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Login
```http
POST /api/v1/auth/login/
```
**Request:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123"
}
```
**Response:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Refresh Token
```http
POST /api/v1/auth/refresh/
```
**Request:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```
**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Logout
```http
POST /api/v1/auth/logout/
Authorization: Bearer {access_token}
```
**Request:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### Users

#### Get Current User
```http
GET /api/v1/users/me/
Authorization: Bearer {access_token}
```
**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "john@example.com",
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "is_staff": false,
  "is_active": true,
  "teams": ["Engineering"],
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Update Current User
```http
PATCH /api/v1/users/me/
Authorization: Bearer {access_token}
```
**Request:**
```json
{
  "first_name": "Johnny",
  "last_name": "Doe"
}
```

#### List All Users (Admin Only)
```http
GET /api/v1/users/
Authorization: Bearer {admin_access_token}
```
**Response:**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/v1/users/?page=2",
  "previous": null,
  "results": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "john@example.com",
      "username": "johndoe",
      "first_name": "John",
      "last_name": "Doe",
      "is_staff": false,
      "is_active": true,
      "teams": ["Engineering"],
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Get User by ID (Admin Only)
```http
GET /api/v1/users/{user_id}/
Authorization: Bearer {admin_access_token}
```

#### Update User (Admin Only)
```http
PATCH /api/v1/users/{user_id}/
Authorization: Bearer {admin_access_token}
```

#### Delete User (Admin Only)
```http
DELETE /api/v1/users/{user_id}/
Authorization: Bearer {admin_access_token}
```

---

### Teams

#### List Teams
```http
GET /api/v1/teams/
Authorization: Bearer {access_token}
```
**Response:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440000",
      "team_name": "Engineering",
      "members": [
        {
          "id": "550e8400-e29b-41d4-a716-446655440000",
          "username": "johndoe",
          "email": "john@example.com",
          "first_name": "John",
          "last_name": "Doe"
        }
      ],
      "member_count": 8,
      "created_at": "2024-01-10T09:00:00Z"
    }
  ]
}
```

#### Create Team (Admin Only)
```http
POST /api/v1/teams/
Authorization: Bearer {admin_access_token}
```
**Request:**
```json
{
  "team_name": "Engineering"
}
```
**Response:**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440000",
  "team_name": "Engineering",
  "members": [],
  "member_count": 0,
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Get Team
```http
GET /api/v1/teams/{team_id}/
Authorization: Bearer {access_token}
```

#### Update Team (Admin Only)
```http
PATCH /api/v1/teams/{team_id}/
Authorization: Bearer {admin_access_token}
```
**Request:**
```json
{
  "team_name": "Engineering Team"
}
```

#### Delete Team (Admin Only)
```http
DELETE /api/v1/teams/{team_id}/
Authorization: Bearer {admin_access_token}
```

#### Add Member to Team (Admin Only)
```http
POST /api/v1/teams/{team_id}/add-member/
Authorization: Bearer {admin_access_token}
```
**Request:**
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000"
}
```
**Response:**
```json
{
  "status": "member added"
}
```

#### Remove Member from Team (Admin Only)
```http
POST /api/v1/teams/{team_id}/remove-member/
Authorization: Bearer {admin_access_token}
```
**Request:**
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000"
}
```
**Response:**
```json
{
  "status": "member removed"
}
```

---

### Moods

#### List Moods
```http
GET /api/v1/moods/
Authorization: Bearer {access_token}
```
**Response:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440000",
      "value": 5,
      "description": "Excellent",
      "image_url": "https://example.com/excellent.png",
      "created_at": "2024-01-01T00:00:00Z"
    },
    {
      "id": "770e8400-e29b-41d4-a716-446655440001",
      "value": 4,
      "description": "Good",
      "image_url": "https://example.com/good.png",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

#### Create Mood (Admin Only)
```http
POST /api/v1/moods/
Authorization: Bearer {admin_access_token}
```
**Request:**
```json
{
  "value": 5,
  "description": "Excellent",
  "image_url": "https://example.com/excellent.png"
}
```

#### Get Mood
```http
GET /api/v1/moods/{mood_id}/
Authorization: Bearer {access_token}
```

#### Update Mood (Admin Only)
```http
PATCH /api/v1/moods/{mood_id}/
Authorization: Bearer {admin_access_token}
```

#### Delete Mood (Admin Only)
```http
DELETE /api/v1/moods/{mood_id}/
Authorization: Bearer {admin_access_token}
```

---

### Workloads

#### List Workloads
```http
GET /api/v1/workloads/
Authorization: Bearer {access_token}
```
**Response:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "880e8400-e29b-41d4-a716-446655440000",
      "value": 3,
      "description": "Moderate",
      "image_url": "https://example.com/moderate.png",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

#### Create Workload (Admin Only)
```http
POST /api/v1/workloads/
Authorization: Bearer {admin_access_token}
```
**Request:**
```json
{
  "value": 3,
  "description": "Moderate",
  "image_url": "https://example.com/moderate.png"
}
```

#### Get Workload
```http
GET /api/v1/workloads/{workload_id}/
Authorization: Bearer {access_token}
```

#### Update Workload (Admin Only)
```http
PATCH /api/v1/workloads/{workload_id}/
Authorization: Bearer {admin_access_token}
```

#### Delete Workload (Admin Only)
```http
DELETE /api/v1/workloads/{workload_id}/
Authorization: Bearer {admin_access_token}
```

---

### Pulse Logs

#### List Pulse Logs
```http
GET /api/v1/pulse-logs/
Authorization: Bearer {access_token}
```
**Query Parameters:**
- `user` - Filter by user ID
- `team` - Filter by team ID
- `year` - Filter by year
- `week_index` - Filter by week number
- `mood` - Filter by mood value
- `workload` - Filter by workload value

**Response:**
```json
{
  "count": 48,
  "next": "http://localhost:8000/api/v1/pulse-logs/?page=2",
  "previous": null,
  "results": [
    {
      "id": "990e8400-e29b-41d4-a716-446655440000",
      "user": "550e8400-e29b-41d4-a716-446655440000",
      "user_name": "johndoe",
      "mood": 4,
      "workload": 3,
      "comment": "Great week! Shipped new feature.",
      "timestamp": "2024-01-15T10:30:00Z",
      "team": "660e8400-e29b-41d4-a716-446655440000",
      "team_name": "Engineering",
      "timestamp_local": "2024-01-15T05:30:00Z",
      "year": 2024,
      "week_index": 3,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Create Pulse Log
```http
POST /api/v1/pulse-logs/
Authorization: Bearer {access_token}
```
**Request:**
```json
{
  "mood": 4,
  "workload": 3,
  "comment": "Great week! Shipped new feature.",
  "team": "660e8400-e29b-41d4-a716-446655440000"
}
```
**Response:**
```json
{
  "id": "990e8400-e29b-41d4-a716-446655440000",
  "user": "550e8400-e29b-41d4-a716-446655440000",
  "user_name": "johndoe",
  "mood": 4,
  "workload": 3,
  "comment": "Great week! Shipped new feature.",
  "timestamp": "2024-01-15T10:30:00Z",
  "team": "660e8400-e29b-41d4-a716-446655440000",
  "team_name": "Engineering",
  "year": 2024,
  "week_index": 3,
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Get Pulse Log
```http
GET /api/v1/pulse-logs/{log_id}/
Authorization: Bearer {access_token}
```

#### Update Pulse Log
```http
PATCH /api/v1/pulse-logs/{log_id}/
Authorization: Bearer {access_token}
```

#### Delete Pulse Log
```http
DELETE /api/v1/pulse-logs/{log_id}/
Authorization: Bearer {access_token}
```

---

### Event Logs

#### List Event Logs (Admin Only)
```http
GET /api/v1/event-logs/
Authorization: Bearer {admin_access_token}
```
**Response:**
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/v1/event-logs/?page=2",
  "previous": null,
  "results": [
    {
      "id": "aa0e8400-e29b-41d4-a716-446655440000",
      "timestamp": "2024-01-15T10:30:00Z",
      "event_name": "user_login",
      "metadata": "{\"ip\": \"192.168.1.1\", \"device\": \"mobile\"}",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Create Event Log (Admin Only)
```http
POST /api/v1/event-logs/
Authorization: Bearer {admin_access_token}
```
**Request:**
```json
{
  "event_name": "user_login",
  "metadata": "{\"ip\": \"192.168.1.1\", \"device\": \"mobile\"}"
}
```

#### Get Event Log (Admin Only)
```http
GET /api/v1/event-logs/{log_id}/
Authorization: Bearer {admin_access_token}
```

#### Update Event Log (Admin Only)
```http
PATCH /api/v1/event-logs/{log_id}/
Authorization: Bearer {admin_access_token}
```

#### Delete Event Log (Admin Only)
```http
DELETE /api/v1/event-logs/{log_id}/
Authorization: Bearer {admin_access_token}
```
### Team Feedbacks

#### Create Non-Anonymous Feedback
```http
Post /api/v1/team-feedbacks/
Authorization: Bearer {access_token}
```
**Request:**
```json
'{
    "message": "Great team collaboration this week!",
    "is_anonymous": false
  }'
```
**Response:**
```json
{
  "id": "bb0e8400-e29b-41d4-a716-446655440000",
  "username": "johndoe",
  "message": "Great team collaboration this week!",
  "is_anonymous": false,
  "created_at": "2024-01-15T10:30:00Z"
}
```
#### Create Anonymous Feedback
```http
Post /api/v1/team-feedbacks/
Authorization: Bearer {access_token}
```
**Request:**
```json
'{
    "message": "Great team collaboration this week!",
    "is_anonymous": true
  }'
```
**Response:**
```json
{
  "id": "bb0e8400-e29b-41d4-a716-446655440000",
  "username": "anonymous",
  "message": "Great team collaboration this week!",
  "is_anonymous": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### List All Feedbacks
```http
Get /api/v1/team-feedbacks/
Authorization: Bearer {access_token}
```
**Response:**
```json
{
  "count": 15,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "cc0e8400-e29b-41d4-a716-446655440000",
      "username": "Anonymous",
      "message": "I think we need to improve our communication.",
      "is_anonymous": true,
      "created_at": "2024-01-15T10:35:00Z"
    },
    {
      "id": "bb0e8400-e29b-41d4-a716-446655440000",
      "username": "johndoe",
      "message": "Great team collaboration this week!",
      "is_anonymous": false,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### Get Specific Feedback
```http
Get /api/v1/team-feedbacks/{feedback_id}/
Authorization: Bearer {access_token}
```
#### Delete Feedback (Own feedback only)
```http
Get /api/v1/team-feedbacks/{feedback_id}/
Authorization: Bearer {access_token}
```
#### Filter Anonymous Feedback Only
```http
Get /api/v1/team-feedbacks/?is_anonymous=true"
Authorization: Bearer {access_token}
```
---
## 👥 Contributor

- **ChrisOnsando** - Backend Development

---

**Built with Django REST Framework**