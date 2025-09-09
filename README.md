# KickoffKart — Football Shop (Assignment 2)

**Live URL (PWS):** https://<replace-with-your-domain>.stndar.dev/

**Identity shown on the site**
- App: **KickoffKart**
- Name: **Juansao Fortunio Tandi**
- Class: **KKI**
- NPM: **2406365345**

---

## 1. Step-by-step implementation of the checklist
I started from scratch, not reusing the Tutorial 1 project:  

1. **Project setup**  
   - Made a new repo named `kickoffkart`.  
   - Set up a Python virtual environment, installed dependencies (`django`, `whitenoise`, `gunicorn`, `psycopg2-binary`, `python-dotenv`, etc.), and created `.env` files to separate local vs production settings.  
   - Added a `.gitignore` to ignore venv, `__pycache__`, `db.sqlite3`, `.env`, and collected staticfiles.  

2. **New Django project**  
   - Ran `django-admin startproject kickoffkart .` so `manage.py` is at the root.  
   - Configured `settings.py` to load environment variables and switch between SQLite (local) and PostgreSQL (PWS).  

3. **Main app + routing**  
   - Created a new app `main` and added it to `INSTALLED_APPS`.  
   - In `kickoffkart/urls.py`, included `main.urls`.  
   - In `main/urls.py`, mapped the root URL to the `show_main` view.  

4. **Model**  
   - Implemented a `Product` model with all six required fields (`name`, `price`, `description`, `thumbnail`, `category`, `is_featured`).  
   - Ran `makemigrations` and `migrate` to create the database schema.  

5. **Views & Templates**  
   - Created `show_main` in `views.py` to load all products, pass identity info (app name, my name, class, NPM), and render it using `main.html`.  
   - Designed `main.html` using Bootstrap for layout. Added `{% load static %}` so images stored in `main/static/main/` display correctly.  

6. **Static images & Fixtures**  
   - Placed actual product images (ball and gloves) in `main/static/main/`.  
   - Created `two_products.json` fixture containing two sample products, one featured and one not.  
   - Loaded data with `python manage.py loaddata two_products`.  

7. **Deployment**  
   - Added my PWS host to `ALLOWED_HOSTS`.  
   - Pushed the repo to PWS.  
   - On PWS, ran `collectstatic`, `migrate`, and `loaddata` so the site works with real images.  

---

## 2. Request → Response diagram & explanation

```mermaid
sequenceDiagram
    participant Client as Browser
    participant Project as urls.py (project)
    participant App as urls.py (main)
    participant View as views.py (show_main)
    participant Model as models.py (Product)
    participant Template as main.html

    Client->>Project: GET /
    Project->>App: forward to main.urls
    App->>View: call show_main(request)
    View->>Model: Product.objects.all()
    Model-->>View: QuerySet (products)
    View->>Template: render("main.html", context)
    Template-->>View: HTML
    View-->>Client: HttpResponse (rendered page)
Relationship explanation

urls.py (project) delegates root requests to main/urls.py.

main/urls.py maps "" to show_main in views.py.

views.py queries the Product model from models.py.

views.py passes identity + product data to main.html.

main.html is rendered and returned as the final response to the client.

3. Role of settings.py in a Django project
Central configuration file controlling the whole project.

Defines installed apps, middleware, template engine, static file handling, and database connections.

Stores security settings (SECRET_KEY, DEBUG, ALLOWED_HOSTS).

In this project, it also loads environment variables and configures WhiteNoise for static files in production.

4. How database migration works in Django
When models are changed, Django compares the new definitions with the current database schema.

python manage.py makemigrations generates migration files (like a step-by-step change log).

python manage.py migrate applies those changes to the database (create tables, add/modify columns, etc.).

This keeps the database schema synchronized with the Python models over time.

5. Why Django is chosen as a starting framework
Batteries included: comes with ORM, routing, template engine, static files, and security features out of the box.

Clear structure: MVT pattern encourages separation of concerns.

Mature & well-documented: easy to find tutorials, docs, and community support.

Scalable: good for small class assignments but also used in real production.

Focus on concepts: helps students learn core ideas of web development (models, views, templates, static files, deployment) without needing to install many separate packages.

6. Any feedback for the teaching assistant
PBP/PBD KKI TAs so far have been really helpful in every tutorials. I like the idea of separating us into several breakhout rooms, each managed by 1 TA. The weight of the tutorial is also still reasonable to finish within the time limit. Overall, my feedback is only positive, and I don't have any criticism.
