## Database

The project uses PostgreSQL as its primary database.

PostgreSQL runs as a Docker Compose service, and Django connects to it using environment variables.

Database configuration is managed through `config/settings.py`.
Database credentials are provided through the `.env` file.