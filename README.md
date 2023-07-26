### Description
The application where users can publish recipes, add other users' recipes to favorites, and subscribe to publications from other authors. The 'Shopping List' feature allows users to create a list of ingredients needed to prepare selected dishes. There is an option to export a text file with a list of required ingredients for the recipes.

## Technologies:
- Django
- Python
- Docker

## Installation
- Clone the repository:
```
git clone git@github.com:HukumaBob/foodgram-project-react.git
```

- Collect images
```
cd frontend 
docker build -t username/foodgram_frontend .
cd ../backend  
docker build -t username/foodgram_backend .
cd ../infra  
docker build -t username/foodgram_nginx . 
```
- Building Containers:
From the 'infra/' directory, deploy the containers using docker-compose:
```
docker-compose up -d --build
```
- Apply migrations:
```
docker-compose exec backend python manage.py migrate
```
- Create superuser:
```
docker-compose exec backend python manage.py createsuperuser
```
- Collect static files:
```
docker-compose exec backend python manage.py collectstatic --no-input
docker-compose exec backend cp -r /app/static/. /static/
```
- Run the command:
```
docker-compose exec backend python manage.py convert_csv

```
### Preparing for Project Deployment on a Remote Server:

Create the .env file in the 'infra' directory:
```
ALLOWED_HOSTS=yourhost 158.160.xxx.xxx 127.0.0.1 localhost backend
SECRET_KEY=yoursecretkey
POSTGRES_USER=django_user
POSTGRES_PASSWORD=mysecretpassword
POSTGRES_DB=django
DB_HOST=db
DB_PORT=5432
```


