# EchoFree News — Backend API

A Django REST API powering the EchoFree News platform, a full-stack news aggregation application designed to help users break out of the "echo chamber". The backend handles article ingestion, user tag management, and parsing via a custom RSS scraper that aggregates content from ~50 publications on an automated schedule.

**Frontend repo:** [news-app-react](https://github.com/tslocom/news-app-react)  
**Live frontend:** [news-app-react-theta-six.vercel.app](https://echofreenews.com)

---

## Features

- **Custom RSS scraper** — aggregates articles from ~50 news publications using `feedparser`, with conditional logic to handle disparate source formats and make all entries uniform
- **Hand-written SQL:** all database queries are written directly, without ORM abstraction, giving full control over schema design and query performance
- **RESTful API:** built with Django REST Framework, providing endpoints for articles, tags, and user preferences
- **Automated ingestion:** scraper runs on a Railway cron job every 3 hours, keeping the article database current
- **User tag system:** users follow tags; the API filters and returns articles matched to their preferences
- **Django admin panel:** full admin interface for database inspection and content management
- **Production deployment:** containerized with a custom Dockerfile, deployed to Railway with a Railway-hosted MySQL database

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Framework | Django 6 + Django REST Framework |
| Database | MySQL (production via Railway) |
| Scraping | feedparser |
| Server | Gunicorn |
| Containerization | Docker |
| Deployment | Railway |
| Environment | python-dotenv |

---

## Project Structure

```
news_api_python/
├── articles/
│   ├── models.py        # Article and Tag schema (no ORM for queries)
│   ├── views.py         # API endpoints
│   ├── serializers.py   # DRF serializers
│   └── scraper.py       # RSS scraper — run this to seed the database
├── users/
│   ├── models.py        # User and tag preference schema
│   └── views.py         # User endpoints
├── news_api_python/
│   ├── settings.py      # Django configuration
│   └── urls.py          # URL routing
├── Dockerfile           # Production container config
├── requirements.txt     # Python dependencies
└── manage.py
```

---

## Getting Started (Local Development)

### Prerequisites
- Python 3.10+
- pip

### Setup

```bash
# Clone the repo
git clone https://github.com/tslocom/news_api_python.git
cd news_api_python

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# Create an admin user
python manage.py createsuperuser

# Start the development server
python manage.py runserver

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env            # Edit with your database credentials

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Fill publications, as well as initial articles and tags in the database by running the scraper
python articles/scraper.py
```

Then visit `http://localhost:8000/admin` to view the database and manage content.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/articles/` | List all articles |
| GET | `/articles/?tag=<tag>` | Filter articles by tag |
| GET | `/tags/` | List all available tags |
| POST | `/users/` | Create a user |
| GET | `/users/<id>/tags/` | Get a user's followed tags |
| POST | `/users/<id>/tags/` | Add a tag to a user's feed |

---

## Deployment

The API is containerized using a custom `Dockerfile` and deployed to **Railway**. The Railway cron job runs `python articles/scraper.py` every 3 hours to keep the article database current. The MySQL database is also hosted on Railway.

```dockerfile
# Dockerfile (summary)
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "news_api_python.wsgi:application", "--bind", "0.0.0.0:8000"]
```

---

## Dependencies

```
Django 6.0.3
djangorestframework 3.17.1
django-cors-headers 4.9.0
feedparser 6.0.12
PyMySQL 1.1.3
gunicorn 26.0.0
python-dotenv 1.2.2
```

---

## Related

- [Frontend — news-app-react](https://github.com/tslocom/news-app-react)