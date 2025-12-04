from src.core.exceptions.custom import DuplicatedException


class UserEmailDuplicatedException(DuplicatedException):
    code = 'USER_EMAIL_DUPLICATED_ERROR'
