# WalletWise

WalletWise is an API designed to manage user balances and facilitate money transfers between users within the system. Each user has their own balance, initially set to 0. The API provides endpoints to increase a user's balance, transfer money between users, and retrieve the current balance of an authenticated user in rubles.
## DETAILED
https://documenter.getpostman.com/view/17813834/2sA2r53kAr 

## Features

- **Increase balance:** Allows users to increase their balance by a specified amount.
- **Transfer balance:** Enables users to transfer balance from their account to another user's account.
- **Check balance in rubles:** Retrieves the current balance of the authenticated user in rubles.
- **Get operations history:** Retrieves the last operations history for the authenticated user.

## Technologies Used

- **Django:** Web framework for building APIs
- **Django Rest Framework (DRF):** Toolkit for building Web APIs in Django
- **PostgreSQL:** Database management system
- **Docker:** Containerization platform for easy deployment

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ShchelkunovaNata/WalletWise.git
   ```

 2.**Navigate to the project directory:**

  ```bash
    cd WalletWise
  ```
3. **Create a virtual environment and activate it:**

```bash
    python3 -m venv env
    source env/bin/activate
```

4. **Install dependencies:**
```bash
    pip install -r requirements.txt
    Create a .env file in the project directory and add the following environment variables:

    makefile
    SECRET_KEY=your_secret_key
    DEBUG=True
```
5. **Apply migrations:**

```bash
    python manage.py migrate
    Run the development server:
```

```bash
python manage.py runserver
Access the API at http://127.0.0.1:8000/api/v1/
```
