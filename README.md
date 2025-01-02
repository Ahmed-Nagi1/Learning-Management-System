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
- **Authentication**: Token Authentication
- **Database**: PostgreSQL (or any Django-supported database)
- **API Documentation**: Auto-generated using DRF’s browsable API.

## Getting Started

### Prerequisites

- Python 3.8+
- Django 5.0+
- Django Rest Framework 3.14+

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/lms-api.git
    cd lms-api
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser for admin access:
    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

## API Endpoints

### Courses

- `GET /courses/` - List all courses.
- `POST /courses/` - Create a new course.
- `GET /courses/{id}/` - Retrieve a specific course.
- `PUT /courses/{id}/` - Update a course.
- `DELETE /courses/{id}/` - Delete a course.

### Modules

- `GET /modules/?course_id={id}` - List modules for a specific course.
- `POST /modules/` - Create a new module.
- `GET /modules/{id}/` - Retrieve a specific module.
- `PUT /modules/{id}/` - Update a module.
- `DELETE /modules/{id}/` - Delete a module.

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

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  

# Local Development

Start the dev server for local development:
```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```
