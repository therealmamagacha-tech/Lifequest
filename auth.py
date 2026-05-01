import json
import os
import hashlib
import hmac
import re

try:
    import requests as _requests
    _HAS_REQUESTS = True
except ImportError:
    _HAS_REQUESTS = False

USER_DIR = "users_data"

# Créer le dossier s'il n'existe pas (utile en local)
if not os.path.exists(USER_DIR):
    os.makedirs(USER_DIR)

SALT = b"lifequest_salt_2026"

# --- Firebase helper (utilisé sur Streamlit Cloud si FIREBASE_URL est défini) ---

def _firebase_url():
    """Retourne l'URL de base Firebase ou None si non configuré."""
    try:
        import streamlit as st
        url = st.secrets.get("FIREBASE_URL", "")
        if url:
            return url.rstrip("/")
    except Exception:
        pass
    return os.getenv("FIREBASE_URL", "").rstrip("/") or None

def _use_firebase():
    return _HAS_REQUESTS and bool(_firebase_url())

def _fb_get(username):
    """Charge les données d'un utilisateur depuis Firebase."""
    url = f"{_firebase_url()}/users/{username.lower()}.json"
    r = _requests.get(url, timeout=5)
    if r.status_code == 200 and r.json() is not None:
        return r.json()
    return None

def _fb_set(username, data):
    """Enregistre les données d'un utilisateur dans Firebase."""
    url = f"{_firebase_url()}/users/{username.lower()}.json"
    r = _requests.put(url, json=data, timeout=5)
    if r.status_code not in (200, 204):
        raise RuntimeError(f"Firebase write error {r.status_code}: {r.text}")

def _is_valid_username(username):
    """Autorise uniquement lettres, chiffres, tirets et underscores (3-32 chars)."""
    return bool(re.match(r'^[a-zA-Z0-9_\-]{3,32}$', username))

def hash_password(password):
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), SALT, 260000)
    return dk.hex()

def save_user(username, data):
    if not _is_valid_username(username):
        raise ValueError("Nom d'utilisateur invalide.")
    if _use_firebase():
        _fb_set(username, data)
    else:
        file_path = os.path.join(USER_DIR, f"{username.lower()}.json")
        with open(file_path, "w") as f:
            json.dump(data, f)

def load_user(username, password):
    if not _is_valid_username(username):
        return None
    if _use_firebase():
        data = _fb_get(username)
    else:
        file_path = os.path.join(USER_DIR, f"{username.lower()}.json")
        if not os.path.exists(file_path):
            return None
        with open(file_path, "r") as f:
            data = json.load(f)
    if data and hmac.compare_digest(data.get("password", ""), hash_password(password)):
        return data
    return None

def user_exists(username):
    if not _is_valid_username(username):
        return False
    if _use_firebase():
        return _fb_get(username) is not None
    return os.path.exists(os.path.join(USER_DIR, f"{username.lower()}.json"))