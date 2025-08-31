# Movie Review API

## Project Overview
This is a Django REST Framework API for managing movie reviews. Users can register, log in, and perform CRUD operations on reviews. JWT authentication is supported for secure access.

## Features
- User registration and authentication (JWT)
- CRUD operations for users and reviews
- Only review owners can edit/delete their reviews
- Search, filter, sort, and paginate reviews
- View reviews for a specific movie
- Rating validation (1–5)

## Setup Instructions
1. Clone the repository and navigate to the project folder.
2. Create and activate a virtual environment:
	```powershell
	python -m venv venv
	.\venv\Scripts\activate
	```
3. Install dependencies:
	```powershell
	pip install -r requirements.txt
	# Or manually:
	pip install django djangorestframework djangorestframework-simplejwt
	```
4. Run migrations:
	```powershell
	python manage.py makemigrations
	python manage.py migrate
	```
5. Create a superuser (optional):
	```powershell
	python manage.py createsuperuser
	```
6. Start the development server:
	```powershell
	python manage.py runserver
	```

## API Endpoints

### Authentication
- `POST /api/register/` — Register a new user
- `POST /api/token/` — Obtain JWT token (login)
- `POST /api/token/refresh/` — Refresh JWT token

### Users
- `GET /api/users/` — List users
- `GET /api/users/{id}/` — Retrieve user
- `PUT /api/users/{id}/` — Update user
- `DELETE /api/users/{id}/` — Delete user

### Reviews
- `GET /api/reviews/` — List all reviews (supports search, filter, sort, pagination)
- `POST /api/reviews/` — Create a review (auth required)
- `GET /api/reviews/{id}/` — Retrieve a review
- `PUT /api/reviews/{id}/` — Update a review (owner only)
- `DELETE /api/reviews/{id}/` — Delete a review (owner only)
- `GET /api/reviews/movie/{title}/` — List reviews for a specific movie (paginated)

#### Filtering & Searching
- Search by movie title or rating: `/api/reviews/?search=Inception` or `/api/reviews/?search=5`
- Filter by movie title: `/api/reviews/?movie_title=Inception`
- Filter by rating(s): `/api/reviews/?rating=4&rating=5`
- Sort by rating or date: `/api/reviews/?ordering=rating` or `/api/reviews/?ordering=-created_date`

## Notes
- Only authenticated users can create, update, or delete reviews.
- Users can only modify their own reviews.
- Ratings must be between 1 and 5.

## Deployment
To deploy, use platforms like Heroku or PythonAnywhere. Ensure you set up environment variables and production settings as needed.