import bcrypt
def check_password(password):
    return bcrypt.checkpw(password.encode('utf-8'), password.encode('utf-8'))
