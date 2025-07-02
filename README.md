# Train Ticket Booking API

A Django REST Framework project for managing users, trains, stations, and train routes with JWT authentication and robust validation.

---

## Features
- User registration and login (JWT authentication)
- Role-based user management (admin, passenger)
- CRUD for stations and trains
- Add, update, delete train stops (with stop number management)
- Soft delete for all major entities (users, stations, trains, stops)
- Search stations by name or code
- Logging for all key actions and errors
- Signals for auto-creating roles and default admin
- PostgreSQL support

---

## Project Structure
```
ticketbooking/
  accounts/         # User and role management
  trains/           # Trains, stations, and stops
  utils/            # Shared constants
  requirements.txt  # Python dependencies
  README.md         # Project documentation
```

---

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <project-root>
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your database in `ticketbooking/settings.py`:**
   - Use PostgreSQL (recommended)
   - Example:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'your_db',
             'USER': 'your_user',
             'PASSWORD': 'your_password',
             'HOST': 'localhost',
             'PORT': '5432',
         }
     }
     ```

5. **Apply migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

---

## Environment Variables
- Set your `SECRET_KEY` and database credentials in `settings.py` or use a `.env` file with `python-dotenv` (optional).

---

## API Usage

### **Authentication**
- Register: `POST /api/auth/register/`
- Login: `POST /api/auth/login/` (returns JWT access and refresh tokens)
- Use the `Authorization: Bearer <access_token>` header for protected endpoints.

### **Stations**
- List: `GET /api/admin/stations/`
- Search by name: `GET /api/admin/stations/by-name/?name=salem`
- Search by code: `GET /api/admin/stations/by-code/?code=MAS`
- Create/Update/Delete: Admin only

### **Trains**
- List: `GET /api/admin/trains/`
- Search by number: `GET /api/admin/trains/by-number/?number=12345`
- Create/Update/Delete: Admin only

### **Train Stops (Routes)**
- Add stop: `POST /api/admin/train-stations/create-route/`
- List stops for train: `GET /api/admin/train-stations/by-train/?train_number=12345`
- Delete stop: `DELETE /api/admin/train-stations/train/<train_number>/station/<station_code>/delete-stop/`
- Delete all stops: `DELETE /api/admin/train-stations/train/<train_number>/delete-all-stops/`

---

## Logging
- All key actions, validations, and errors are logged using `train_logger` and `request_logger`.
- Configure logging output in your Django `settings.py` as needed.

---

## Contribution Guidelines
- Fork the repo and create a feature branch.
- Write clear commit messages.
- Add/modify tests for new features or bug fixes.
- Open a pull request with a clear description of your changes.

---

## License
This project is licensed under the MIT License.
