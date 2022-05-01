# Conditioners

## Deployed on [Heroku](https://conditioners-django.herokuapp.com/)

### How to start the project?

### For Windows:
```
  pipenv shell
```
```
  pipenv install django django-sslserver pillow
```
```
  python manage.py runsslserver
```

### For Linux:
```
  pipenv --python 3.10
```
```
  pipenv shell
```
```
  pipenv install django django-sslserver pillow
```
```
  python manage.py runsslserver
```

### Administrative credentials
```
  username: admin
```
```
  password: admin
```
If any problems occure by administrative login run:
```
  python manage.py createsuperuser
```
