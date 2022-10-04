# FastAPI Assignment for Rosela

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/kevinnguyenai/rosela-pai/tree/main)


## TO DO:
- add dotenv by `python-dotenv` 
- add alembic to control change migrations for database
- use SQLite
- use SQLAlchemy for ORM
- add Dockerfile
- add Docker-compose

## Application
 `main.py` is main application script to bootstrap fastapi application
 `localapp.sh` is script to bootstrap application
 `.env.loal` is default environment variable file use in local development, `copy .env.local .env` and bootstrap application by `./localapp.sh`