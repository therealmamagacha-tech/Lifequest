import json
import os
import hashlib
import hmac
import re

USER_DIR = "users_data"

# Créer le dossier s'il n'existe pas
if not os.path.exists(USER_DIR):
    os.makedirs(USER_DIR)

SALT = b"lifequest_salt_2026"

def _is_valid_username(username):
    """Autorise uniquement lettres, chiffres, tirets et underscores (3-32 chars)."""
    return bool(re.match(r'^[a-zA-Z0-9_\-]{3,32}$', username))

def hash_password(password):
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), SALT, 260000)
    return dk.hex()

def save_user(username, data):
    if not _is_valid_username(username):
        raise ValueError("Nom d'utilisateur invalide.")
    file_path = os.path.join(USER_DIR, f"{username.lower()}.json")
    with open(file_path, "w") as f:
        json.dump(data, f)

def load_user(username, password):
    if not _is_valid_username(username):
        return None
    file_path = os.path.join(USER_DIR, f"{username.lower()}.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
            if hmac.compare_digest(data["password"], hash_password(password)):
                return data
    return None

def user_exists(username):
    if not _is_valid_username(username):
        return False
    return os.path.exists(os.path.join(USER_DIR, f"{username.lower()}.json"))