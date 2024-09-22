#!/bin/sh


python manage.py migrate

python manage.py clear_cache

python manage.py delete_posts
python manage.py delete_users

python manage.py seed_users
python manage.py seed_blog_posts

python manage.py collectstatic --noinput

exec python manage.py runserver 0.0.0.0:8000
