This is an RSS Reader API designed to database articles and the tags they use so that they can be filtered by user specified keywords  
This was designed as the back end for the React News App https://github.com/tslocom/news-app-react  
To use this backend, first run python -m venv venv then use source venv/bin/activate to run the venv  
Then do your migrations using python manage.py makemigrations and python manage.py migrate  
Then you can run the scraper file with python articles/scraper.py  
You will then need to create your own Django superuser with python manage.py createsuperuser and follow the prompts  
You can now use the admin panel to view the database using python manage.py runserver and go to the localhost link provided but you must add /admin at the end