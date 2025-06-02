# Online shop
Behold My Awesome Project!

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

## Settings

Moved to [settings](https://cookiecutter-django.readthedocs.io/en/latest/1-getting-started/settings.html).

## Basic Commands

### 1. Starting project

 - To start project on ur local machine, run:
```bash
      docker compose -f docker-compose.local.yml up --build
```
### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### 2. setup elastisearch index
 - To setup elastisearch index, run:
```bash
    docker exec -it market_local_django python manage.py search_index --rebuild
```

### 3. Load data
 - U can load data from external sqlite database (--dry-run) optional:
```bash
    docker exec -it market_local_django python manage.py import_products_from_sql
```
