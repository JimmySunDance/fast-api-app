[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# To Run
## Install requirements 
```
pip install -r requirements.txt
```
## Run app
```
uvicorn app.main:app --reload
```

## Swagger
```
http://127.0.0.1:8000/docs
```

## Generate secret key
```
openssl rand -hex 32
```

## Run Black formatter
```
black .
```

## Key alembic commands
- new revision
```
alembic revision -m '< message >'
```
- upgrade to latest
```
alembic upgrade head
```
- downgrade
```
alembic downgrade -1
alembic downgrade < revision number>
```
- auto build revision based off models file
```
alembic revision --autogenerate -m '< message >'
```

# Heroku
- Deploy Updates
```
git push heroku HEAD:master
```

- Restart app
```
heroku ps:restart
```

- App information
```
heroku apps:info fastapi-jpoulten
```

# Alembic on Heroku
```
heroku run alembic upgrade head
```

# Docker
- Build an image
```
docker build -t < name > .
```
- run api in docker container
```
docker-compose -f docker-compose-dev.yml up -d
docker-compose exec < name > alembic upgrade head
```
- close container
```
docker-compose -f docker-compose-dev.yml down
```