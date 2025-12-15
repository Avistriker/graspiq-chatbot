# generate_secret.py
import secrets
import string

# Method 1: Hex string (recommended for Flask)
hex_key = secrets.token_hex(32)
print(f"Hex Key (Recommended): {hex_key}")
print(f".env format: FLASK_SECRET_KEY={hex_key}")

# Method 2: URL-safe string
url_key = secrets.token_urlsafe(32)
print(f"\nURL-safe Key: {url_key}")
print(f".env format: FLASK_SECRET_KEY={url_key}")

# Method 3: Random string with mixed characters
chars = string.ascii_letters + string.digits + "!@#$%^&*()"
mixed_key = ''.join(secrets.choice(chars) for _ in range(50))
print(f"\nMixed Key: {mixed_key}")
print(f".env format: FLASK_SECRET_KEY={mixed_key}")