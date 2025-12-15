from src.core.exceptions.custom import DuplicatedException, NotFoundException


class FinanceDuplicatedException(DuplicatedException):
    code = 'USER_EMAIL_DUPLICATED_ERROR'


class FinanceNotFoundException(NotFoundException):
    code = 'FINANCE_NOT_FOUND_ERROR'


__all__ = [
    'DuplicatedException',
    'FinanceDuplicatedException',
    'FinanceNotFoundException',
    'NotFoundException',
]
