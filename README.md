# Janitri Backend Assignment

## Overview

This project is a backend system for monitoring patients' heart rate using devices. Built with **Django** and  **Django REST Framework (DRF)** , it provides RESTful APIs to manage users, patients, places, devices, and heart rate records.

The system ensures  **secure data handling** ,  **validation** ,  **pagination** , and **filtering** wherever required. Swagger documentation is also available for easy API exploration.

---

## Features

* User registration and login (with authentication)
* Patient management (add and retrieve)
* Device management (assign to patients, toggle status)
* Heart rate recording and retrieval
* Pagination, filtering, and ordering on list APIs
* Redis integration for caching or OTP management
* Robust validation and error handling
* Unit tests for major functionalities

---

## Setup Instructions

### Prerequisites

* Python 3.10+
* Redis
* Virtual environment (`venv` or `virtualenv`)

### Installation

1. **Clone the repository:**

**bash**

```
git clone <your-repo-url>
cd janitri-backend
```

2. **Create and activate a virtual environment:**

**bash**

```
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate      # Windows
```

3. **Install dependencies:**

**bash**

```
pip install -r requirements.txt
```

4. **Install and start Redis:**
   **Linux / Mac:**
   **bash**

   ```
   brew install redis      # macOS
   sudo apt install redis  # Ubuntu/Debian
   redis-server
   ```

   **Windows:**
   Download and install Redis from [https://redis.io/docs/getting-started/](https://redis.io/docs/getting-started/). Start Redis server manually.
5. **Configure environment variables:**
   Copy `.env.example` to `.env` and set values for:

   * `SECRET_KEY`
   * `DATABASE_URL`
   * `REDIS_URL` (e.g., `redis://127.0.0.1:6379/0`)
   * Any other required keys
6. **Apply migrations:**

**bash**

```
python manage.py migrate
```

7. **Create a superuser (optional):**

**bash**

```
python manage.py createsuperuser
```

8. **Run the server:**

**bash**

```
python manage.py runserver
```

The API will be available at [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/).

---

## API Documentation

The project uses DRF Spectacular for API documentation.

* **Swagger UI:**
  [http://127.0.0.1:8000/api/swagger/](http://127.0.0.1:8000/api/swagger/) or [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
* **Redoc UI:**
  [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)
* **OpenAPI Schema:**
  [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)

---

## Endpoints Overview

### Users

* `POST /api/auth/register/` — Register a new user
* `POST /api/auth/login/` — Login user

### Patients

* `GET/POST /api/patients/` — List and create patients
* `GET /api/patients/<id>/` — Retrieve patient details

### Devices

* `GET/POST /api/devices/` — List and create devices
* `GET/PUT /api/devices/<id>/` — Update or retrieve a device
* `POST /api/devices/<id>/change-status/` — Toggle device active/inactive

### Heart Rate Records

* `POST /api/records/` — Record heart rate
* `GET /api/records/<patient_id>/` — Retrieve heart rate history

> All APIs require authentication (token-based).

---

## Assumptions / Decisions

* A patient can have only one device assigned at a time.
* Devices are always linked to a place (clinic/hospital).
* Heart rate is stored in BPM (beats per minute).
* Redis is used for caching or temporary storage (like OTPs).
* SMTP is used to send user credentials when created by admin.
* API responses follow a consistent success/error format.
* Unit tests cover major functionalities including device assignment, patient creation, and heart rate recording.

---

## Testing

Run all tests using:

**bash**

```
python manage.py test
```

---

## Additional Information

* Admin panel available at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
* DRF Spectacular is used for auto-generated API documentation
* Code structure follows Django best practices with apps for users, places, patients, devices, records, and alerts.
* Redis is required for OTP management. Ensure Redis server is running before starting the Django server.

SMTP integration is added:

* When an  **admin creates a new user** , that user automatically receives an email with login credentials.

---



## Personal Note

I was originally planning to build a project around **family health care** — a system to track health records, medicine intake, medical reports, and checkup history, helping families take the right steps at the right time.

However, I received this assignment from  **Janitri** , and I am grateful for the opportunity. This project helped me learn and apply multiple backend concepts in a real-world healthcare context.

**Thank you, Janitri, for giving me this chance. I am looking forward to working with you!**

---



## Contact

For questions or clarifications, contact:
Name: Rabindra Maharana
Email: maharanarabindra2001@gmail.com
Phone: 9337947267
