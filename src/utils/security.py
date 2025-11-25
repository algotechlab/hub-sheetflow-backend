from argon2 import PasswordHasher
from argon2.exceptions import (
    InvalidHash,
    VerificationError,
    VerifyMismatchError,
)


# Criamos um hasher padrão seguro
ph = PasswordHasher()


def get_password_hash(password: str) -> str:
    """
    Gera o hash Argon2 de uma senha em texto plano.
    """
    return ph.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha digitada corresponde ao hash armazenado.
    """
    try:
        return ph.verify(hashed_password, plain_password)
    except (VerifyMismatchError, VerificationError, InvalidHash):
        return False
