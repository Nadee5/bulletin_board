import random
import string


def generate_new_password(length=12):
    """Генерация нового пароля.
    Использует: строчные и заглавные англ. буквы, цифры от 0-9, знаки пунктуации."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))
