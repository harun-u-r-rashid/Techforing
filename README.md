

`🗂️ VS Code Project Structure:`

- `appAuth`: Contains models, serializers, views and urls of user authentication.
- `appProject`: Contains models, serializers, views and urls of project.
- `appTask`: Contains models, serializers, views and urls of task and comment.


`🚀 Guide to set up the project, migrate the database and run the server:`

- Create virtual environment : `python -m venv env`
- Active virtual environment : `env/Scripts/activate`
- Install Django : `pip install django`
- Install Django Environ : `pip install django-environ`
- Install Jazzmin : `pip install django-jazzmin`
- Install rest framework : `pip install djangorestframework`
- Install simplejwt : `pip install djangorestframework-simplejwt`
- Install Corsheaders : `pip install django-cors-headers`
- Install drf spectacular : `pip install drf-spectacular`
- Run migration command: `py manage.py makemigrations`
- Run migrate command : `py manage.py migrate`
- Create Superuser : `py manage.py createsuperuser` (Give Email, Username,First name, Last name, Password, Password again)
- Run server : `py manage.py runserver`