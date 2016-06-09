##Getting Started

1. Clone Repository

2. Create a python3 virtual environment for this project

3. Install requirements
  ```
  pip install -r requirements.txt
  ```
4. Create a PostgreSQL Database and configure the project's DATABASES setting (in settings.py) to use your database.

  ```python
  # https://docs.djangoproject.com/en/1.9/ref/settings/#databases
  # Example Configuration
  
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': 'wall',
          'USER': 'walluser',
          'PASSWORD': 'wallpass',
          'HOST': '127.0.0.1',
          'PORT': '5432',
      }
  }
  ```
5. Apply migrations (this will create a default admin user, `username: admin` `password:admin`)

  ```
  python manage.py migrate
  ```
6. Start the development server

  ```
  python manage.py runserver 0.0.0.0:9000
  ```
