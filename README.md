# Geo API (Django + PostGIS)

This is a simple Geo API built with **Django**, **Django REST Framework**, and **PostgreSQL + PostGIS**.  
The project provides authentication, geo point management, and geo-based search.

---

## Tech Stack

- Python 3.14.2
- Django
- Django REST Framework
- PostgreSQL + PostGIS
- GeoDjango
- SimpleJWT
- uv
- pytest
- ruff
- mypy
- pre-commit

---

## Requirements

### System requirements

- Python 3.14+
- PostgreSQL with PostGIS extension enabled
- GDAL
- GEOS

---

## Geo libraries setup

GeoDjango requires native C libraries.

### Windows

```
GDAL_LIBRARY_PATH=C:\User\username\path\to\lib\gdal312.dll
GEOS_LIBRARY_PATH=C:\User\username\path\to\lib\geos_c.dll
```

### Unix
```
GDAL_LIBRARY_PATH=/usr/lib/libgdal.so
GEOS_LIBRARY_PATH=/usr/lib/libgeos_c.so
```

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/Mixaqi/red_collar_test_task
cd red_collar_test_task
```
### 2. Install dependencies
```
uv sync
```

### 3. Create .env file in the root directory to store your configuration (check .env.example)

```
#django
SECRET_KEY
DEBUG

#geolibraries
GDAL_LIBRARY_PATH
GEOS_LIBRARY_PATH

#db (Postgres + PostGIS)
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_HOST
POSTGRES_PORT
```

### Database & Server management
All commands are executed through ```uv run``` to ensure they use the project's isolated enviroment

#### Database migrations
Create and apply the POSTGIS-enabled database schema:
```
uv run manage.py makemigrations
uv run manage.py migrate
```

Run development server
```
uv run manage.py runserver
```

### Tests
```
uv run pytest
```

### Git Hooks
To ensure code quality before every commit, initialize **pre-commit**

```uv run pre-commit install```

# Endpoints
Base URL
```
http://127.0.0.1:8000/api/
```

All protected endpoints require JWT authentication
```
Authorization: Bearer <access token>
```

## Authentication 
```/api/auth/```

### Register:

**POST** ```/api/auth/register/```

**Request body**:
```
{
    "username": "testuser",
    "email": "test@mail.com",
    "password": "password123Test"
}
```

**Response:**
```
{
    "username": "testuser",
    "email": "test@mail.com"
}
```

### Login:

**POST** ```/api/auth/login/```
**Request body**:
```
{
    "username": "testuser",
    "password": "password123Test"
}
```

**Response:**
```
{
    "refresh": "refresh_token",
    "access": "access_token"
}
```

### Refresh access token

**POST** ```/api/auth/refresh/```
**Request body**:
```
{
    "refresh": "refresh_token"
}
```

**Response:**
```
{
    "access": "access_token",
    "refresh": "refresh_token"
}
```

### Current user (Protected):
**GET** ```/api/auth/me/```

**Response:**
```
{
    "id": id,
    "username": "username"
}
```

### Logout (Protected):
**POST** ```/api/auth/logout/```
**Request body:**
```
{
    "refresh": "refresh_token"
}
```

**Response:** 
```
{
    "detail": "Logged out"
}
```
## Geo Points (Protected)
```/api/points/```

### Create point:

**POST** ```/api/points/```
**Request body:**
```
{
    "location": {"type": "Point", "coordinates": [11.88, 14.86]}
}
```

**Response**
```
{
    "type": "Feature",
    "geometry": {
        "type": "Point",
        "coordinates": [
            11.88,
            14.86
        ]
    },
    "properties": {
        "created_at": "2026-01-18T09:58:15.204377Z"
    }
}
```
**Rules**
1. Only GeoJSON Point is allowed
2. Coordinates order: [lon, lat]
3. SRID must be 4326
4. Latitude range: [-90, 90]
5. Longitude range: [-180, 180]
6. Point location must be unique

 ### Points search (Another points in this radius):
**GET** ```/api/points/search/?latitude=14.86&longitude=11.88&offset=0&radius=5```

**Response:**
```
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        11.88,
                        14.87
                    ]
                },
                "properties": {
                    "created_at": "2026-01-16T18:45:57.082802Z"
                }
            },

        ]
    }
}
```
### Add message to point 
**POST** ```/api/points/message/```

**Request body:**
```
{
  "text": "Hello world",
  "location": {
    "type": "Point",
    "coordinates": [11.88, 14.86]
  }
}
```

**Response:**
```
{
    "text": "Hello world",
    "created_at": "2026-01-18T10:12:38.499704Z",
    "location": {
        "type": "Point",
        "coordinates": [
            11.88,
            14.86
        ]
    }
}
```

### Search points in current radius
**POST** 
```/api/points/message/search/?latitude=14.86&longitude=11.88&radius=5```

**Response:**
```
[
    {
        "text": "Hello world",
        "created_at": "2026-01-18T10:12:38.499704Z",
        "location": {
            "type": "Point",
            "coordinates": [
                11.88,
                14.86
            ]
        }
    }
]
```


