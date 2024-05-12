# Library Project
#### This project is a library management system built using Django and Django Rest Framework (DRF). It allows users to manage books, authors, library copies, reservations, and more.

## Stack
- Django
- Python
- Django Rest Framework (DRF)
- Pytest

## Features
- CRUD operations for books, authors, library copies, and reservations.
- User authentication and authorization.
- Search and filtering functionality.
- API endpoints for integration with other systems.

## Installation
1. Clone the repository:
```shell
git clone https://github.com/TkachNekit/library
```
2. Navigate to the project directory:
```shell
cd library
```
3. Create a virtual environment:
```shell
python -m venv env
```
4. Activate the virtual environment: <br>
On Windows:
```shell
env\Scripts\activate
```
On macOS and Linux:
```shell
source env/bin/activate
```
5. Install the dependencies:
```shell
pip install -r requirements.txt
```
6. Run migrations:
```shell
python manage.py migrate
```
7. Create a superuser:
```shell
python manage.py createsuperuser
```
8. Start the development server:
```shell
python manage.py runserver
```
## Usage
1. Access the admin panel:
```http request
http://127.0.0.1:8000/admin/
```
2. Log in with the superuser credentials created during installation.
3. Explore the available models and manage data.
4. Access the API endpoints:
```http request
http://127.0.0.1:8000/api/
```
## Testing
To run the tests, use the following command:
```shell
pytest
```

© Tkachenko Nikita | 2024