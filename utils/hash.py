from passlib.hash import bcrypt

# دالة لتشفير الباسورد
def hash_password(password: str) -> str:
    return bcrypt.hash(password)

# دالة للتحقق من الباسورد
def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.verify(password, hashed)