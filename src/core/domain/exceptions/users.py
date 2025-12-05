from src.core.exceptions.custom import DuplicatedException, NotFoundException


class UserEmailDuplicatedException(DuplicatedException):
    code = 'USER_EMAIL_DUPLICATED_ERROR'


class UserNotFoundException(NotFoundException):
    code = 'USER_NOT_FOUND_ERROR'


__all__ = [
    'DuplicatedException',
    'UserEmailDuplicatedException',
    'UserNotFoundException',
    'NotFoundException',
]
