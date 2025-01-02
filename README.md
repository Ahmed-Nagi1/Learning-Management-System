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
- **Authentication**: Dj Rest Auth
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
