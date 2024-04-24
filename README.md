

# Django Authentication and Session Management

This Django project provides a comprehensive solution for user authentication and session management. It includes various views and endpoints to handle user registration, login, logout, password management, and account activation.

## Features

- **User Registration**: Users can register for an account using a simple registration form.
- **Account Activation**: Activation links are sent via email for account verification.
- **User Login and Logout**: Secure login and logout functionality with session management.
- **Password Management**: Users can change their passwords and reset forgotten passwords via email.
- **Profile Management**: User details can be viewed and updated as needed.
- **CSRF Protection**: Includes a CSRF token endpoint for enhanced security.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/DingxDon/Django-Auth-Session.git
cd Django-Auth-Session
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run migrations:

```bash
python manage.py migrate
```

4. Start the development server:

```bash
python manage.py runserver
```

5. Access the application in your browser at `http://localhost:8000`.

## Usage

- Register a new user account by visiting the registration page.
- Activate the account by clicking on the activation link received via email.
- Log in to the application using your credentials.
- Manage your account settings, including password change and profile updates.
- Log out securely when done using the application.

## API Endpoints

- `/accounts/csrf_token/`: Obtain CSRF token.
- `/accounts/registration/`: User registration.
- `/accounts/activate/<str:uid>/<str:token>/`: Activate user account.
- `/accounts/activate/`: Confirm account activation.
- `/accounts/login/`: User login.
- `/accounts/user/`: User details.
- `/accounts/change_password/`: Change password.
- `/accounts/reset_password/<str:uid>/<str:token>/`: Reset password.
- `/accounts/reset_password_confirm/<str:uid>/<str:token>/`: Confirm password reset.
- `/accounts/reset_password/`: Initiate password reset via email.
- `/accounts/logout/`: User logout.
- `/accounts/delete/`: Delete user account.

## Contributors

- DingxDon

## License

This project is licensed under the [MIT License](LICENSE).
