import secrets
import string
from uuid import uuid4


def generate_session_token():
	return f"chatter-{uuid4()}"


def generate_random_user_name() -> str:
	return 'user#' + ''.join(secrets.choice(string.digits) for i in range(8))
