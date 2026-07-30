import secrets
import string

# Generate a secure JWT secret
jwt_secret = secrets.token_hex(32)
jwt_refresh_secret = secrets.token_hex(32)

print(f"JWT_SECRET={jwt_secret}")
print(f"JWT_REFRESH_SECRET={jwt_refresh_secret}")