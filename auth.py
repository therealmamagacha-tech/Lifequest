import json
import os
import hashlib

USER_DIR = "users_data"

# Créer le dossier s'il n'existe pas
if not os.path.exists(USER_DIR):
    os.makedirs(USER_DIR)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_user(username, data):
    file_path = os.path.join(USER_DIR, f"{username.lower()}.json")
    with open(file_path, "w") as f:
        json.dump(data, f)

def load_user(username, password):
    file_path = os.path.join(USER_DIR, f"{username.lower()}.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
            if data["password"] == hash_password(password):
                return data
    return None

def user_exists(username):
    return os.path.exists(os.path.join(USER_DIR, f"{username.lower()}.json"))