import hashlib

KEY = "MK7Bl7O903"


def generate_email_hash(email):
    return hashlib.sha224( email+KEY).hexdigest()