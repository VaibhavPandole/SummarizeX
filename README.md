# SummarizeX
A powerful AI tool that quickly converts long texts into concise summaries and clear bullet points, saving you time and enhancing productivity.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.11 or higher
- Other dependencies are listed in the requirements.txt file

## Local Dev Setup
##### Steps to install and run application on your local machine.
* Run `$ cd ..` command for jump out from the project directory
* Run `$ python3.11 -m venv env` command to Create Virtual environment
* Run `$ source env/bin/activate` command to activate virtual environment
* Run `$ cd SummerizeX` command for jump into the project directory
* Run `$ pip install -r requirements.txt` command to Install project requirement file
* Run `$ python manage.py migrate` command to apply migrations on your local machine
* Run `$ python manage.py runserver` command to run project on your local machine
* Run `$ python manage.py test` command to run the unittest case on your local machine

## API Endpoints
### User Registration
- **Endpoint**: `POST http://127.0.0.1:8000/api/user-registration/`
- **Request Body**:
    ```
  {"email": "abc@xyz.com",
  "password": "secret_password"}
  ```
- **Response**:
    ```
  "User registered successfully"
  ```
  
### Generate User Access Token
- **Endpoint**: `POST http://127.0.0.1:8000/api/token/`
- **Request Body**:
    ```
  {"username": "abc@xyz.com",
  "password": "secret_password"}
  ```
- **Response**:
    ```
  {"refresh_token": "encrypted_refresh_token",
  "access_token": "encrypted_access_token"}
  ```
  
### Generate Refresh Token
- **Endpoint**: `POST http://127.0.0.1:8000/api/token/refresh/`
- **Request Body**:
    ```
  {"refresh": "encrypted_refresh_token"}
  ```
- **Response**:
    ```
  {"access": "encrypted_access_token"}
  ```
  
### Generate Summary
- **Endpoint**: `POST http://127.0.0.1:8000/api/generate-summary/`
- **Request Body**:
    ```
  {"text": "your long text here"}
  ```
- **Headers**:
    ```
  {"Authorization": "Bearer encrypted_access_token"}
  ```
- **Response**:
    ```
  {
  "original_text": "your long original text",
  "summary": "openai summary",
  "bullet_points": ""
  }
  ```
  
### Generate Bullet Points
- **Endpoint**: `POST http://127.0.0.1:8000/api/generate-bullet-points/`
- **Request Body**:
    ```
  {"text": "your long text here"}
  ```
- **Headers**:
    ```
  {"Authorization": "Bearer encrypted_access_token"}
  ```
- **Response**:
    ```
  {
  "original_text": "your long original text",
  "summary": "",
  "bullet_points": "bullet points from your original text"
  }
  ```