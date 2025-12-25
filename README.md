# Movie Review API

A Django REST Framework API for managing movie reviews with a stunning **Cinema Dark Mode** UI. Search movies via OMDB API, write reviews with interactive star ratings, and enjoy a professional dark-themed interface.

## Features

### API Features
- User registration and authentication (JWT)
- CRUD operations for users and reviews
- OMDB API integration for movie search
- Only review owners can edit/delete their reviews
- Search, filter, sort, and paginate reviews
- Rating validation (1–5 stars)

### UI Features (Cinema Dark Mode)
- Dark theme with gold accents (movie theater aesthetic)
- Interactive star rating component
- Skeleton loader with shimmer animation
- Toast notifications (success, error, warning, info)
- Animated hero section with film strip background
- Fully responsive design
- GPU-accelerated animations

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/Kalanza/Movie-Review-API-.git
cd Movie-Review-API-

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser (optional)
python manage.py createsuperuser

# Start server
python manage.py runserver
```

### 2. Access the Application

- **Homepage**: http://localhost:8000
- **Movie Search**: http://localhost:8000/search/
- **Reviews**: http://localhost:8000/reviews/
- **Admin Panel**: http://localhost:8000/admin/
- **API Docs (Swagger)**: http://localhost:8000/swagger/

## UI Components

### Star Rating
Interactive 5-star rating system with hover effects:
```html
<div data-star-rating data-input="rating"></div>
<input type="hidden" id="rating" name="rating">
```

### Toast Notifications
```javascript
window.toast.success('Review submitted!');
window.toast.error('Failed to load data');
window.toast.warning('Please fill all fields');
window.toast.info('Loading...');
```

### Skeleton Loader
```javascript
const skeleton = window.createSkeletonLoader(6);
$('#results').append(skeleton);
```

## API Endpoints

### Authentication
- `POST /api/register/` — Register a new user
- `POST /api/token/` — Obtain JWT token (login)
- `POST /api/token/refresh/` — Refresh JWT token

### Reviews
- `GET /api/reviews/` — List all reviews
- `POST /api/reviews/` — Create a review (auth required)
- `GET /api/reviews/{id}/` — Retrieve a review
- `PUT /api/reviews/{id}/` — Update review (owner only)
- `DELETE /api/reviews/{id}/` — Delete review (owner only)

### Movie Search
- `GET /api/search-movies/?search={title}` — Search movies via OMDB API

### Filtering & Searching
```
/api/reviews/?search=Inception
/api/reviews/?movie_title=Inception
/api/reviews/?rating=4&rating=5
/api/reviews/?ordering=rating
/api/reviews/?ordering=-created_date
```

## Design System

### Color Palette
- **Backgrounds**: #121212, #1f1f1f, #1a1a1a
- **Gold Accent**: #FFD700 (movie theater lights)
- **Text**: #FFFFFF, #B0B0B0, #707070

### Typography
- **Headers**: Oswald (Google Fonts)
- **Body**: Open Sans (Google Fonts)

### Key Features
- Hover effects on movie cards (lift + glow)
- Gold gradient buttons
- Animated film strip background
- Smooth transitions and animations

## Customization

### Change Accent Color
Edit `static/css/custom.css`:
```css
:root {
    --accent-gold: #YOUR_COLOR;
}
```

### Adjust Animation Speed
```css
.card {
    transition: all 0.6s ease; /* Change from default 0.4s */
}
```

## Project Structure

```
Movie-Review-API-/
├── moviereviewapi/          # Django settings
├── reviews/                 # Main app
│   ├── templates/          # HTML templates
│   ├── views.py            # Views
│   ├── models.py           # Database models
│   ├── serializers.py      # DRF serializers
│   └── urls.py             # URL routing
├── static/                 # Static files
│   ├── css/custom.css     # Cinema Dark styling
│   └── js/custom.js       # Interactive components
├── staticfiles/           # Collected static files
├── manage.py              # Django management
└── requirements.txt       # Dependencies
```

## Environment Variables

Create a `.env` file for production:
```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
OMDB_API_KEY=your-omdb-api-key
```

## Deployment

### Heroku
```bash
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py collectstatic --noinput
```

### PythonAnywhere
1. Upload code to PythonAnywhere
2. Set up virtual environment
3. Configure WSGI file
4. Set static files path: `/static/` → `/path/to/staticfiles/`

## Notes

- Only authenticated users can create/update/delete reviews
- Ratings must be between 1 and 5
- OMDB API key required for movie search
- Static files must be collected before deployment

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Django REST Framework
- OMDB API
- Bootstrap 5
- Font Awesome
- Google Fonts (Oswald & Open Sans)

---

**Built with love for movie lovers**
