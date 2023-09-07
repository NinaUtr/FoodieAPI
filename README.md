# Foodie API

## Overview
This is a simple API that allows you to perform CRUD operations on recipes, manage user accounts, and implement authorization. Additionally, there's an asynchronous function to fetch random recipes from an external API, provided you have a registered API key and store it in the `.env` file.

## Getting Started
To set up and run the application, follow these steps:

1. Create a `.env` file with the following environment variables:

```env
DB_USER=
DB_PASSWORD=
DB_NAME=
DATABASE_URL=postgresql://(DB_USER):(DB_PASSWORD)@database:5432/(DB_NAME)
JWT_SECRET=
RANDOM_RECIPE_API_KEY=
```

2. For Alembic database migrations, update the `alembic.ini` file:

```ini
sqlalchemy.url = postgresql://(DB_USER):(DB_PASSWORD)@database:5432/(DB_NAME)
```

## Usage
- Use the API to create, update, delete, and search for recipes.
- Manage user accounts, including user creation and authentication.
- Utilize authorization features to secure your endpoints.
- Access random recipes from an external API by registering (https://api.spoonacular.com) and adding your API key to the `.env` file as `RANDOM_RECIPE_API_KEY`.

## Starting the Application

1. Start the containers using `docker-compose`:

```bash
docker-compose up
```

Ensure that both the application and database containers are up and running.

2. In a separate terminal, migrate the database by executing the following command:

```bash
docker-compose exec backend bash -c "alembic upgrade head"
```

This command will apply any pending database migrations and update the database schema to the latest version defined in your Alembic migration scripts.

Now, your application should be up and ready to use.



