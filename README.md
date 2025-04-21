# 🧪 API Testing with Python

This project demonstrates a basic API testing setup using `requests` and pure Python. It targets [reqres.in](https://reqres.in), a free API for practice.

## ✅ What It Tests:
- `POST /api/login` with valid and invalid credentials
- `GET /api/users/{id}` for existing and non-existing users
- `POST /api/users` to create a user
- `PUT /api/users/{id}` to update a user
- `DELETE /api/users/{id}` to delete a user

## 📁 Project Structure

api-testing


## 🧪 How to Run
Install dependencies:
```bash
pip install -r requirements.txt

Run the tests:

python api_test.py

🗂️ Output

    test_results.csv: Logs test outcomes with status, message, and duration

    log.txt: Logs unexpected exceptions

