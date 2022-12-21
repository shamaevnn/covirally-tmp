import bcrypt


def get_password_hash(password: str) -> str:
    """
    password: пароль, который пользователь вводит при логине
    return: хэш пароля, который хранится в базе данных
    """
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    decoded_password: str = hashed_password.decode("utf-8")
    return decoded_password


def password_is_correct(password: str, hashed_password: str) -> bool:
    res: bool = bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    return res
