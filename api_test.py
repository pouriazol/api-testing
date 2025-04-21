import requests
import json
import csv
import time
from datetime import datetime

# ---------------------------
# Configuration and Constants
# ---------------------------
BASE_URL = "https://reqres.in"
LOGIN_ENDPOINT = "/api/login"
USER_ENDPOINT = "/api/users"
CREATE_ENDPOINT = "/api/users"
DELETE_ENDPOINT = "/api/users"
TEST_DATA_FILE = "test_data.json"
RESULTS_FILE = "test_results.csv"
ERROR_LOG_FILE = "log.txt"

# ---------------------------
# Utility Functions
# ---------------------------

def load_test_data():
    with open(TEST_DATA_FILE, "r") as f:
        return json.load(f)

def log_result(test_name, status, message, duration):
    with open(RESULTS_FILE, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, test_name, status, message, f"{duration:.2f}s"])

def log_error(error_msg):
    with open(ERROR_LOG_FILE, "a") as f:
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        f.write(f"{timestamp} {error_msg}\n")

# ---------------------------
# Test Functions
# ---------------------------

def test_login_success():
    test_name = "Login with Valid Credentials"
    data = test_data["valid_login"]
    start = time.time()
    try:
        response = requests.post(BASE_URL + LOGIN_ENDPOINT, json=data)
        duration = time.time() - start
        if response.status_code == 200 and "token" in response.json():
            log_result(test_name, "PASS", "Login successful and token received.", duration)
        else:
            log_result(test_name, "FAIL", f"Unexpected response: {response.text}", duration)
    except Exception as e:
        log_result(test_name, "ERROR", str(e), 0)
        log_error(f"{test_name} - Exception: {e}")

def test_login_failure():
    test_name = "Login with Missing Password"
    data = test_data["invalid_login"]
    start = time.time()
    try:
        response = requests.post(BASE_URL + LOGIN_ENDPOINT, json=data)
        duration = time.time() - start
        if response.status_code == 400 and "error" in response.json():
            log_result(test_name, "PASS", "Proper error returned for missing password.", duration)
        else:
            log_result(test_name, "FAIL", f"Unexpected response: {response.text}", duration)
    except Exception as e:
        log_result(test_name, "ERROR", str(e), 0)
        log_error(f"{test_name} - Exception: {e}")

def test_get_existing_user():
    test_name = "Get User with Valid ID"
    user_id = test_data["valid_user_id"]
    start = time.time()
    try:
        response = requests.get(f"{BASE_URL}{USER_ENDPOINT}/{user_id}")
        duration = time.time() - start
        if response.status_code == 200 and "data" in response.json():
            log_result(test_name, "PASS", "User data retrieved successfully.", duration)
        else:
            log_result(test_name, "FAIL", f"Unexpected response: {response.text}", duration)
    except Exception as e:
        log_result(test_name, "ERROR", str(e), 0)
        log_error(f"{test_name} - Exception: {e}")

def test_get_nonexistent_user():
    test_name = "Get User with Invalid ID"
    user_id = test_data["invalid_user_id"]
    start = time.time()
    try:
        response = requests.get(f"{BASE_URL}{USER_ENDPOINT}/{user_id}")
        duration = time.time() - start
        if response.status_code == 404:
            log_result(test_name, "PASS", "404 returned as expected for non-existing user.", duration)
        else:
            log_result(test_name, "FAIL", f"Expected 404, got {response.status_code}", duration)
    except Exception as e:
        log_result(test_name, "ERROR", str(e), 0)
        log_error(f"{test_name} - Exception: {e}")

def test_create_user():
    test_name = "Create User"
    data = test_data["create_user"]
    start = time.time()
    try:
        response = requests.post(BASE_URL + CREATE_ENDPOINT, json=data)
        duration = time.time() - start
        if response.status_code == 201 and "id" in response.json():
            log_result(test_name, "PASS", "User created successfully.", duration)
        else:
            log_result(test_name, "FAIL", f"Unexpected response: {response.text}", duration)
    except Exception as e:
        log_result(test_name, "ERROR", str(e), 0)
        log_error(f"{test_name} - Exception: {e}")

def test_delete_user():
    test_name = "Delete User"
    user_id = test_data["delete_user_id"]
    start = time.time()
    try:
        response = requests.delete(f"{BASE_URL}{DELETE_ENDPOINT}/{user_id}")
        duration = time.time() - start
        if response.status_code == 204:
            log_result(test_name, "PASS", "User deleted successfully (204).", duration)
        else:
            log_result(test_name, "FAIL", f"Expected 204, got {response.status_code}", duration)
    except Exception as e:
        log_result(test_name, "ERROR", str(e), 0)
        log_error(f"{test_name} - Exception: {e}")

# ---------------------------
# Main Execution
# ---------------------------
if __name__ == "__main__":
    test_data = load_test_data()

    with open(RESULTS_FILE, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Timestamp", "Test Name", "Status", "Message", "Duration"])

    print(" Starting API Tests...\n")
    test_login_success()
    test_login_failure()
    test_get_existing_user()
    test_get_nonexistent_user()
    test_create_user()
    test_delete_user()
    print("\n✅ All tests completed. Check 'test_results.csv' and 'log.txt'.")
