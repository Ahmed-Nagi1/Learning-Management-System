# Learning Management System (LMS) API

Welcome to the Learning Management System (LMS) API! This project is a robust and scalable backend solution built with Django and Django Rest Framework (DRF). It is designed to manage courses and their associated modules, providing a structured and secure platform for educational content delivery.

## Features

- **Course Management**: Create, update, retrieve, and delete courses. Each course is tied to an instructor for proper ownership.
- **Module Management**: Organize course content into modules with customizable ordering. Only the course instructor can modify modules.
- **Authentication & Permissions**: Secure access using Token Authentication and IsAuthenticated permissions.
- **RESTful API Design**: Follows REST principles with hyperlinked relationships for intuitive navigation.
- **Custom Query Logic**: Retrieve modules filtered by course ID for efficient data access.

## Technologies Used

- **Backend**: Django, Django Rest Framework (DRF)
- **Authentication**: dj-rest-auth & django-alluth
- **Database**: PostgreSQL
- **API Documentation**: Auto-generated using drf_yasg browsable API.

## Getting Started


# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  

## Local Development

Start the dev server for local development:
```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```

## API Endpoints

This project includes a fully interactive API documentation powered by drf_yasg, a library for generating Swagger and ReDoc documentation for Django REST Framework (DRF).
Features

* Interactive Swagger UI: Test API endpoints directly within the browser.
* ReDoc Interface: Professionally styled documentation for better readabi* lity.
* Auto-generated: No need to write documentation manually; drf_yasg extracts t* he information from DRF views and serializers.

## Contributing

Contributions are welcome! If you’d like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes with clear and descriptive messages.
4. Push your branch and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Built with ❤️ using Django and Django Rest Framework.
- Inspired by the need for scalable and secure e-learning solutions.

Feel free to explore the API and contribute to its development. For any questions or feedback, please open an issue or contact the maintainers. Happy coding! 🚀

This README is clear, concise, and provides all the necessary information for users and contributors.




[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Settings

Moved to [settings](https://cookiecutter-django.readthedocs.io/en/latest/1-getting-started/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy lms

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/2-local-development/developing-locally.html#using-webpack-or-gulp).

### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd lms
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd lms
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd lms
celery -A config.celery_app worker -B -l info
```

### Email Server

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server [Mailpit](https://github.com/axllent/mailpit) with a web interface is available as docker container.

Container mailpit will start automatically when you will run all docker containers.
Please check [cookiecutter-django Docker documentation](https://cookiecutter-django.readthedocs.io/en/latest/2-local-development/developing-locally-docker.html) for more details how to start all containers.

With Mailpit running, to view messages that are sent by your application, open your browser and go to `http://127.0.0.1:8025`

### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at <https://sentry.io/signup/?code=cookiecutter> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](https://cookiecutter-django.readthedocs.io/en/latest/3-deployment/deployment-with-docker.html).
