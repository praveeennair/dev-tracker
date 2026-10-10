# DevTrack

## About
DevTrack is a lightweight issue tracking REST API built with Django and Django REST Framework (DRF). It allows development teams to record and track issues (bugs, tasks, and features) and associate them with team reporters. The API provides endpoints to create, retrieve, and filter issues by ID or lifecycle status (`open`, `in_progress`, `resolved`, `closed`), utilizing object-oriented domain models with polymorphic priority handling and input validation.

## How to Run

### Prerequisites
- Python 3.10+ (or Docker)
- pip

### Option 1: Local Setup

1. **Clone the repository and navigate to the project directory:**
   ```bash
   cd devtrack
   ```

2. **Create and activate a virtual environment:**
   - **Windows:**
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install project dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations (optional for Django admin/auth):**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```
   The API will be available at `http://127.0.0.1:8000/`.

---

### Option 2: Docker Setup

1. **Build and run the container with Docker Compose:**
   ```bash
   docker-compose up --build
   ```
   The API will be available at `http://localhost:8000/`.

## API Endpoints

| Method | Endpoint | What it does |
|--------|----------|--------------|
| `POST` | `/api/reporters/` | Creates and registers a new reporter |
| `GET` | `/api/reporters/` | Retrieves all registered reporters |
| `GET` | `/api/reporters/?id=<id>` | Retrieves a specific reporter by ID |
| `POST` | `/api/issues/` | Creates a new issue linked to an existing reporter with polymorphic priority processing |
| `GET` | `/api/issues/` | Retrieves all tracked issues |
| `GET` | `/api/issues/?id=<id>` | Retrieves a specific issue by ID |
| `GET` | `/api/issues/?status=<status>` | Filters and retrieves issues by status (`open`, `in_progress`, `resolved`, `closed`) |

---

### 1. `POST /api/reporters/`
Registers a new reporter in the system.

#### Success
- **Status Code:** `201 Created`
- **Payload:**
  ```json
  {
    "id": 1,
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "team": "Backend Engineering"
  }
  ```
- **Response:**
  ```json
  {
    "id": 1,
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "team": "Backend Engineering"
  }
  ```

#### Error
- **Status Code:** `400 Bad Request`
- **Payload (Missing Field):**
  ```json
  {
    "id": 2,
    "name": "Bob Smith"
  }
  ```
- **Response:**
  ```json
  {
    "error": "Missing field: 'email'"
  }
  ```
- **Payload (Duplicate ID):**
  ```json
  {
    "id": 1,
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "team": "Backend Engineering"
  }
  ```
- **Response:**
  ```json
  {
    "error": "Reporter ID already exists"
  }
  ```

---

### 2. `GET /api/reporters/`
Retrieves a list of all registered reporters.

#### Success
- **Status Code:** `200 OK`
- **Response:**
  ```json
  [
    {
      "id": 1,
      "name": "Alice Johnson",
      "email": "alice@example.com",
      "team": "Backend Engineering"
    }
  ]
  ```

---

### 3. `GET /api/reporters/?id=<id>`
Retrieves details of a specific reporter using their unique ID.

#### Success
- **Request URL:** `GET /api/reporters/?id=1`
- **Status Code:** `200 OK`
- **Response:**
  ```json
  {
    "id": 1,
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "team": "Backend Engineering"
  }
  ```

#### Error
- **Request URL (Non-Existent Reporter):** `GET /api/reporters/?id=999`
- **Status Code:** `404 Not Found`
- **Response:**
  ```json
  {
    "error": "Reporter not found"
  }
  ```
- **Request URL (Invalid ID Format):** `GET /api/reporters/?id=invalid`
- **Status Code:** `400 Bad Request`
- **Response:**
  ```json
  {
    "error": "Invalid reporter ID"
  }
  ```

---

### 4. `POST /api/issues/`
Creates a new issue ticket associated with an existing reporter. Uses polymorphic subclasses (`CriticalIssue`, `LowPriorityIssue`, `Issue`) to attach custom descriptive messages.

#### Success
- **Status Code:** `201 Created`
- **Payload (Critical Priority):**
  ```json
  {
    "id": 101,
    "title": "Database connection pool exhausted",
    "description": "Production service experiencing timeout errors under high traffic",
    "status": "open",
    "priority": "critical",
    "reporter_id": 1
  }
  ```
- **Response:**
  ```json
  {
    "id": 101,
    "title": "Database connection pool exhausted",
    "description": "Production service experiencing timeout errors under high traffic",
    "status": "open",
    "priority": "critical",
    "reporter_id": 1,
    "message": "[URGENT] Database connection pool exhausted — needs immediate attention"
  }
  ```

#### Error
- **Status Code:** `404 Not Found`
- **Payload (Non-Existent Reporter):**
  ```json
  {
    "id": 102,
    "title": "Fix navbar alignment",
    "description": "Button is shifted 5px to the left on mobile screens",
    "status": "open",
    "priority": "low",
    "reporter_id": 999
  }
  ```
- **Response:**
  ```json
  {
    "error": "Reporter not found"
  }
  ```
- **Status Code:** `400 Bad Request`
- **Payload (Invalid Status):**
  ```json
  {
    "id": 103,
    "title": "Update README docs",
    "description": "Include API endpoints reference",
    "status": "pending_review",
    "priority": "medium",
    "reporter_id": 1
  }
  ```
- **Response:**
  ```json
  {
    "error": "Invalid status"
  }
  ```
- **Payload (Duplicate Issue ID):**
  ```json
  {
    "id": 101,
    "title": "Duplicate Issue Title",
    "description": "Duplicate issue payload test",
    "status": "open",
    "priority": "medium",
    "reporter_id": 1
  }
  ```
- **Response:**
  ```json
  {
    "error": "Issue ID already exists"
  }
  ```

---

### 5. `GET /api/issues/`
Retrieves all tracked issues.

#### Success
- **Status Code:** `200 OK`
- **Response:**
  ```json
  [
    {
      "id": 101,
      "title": "Database connection pool exhausted",
      "description": "Production service experiencing timeout errors under high traffic",
      "status": "open",
      "priority": "critical",
      "reporter_id": 1
    }
  ]
  ```

---

### 6. `GET /api/issues/?id=<id>`
Retrieves a specific issue by its ID.

#### Success
- **Request URL:** `GET /api/issues/?id=101`
- **Status Code:** `200 OK`
- **Response:**
  ```json
  {
    "id": 101,
    "title": "Database connection pool exhausted",
    "description": "Production service experiencing timeout errors under high traffic",
    "status": "open",
    "priority": "critical",
    "reporter_id": 1
  }
  ```

#### Error
- **Request URL (Non-Existent Issue):** `GET /api/issues/?id=9999`
- **Status Code:** `404 Not Found`
- **Response:**
  ```json
  {
    "error": "Issue not found"
  }
  ```
- **Request URL (Invalid ID Format):** `GET /api/issues/?id=invalid`
- **Status Code:** `400 Bad Request`
- **Response:**
  ```json
  {
    "error": "Invalid issue ID"
  }
  ```

---

### 7. `GET /api/issues/?status=<status>`
Filters issues by lifecycle status (`open`, `in_progress`, `resolved`, `closed`).

#### Success
- **Request URL:** `GET /api/issues/?status=open`
- **Status Code:** `200 OK`
- **Response:**
  ```json
  [
    {
      "id": 101,
      "title": "Database connection pool exhausted",
      "description": "Production service experiencing timeout errors under high traffic",
      "status": "open",
      "priority": "critical",
      "reporter_id": 1
    }
  ]
  ```

---

## Design Decision
**Domain Entity Modeling with Polymorphic Priority Handling and Relation Validation:**

Instead of coupling all data transformations inside views, the system uses object-oriented domain entities (`BaseEntity`, `Reporter`, `Issue`, `CriticalIssue`, `LowPriorityIssue`):
- **Polymorphism via `.describe()`**: Subclasses customize issue presentation based on priority (`CriticalIssue` generates urgent alerts, while `LowPriorityIssue` flags items for deferred handling) without polluting the API views with conditional formatting.
- **Relational Integrity in File-Based Storage**: Even with JSON persistence (`reporters.json` and `issues.json`), issue creation strictly validates that the specified `reporter_id` exists before storing the ticket, preventing dangling or orphaned issues.
