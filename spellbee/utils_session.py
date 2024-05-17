import random
import string


def generate_session_id() -> str:
    """ Generates a unique session id for each call """
    length = 10
    letters = string.ascii_letters + string.digits
    session_id = ''.join(random.choice(letters) for _ in range(length))
    return session_id



